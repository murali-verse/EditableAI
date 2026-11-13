import os
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, Any, Optional

from app.database.db import get_connection

class AnalysisCache:
    """
    High-Performance Multi-Tier Caching Layer for REELCRAFT AI.
    - Tier 1: In-memory LRU dict for sub-millisecond retrieval
    - Tier 2: Persistent SQLite cache storing parsed JSON, transcripts & scene metadata
    - Fast Fingerprinting: Chunked SHA-256 hashing to verify media identity without I/O bottlenecks.
    """
    _memory_cache: Dict[str, Dict[str, Any]] = {}
    _max_memory_items: int = 256
    _hits: int = 0
    _misses: int = 0

    @classmethod
    def compute_file_hash(cls, filepath: str) -> str:
        """
        Computes a fast, collision-resistant SHA-256 fingerprint for media files.
        For large files (> 8MB), reads initial, middle, and tail chunks plus file size.
        """
        p = Path(filepath)
        if not p.is_file():
            return hashlib.sha256(filepath.encode("utf-8")).hexdigest()

        file_size = p.stat().st_size
        h = hashlib.sha256()
        h.update(f"size:{file_size}:name:{p.name}:".encode("utf-8"))

        chunk_size = 2 * 1024 * 1024  # 2MB
        with open(p, "rb") as f:
            if file_size <= chunk_size * 3:
                # Small to medium file: hash completely
                while chunk := f.read(1024 * 1024):
                    h.update(chunk)
            else:
                # Large video file: sample head, midpoint, and tail
                # 1. Head chunk
                h.update(f.read(chunk_size))
                # 2. Midpoint chunk
                f.seek(file_size // 2)
                h.update(f.read(chunk_size))
                # 3. Tail chunk
                f.seek(max(0, file_size - chunk_size))
                h.update(f.read(chunk_size))

        return h.hexdigest()

    @classmethod
    def get(cls, file_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieves cached analysis from Tier 1 (RAM) or Tier 2 (SQLite)."""
        # Tier 1: In-Memory Cache
        if file_hash in cls._memory_cache:
            cls._hits += 1
            return cls._memory_cache[file_hash]

        # Tier 2: SQLite Persistent Cache
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT analysis_json FROM media_analysis_cache WHERE file_hash = ?",
                (file_hash,)
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                data = json.loads(row["analysis_json"])
                # Promote to Tier 1
                cls._put_memory(file_hash, data)
                cls._hits += 1
                return data
        except Exception:
            pass

        cls._misses += 1
        return None

    @classmethod
    def put(
        cls,
        file_hash: str,
        filepath: str,
        filename: str,
        duration: float,
        analysis_data: Dict[str, Any]
    ) -> None:
        """Stores analysis in both Tier 1 (RAM) and Tier 2 (SQLite)."""
        cls._put_memory(file_hash, analysis_data)

        # Persist to SQLite
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO media_analysis_cache (
                file_hash, filepath, filename, duration, analysis_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                file_hash,
                str(filepath),
                filename,
                duration,
                json.dumps(analysis_data, ensure_ascii=False)
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[AnalysisCache] SQLite write warning: {e}")

    @classmethod
    def _put_memory(cls, file_hash: str, data: Dict[str, Any]) -> None:
        if len(cls._memory_cache) >= cls._max_memory_items:
            # Simple FIFO eviction
            oldest_key = next(iter(cls._memory_cache))
            del cls._memory_cache[oldest_key]
        cls._memory_cache[file_hash] = data

    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """Returns cache telemetry and hit rate metrics."""
        total = cls._hits + cls._misses
        hit_rate = (cls._hits / total * 100.0) if total > 0 else 0.0
        return {
            "hits": cls._hits,
            "misses": cls._misses,
            "total_requests": total,
            "hit_rate_pct": round(hit_rate, 2),
            "memory_cache_entries": len(cls._memory_cache),
        }

    @classmethod
    def clear(cls) -> None:
        cls._memory_cache.clear()
        cls._hits = 0
        cls._misses = 0

