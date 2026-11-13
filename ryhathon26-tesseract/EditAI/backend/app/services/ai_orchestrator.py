import os
import time
from typing import Dict, Any, List, Optional, Tuple

from app.services.video_service import VideoService
from app.services.speech_service import SpeechService
from app.services.semantic_service import SemanticService
from app.services.ai_adapter import AIModelAdapter

class AIOrchestrator:
    """
    Centralized Model Orchestration Layer for REELCRAFT AI.
    Dispatches tasks according to the architectural responsibility matrix:
    ----------------------------------------------------------------------
    - Speech Transcription:    Faster-Whisper (GPU/CPU) + companion SRT fallback
    - Scene & Motion Analysis: OpenCV + PySceneDetect + Perceptual dHash
    - Visual Understanding:    Optical Flow Vectors + Qwen2.5-VL / Vision descriptor
    - Semantic Search & Sim:   BGE-M3 / SentenceTransformer Embeddings (Cosine similarity)
    - High-Level Reasoning:    Qwen 2.5 (Ollama 11434 / Cloud fallback)
    - Guardrail Validation:    Python (Deterministic timecode clamping & schema checks)
    ----------------------------------------------------------------------
    """

    @classmethod
    def get_system_diagnostics(cls) -> Dict[str, Any]:
        """Verifies local model availability, GPU hardware status, and runtime readiness."""
        import torch
        cuda_ok = torch.cuda.is_available()
        cuda_dev = torch.cuda.get_device_name(0) if cuda_ok else "None (CPU Active)"

        # 1. Ollama Qwen2.5 check
        ollama_status = AIModelAdapter.get_ollama_status()

        # 2. Embedding model status
        embedding_ready = SemanticService.get_model() is not None

        # 3. Whisper status
        whisper_ready = SpeechService._get_whisper_model() is not None

        return {
            "device": "cuda" if cuda_ok else "cpu",
            "gpu_device": cuda_dev,
            "orchestrator_matrix": {
                "whisper": {
                    "model": os.environ.get("WHISPER_MODEL", "tiny.en"),
                    "status": "ready" if whisper_ready else "fallback_active",
                    "responsibility": "Speech transcription & word timestamps"
                },
                "opencv": {
                    "status": "ready",
                    "responsibility": "Scene detection, motion scoring & perceptual keyframe deduplication"
                },
                "vision": {
                    "status": "ready",
                    "responsibility": "Camera movement estimation (Pan/Tilt/Zoom) & story role tagging"
                },
                "bge_embeddings": {
                    "model": SemanticService._model_name,
                    "status": "ready" if embedding_ready else "statistical_fallback_active",
                    "responsibility": "Semantic search, sentence clustering & repetition detection"
                },
                "qwen2_5_reasoning": {
                    "model": ollama_status.get("active_model") or "qwen2.5:7b",
                    "status": "online" if ollama_status.get("online") else "offline_semantic_engine",
                    "endpoint": ollama_status.get("base_url"),
                    "responsibility": "Hierarchical cross-clip story planning & conversational copilot"
                },
                "python_guardrails": {
                    "status": "active",
                    "responsibility": "Deterministic boundary validation, OTIO interchange & timeline math"
                }
            }
        }

    @classmethod
    def analyze_clip_multimodal(
        cls,
        video_path: str,
        clip_id: str,
        brief: str = ""
    ) -> Dict[str, Any]:
        """
        Orchestrates full multimodal analysis for an individual clip:
        1. Probes duration and media parameters via VideoService.
        2. Detects scenes, camera motion vectors, and keyframe dHash via OpenCV.
        3. Transcribes speech and word boundaries via Faster-Whisper.
        4. Extracts declarative facts and audio turns.
        5. Synthesizes structured clip JSON.
        """
        t0 = time.time()

        # 1. Probe technical specs
        meta = VideoService.probe_media(video_path)
        dur = meta.duration

        # 2. Visual analysis & scenes
        scenes = VideoService.detect_scenes(video_path, dur)

        # 3. Speech transcription
        speech_segs, speech_err = SpeechService.transcribe(video_path, dur)
        facts = []
        if speech_segs:
            full_text = " ".join(s.text for s in speech_segs)
            facts = SpeechService.extract_key_facts(full_text)

        # 4. Integrate scene visuals with spoken transcript
        segments: List[Dict[str, Any]] = []
        if scenes:
            for sc in scenes:
                # Find matching dialogue in this scene time window
                overlap_text = " ".join(
                    s.text for s in speech_segs
                    if not (s.end_time <= sc.start_time or s.start_time >= sc.end_time)
                ).strip()

                quality = 0.85
                if sc.motion_score > 3.0 and sc.motion_score < 25.0:
                    quality += 0.08
                if overlap_text:
                    quality += 0.05

                segments.append({
                    "start": sc.start_time,
                    "end": sc.end_time,
                    "transcript": overlap_text,
                    "visual_summary": sc.visual_description,
                    "camera_movement": sc.camera_movement,
                    "story_role": sc.story_role,
                    "quality": round(min(0.99, quality), 2),
                    "detected_objects": sc.detected_objects,
                })
        else:
            # Fallback single segment if no scene transitions detected
            segments.append({
                "start": 0.0,
                "end": dur,
                "transcript": " ".join(s.text for s in speech_segs),
                "visual_summary": "Full Clip Sequence",
                "camera_movement": "Static Shot",
                "story_role": "general",
                "quality": 0.85,
            })

        elapsed = round(time.time() - t0, 3)

        return {
            "clip_id": clip_id,
            "filename": meta.filename,
            "filepath": video_path,
            "duration": dur,
            "width": meta.width,
            "height": meta.height,
            "fps": meta.fps,
            "has_audio": meta.has_audio,
            "segments": segments,
            "facts": facts,
            "analysis_time_sec": elapsed,
        }

