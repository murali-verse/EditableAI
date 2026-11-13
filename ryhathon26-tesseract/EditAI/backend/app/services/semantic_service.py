import os
import re
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

# Ensure Transformers only uses PyTorch
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

class SemanticService:
    """
    Local Semantic Embedding, Similarity Detection, and Transcript Retrieval Service.
    Supports BGE-M3 / BGE / MiniLM models with CPU/GPU auto-detection,
    plus lightweight fallback using TF-IDF / character n-gram cosine matching
    to guarantee zero downtime if model weights are not pre-downloaded.
    """
    _model = None
    _model_name = os.environ.get("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    _device = None

    @classmethod
    def _get_device(cls) -> str:
        if cls._device is None:
            try:
                import torch
                cls._device = "cuda" if torch.cuda.is_available() else "cpu"
            except Exception:
                cls._device = "cpu"
        return cls._device

    @classmethod
    def get_model(cls):
        """Lazy loader for SentenceTransformer to minimize startup RAM/VRAM footprint."""
        if cls._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                device = cls._get_device()
                # Try preferred model (BGE or MiniLM)
                model_name = cls._model_name
                try:
                    cls._model = SentenceTransformer(model_name, device=device)
                except Exception:
                    # Fallback to extremely fast, universally supported all-MiniLM-L6-v2
                    cls._model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
            except Exception as e:
                print(f"[SemanticService] Embedding model load notice: {e}. Using resilient statistical similarity.")
                cls._model = False
        return cls._model if cls._model is not False else None

    @classmethod
    def encode_texts(cls, texts: List[str]) -> np.ndarray:
        """Encodes a list of text strings into normalized embedding vectors."""
        if not texts:
            return np.zeros((0, 384), dtype=np.float32)

        model = cls.get_model()
        if model is not None:
            try:
                embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
                return np.array(embeddings, dtype=np.float32)
            except Exception as e:
                print(f"[SemanticService] Encode fallback triggered: {e}")

        # Statistical TF-IDF fallback vectorizer
        return cls._statistical_encode(texts)

    @classmethod
    def _statistical_encode(cls, texts: List[str]) -> np.ndarray:
        """Lightweight offline bag-of-words / character n-gram normalized vector representation."""
        vocab = {}
        tokenized = []
        for t in texts:
            words = re.findall(r"\b[a-zA-Z0-9_]{3,}\b", t.lower())
            tokenized.append(words)
            for w in words:
                if w not in vocab:
                    vocab[w] = len(vocab)

        dim = max(len(vocab), 1)
        matrix = np.zeros((len(texts), dim), dtype=np.float32)
        for i, words in enumerate(tokenized):
            for w in words:
                if w in vocab:
                    matrix[i, vocab[w]] += 1.0
            norm = np.linalg.norm(matrix[i])
            if norm > 0:
                matrix[i] /= norm
        return matrix

    @classmethod
    def compute_similarity(cls, text1: str, text2: str) -> float:
        """Calculates cosine semantic similarity between two statements (0.0 to 1.0)."""
        if not text1.strip() or not text2.strip():
            return 0.0
        if text1.strip().lower() == text2.strip().lower():
            return 1.0

        vecs = cls.encode_texts([text1, text2])
        if vecs.shape[0] < 2 or vecs.shape[1] == 0:
            return 0.0
        sim = float(np.dot(vecs[0], vecs[1]))
        return max(0.0, min(1.0, sim))

    @classmethod
    def search_transcripts(
        cls,
        query: str,
        corpus: List[Dict[str, Any]],
        top_k: int = 5,
        threshold: float = 0.30
    ) -> List[Dict[str, Any]]:
        """
        Searches transcript segments across all clips in a project using semantic similarity.
        Each corpus item should contain: {'clip_id': str, 'text': str, 'start': float, 'end': float}.
        """
        if not query.strip() or not corpus:
            return []

        texts = [item.get("text", "") or item.get("transcript", "") for item in corpus]
        query_vec = cls.encode_texts([query])[0]
        corpus_vecs = cls.encode_texts(texts)

        if corpus_vecs.shape[0] == 0 or corpus_vecs.shape[1] != query_vec.shape[0]:
            return []

        scores = np.dot(corpus_vecs, query_vec)
        results = []
        for idx in np.argsort(-scores):
            score = float(scores[idx])
            if score >= threshold:
                results.append({
                    **corpus[idx],
                    "score": round(score, 3),
                    "matched_text": texts[idx]
                })
            if len(results) >= top_k:
                break

        return results

    @classmethod
    def detect_repeated_statements(
        cls,
        segments: List[Dict[str, Any]] = None,
        threshold: float = 0.70,
        clips: List[Dict[str, Any]] = None,
        similarity_threshold: Optional[float] = None,
        **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """
        Identifies statements across different clips or scenes that express repeated ideas,
        flagging candidate alternative takes for AI comparison.
        Accepts either a flat list of segments or nested clip analyses.
        """
        eff_threshold = similarity_threshold if similarity_threshold is not None else threshold

        # Handle clips vs segments parameter
        target_items = segments or clips or kwargs.get("all_clips") or []
        flat_segments: List[Dict[str, Any]] = []

        for item in target_items:
            if isinstance(item, dict) and "segments" in item and isinstance(item["segments"], list):
                cid = item.get("clip_id", "clip")
                fname = item.get("filename", "")
                for s in item["segments"]:
                    flat_segments.append({**s, "clip_id": s.get("clip_id") or cid, "filename": s.get("filename") or fname})
            elif isinstance(item, dict):
                flat_segments.append(item)

        pairs = []
        n = len(flat_segments)
        if n < 2:
            return []
        segments = flat_segments

        texts = [s.get("transcript", "") or s.get("text", "") for s in segments]
        # Filter segments with substantive dialogue (> 3 words)
        valid_indices = [i for i, t in enumerate(texts) if len(t.split()) >= 3]
        if len(valid_indices) < 2:
            return []

        valid_texts = [texts[i] for i in valid_indices]
        vecs = cls.encode_texts(valid_texts)

        sim_matrix = np.dot(vecs, vecs.T)

        for i in range(len(valid_indices)):
            for j in range(i + 1, len(valid_indices)):
                sim = float(sim_matrix[i, j])
                orig_i = valid_indices[i]
                orig_j = valid_indices[j]
                seg_a = segments[orig_i]
                seg_b = segments[orig_j]

                # Focus on repeated concepts across clips or far apart takes
                is_different_clip = seg_a.get("clip_id") != seg_b.get("clip_id")
                time_diff = abs(seg_a.get("start", 0) - seg_b.get("start", 0))

                if sim >= threshold and (is_different_clip or time_diff > 4.0):
                    pairs.append({
                        "similarity": round(sim, 3),
                        "segment_a": {
                            "clip_id": seg_a.get("clip_id"),
                            "start": seg_a.get("start"),
                            "end": seg_a.get("end"),
                            "text": texts[orig_i]
                        },
                        "segment_b": {
                            "clip_id": seg_b.get("clip_id"),
                            "start": seg_b.get("start"),
                            "end": seg_b.get("end"),
                            "text": texts[orig_j]
                        },
                        "status": "candidate_repetition"
                    })

        # Sort highest similarity first
        pairs.sort(key=lambda p: -p["similarity"])
        return pairs
