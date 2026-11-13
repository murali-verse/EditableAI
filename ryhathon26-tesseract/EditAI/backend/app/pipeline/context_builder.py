# app/pipeline/context_builder.py
import json
from typing import Any, List, Dict
from collections import defaultdict

from app.services.semantic_service import SemanticService

def build_story_context(
    brief: str,
    clips: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Combine analyses from multiple clips into one unified story context.
    Executes semantic similarity clustering and repeated take detection.
    """
    all_segments = []
    clip_summaries = []
    role_groups = defaultdict(list)

    for clip in clips:
        clip_id = clip["clip_id"]
        duration = float(clip["duration"])

        clip_summaries.append({
            "clip_id": clip_id,
            "duration": duration,
            "filename": clip.get("filename", ""),
            "summary": clip.get("summary", ""),
            "segments": clip.get("segments", []),
        })

        for index, segment in enumerate(clip.get("segments", [])):
            start = float(segment["start"])
            end = float(segment["end"])

            item = {
                "segment_id": f"{clip_id}_seg_{index:04d}",
                "clip_id": clip_id,
                "start": start,
                "end": end,
                "transcript": segment.get("transcript", ""),
                "visual_summary": segment.get("visual_summary", ""),
                "story_role": segment.get("story_role", "broll"),
                "quality": segment.get("quality", 0.85),
                "camera_movement": segment.get("camera_movement", "Static"),
            }

            all_segments.append(item)
            role_groups[item["story_role"]].append(item["segment_id"])

    all_segments.sort(key=lambda s: (s["clip_id"], s["start"]))

    # Detect cross-clip repeated statements using SemanticService
    repetition_candidates = SemanticService.detect_repeated_statements(all_segments, threshold=0.72)

    # Aggregate extracted key facts across clips
    cross_clip_facts = []
    for clip in clips:
        for f in clip.get("facts", []):
            if f not in cross_clip_facts:
                cross_clip_facts.append(f)

    return {
        "cross_clip_facts": cross_clip_facts,
        "brief": brief,
        "clip_count": len(clip_summaries),
        "clips": clip_summaries,
        "segments": all_segments,
        "segments_by_story_role": dict(role_groups),
        "repetition_candidates": repetition_candidates[:10],
        "editorial_instructions": [
            "Treat all clips as one unified story.",
            "Do not assume upload order is story order.",
            "Compare statements across every source clip.",
            "Keep the clearest complete version of repeated information.",
            "Preserve unique facts, qualifications, and useful context.",
            "Use B-roll when it supports the spoken narrative.",
            "Keep uncertain removals in a review list.",
            "Return exact source clip IDs and source timestamps.",
        ],
    }


def build_planner_prompt(
    context: dict[str, Any],
) -> str:
    """
    Create the input prompt for Qwen 2.5 with hierarchical reasoning instructions.
    """
    rep_notes = ""
    reps = context.get("repetition_candidates", [])
    if reps:
        rep_notes = "\nCROSS-CLIP REPETITION CANDIDATES DETECTED FOR EVALUATION:\n"
        for idx, r in enumerate(reps[:5], 1):
            a = r["segment_a"]
            b = r["segment_b"]
            rep_notes += (
                f"- Pair {idx} (Similarity: {r['similarity']:.2f}):\n"
                f"  Take A [{a['clip_id']} {a['start']}s-{a['end']}s]: \"{a['text']}\"\n"
                f"  Take B [{b['clip_id']} {b['start']}s-{b['end']}s]: \"{b['text']}\"\n"
                f"  Instruction: Decide whether Take B is a redundant flub/repeat, or contains unique distinct facts.\n"
            )

    return f"""
You are an expert editorial planning assistant for video production.

Create one coherent, logically structured video edit from multiple source clips.

CLIENT BRIEF & EDITORIAL GOAL:
{context["brief"]}
{rep_notes}
CLIP AND MULTIMODAL SEGMENT POOL:
{json.dumps(context, ensure_ascii=False, indent=2)}

HIERARCHICAL REASONING RULES:
1. Understand all clips together before selecting segments.
2. Choose a logical story order (Hook -> Setup -> Dynamic Cutaway -> Core Value Message -> Climax / Outro), NOT upload order.
3. Compare candidate takes across clips. If statements repeat, keep the most articulate take.
4. NEVER remove unique information merely because wording sounds similar.
5. Preserve enough context for every statement to remain clear and coherent.
6. Pair spoken dialogue with visual B-roll cuts where appropriate.
7. CRITICAL: Do NOT invent timestamps, clip IDs, or events. Use ONLY real clip_id and timestamps from the pool.
8. Keep questionable or rejected takes in review_items so the editor can inspect them.
9. Return strict JSON only matching this schema:

{{
  "story_summary": "Concise overview of the synthesized video story arc.",
  "ordered_segments": [
    {{
      "clip_id": "clip_001",
      "start": 0.0,
      "end": 5.0,
      "decision": "keep",
      "reason": "Editorial justification for keeping this cut in the timeline.",
      "story_role": "introduction"
    }}
  ],
  "review_items": [
    {{
      "clip_id": "clip_002",
      "start": 10.0,
      "end": 14.0,
      "reason": "Repeated statement from clip_001; kept in review pool for editor confirmation."
    }}
  ]
}}
""".strip()
