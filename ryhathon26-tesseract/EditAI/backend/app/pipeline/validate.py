# app/pipeline/validate.py

from typing import Any


def repair_edit_plan_segments(
    clips: list[dict[str, Any]],
    edit_plan: dict[str, Any]
) -> dict[str, Any]:
    """
    Auto-repairs minor LLM formatting variations:
    - Flattens nested arrays.
    - Parses string timestamps to float.
    - Infers decision='keep' if missing.
    - Filters hallucinated clip IDs if valid ones exist.
    """
    if not isinstance(edit_plan, dict):
        return edit_plan

    valid_clip_ids = {c.get("clip_id") for c in clips if isinstance(c, dict) and c.get("clip_id")}
    raw_segments = edit_plan.get("ordered_segments", [])
    if not isinstance(raw_segments, list):
        return edit_plan

    flat_segments = []
    def _flatten(items):
        for it in items:
            if isinstance(it, list):
                _flatten(it)
            elif isinstance(it, dict):
                flat_segments.append(it)

    _flatten(raw_segments)

    repaired = []
    for s in flat_segments:
        item = dict(s)
        # Infer keep if missing
        if "decision" not in item:
            item["decision"] = "keep"

        # Coerce timestamps
        for k in ("start", "end"):
            if k in item:
                try:
                    item[k] = float(item[k])
                except (ValueError, TypeError):
                    pass

        # Filter hallucinated clip IDs if possible
        cid = item.get("clip_id")
        if valid_clip_ids and cid not in valid_clip_ids:
            # Check for close prefix match (e.g. 'clip_1' vs 'clip_001')
            matched = False
            for vcid in valid_clip_ids:
                if str(cid).replace("_", "").lower() in str(vcid).replace("_", "").lower():
                    item["clip_id"] = vcid
                    matched = True
                    break
            if not matched:
                continue

        repaired.append(item)

    return {
        **edit_plan,
        "ordered_segments": repaired
    }


def validate_edit_plan(
    clips: list[dict[str, Any]],
    edit_plan: dict[str, Any],
    min_segment_duration: float = 0.15,
    tolerance: float = 0.05,
    auto_repair: bool = True,
) -> dict[str, Any]:
    """
    Validate source references and edit ranges.

    Returns:
      valid_segments: segments safe to consider for export
      review_items: questionable or rejected segments
      errors: structural errors
      warnings: non-fatal concerns
    """

    if auto_repair:
        edit_plan = repair_edit_plan_segments(clips, edit_plan)

    by_id = {clip["clip_id"]: clip for clip in clips}

    valid_segments = []
    review_items = list(edit_plan.get("review_items", []))
    errors = []
    warnings = []

    segments = edit_plan.get("ordered_segments")

    if not isinstance(segments, list):
        return {
            "valid": False,
            "valid_segments": [],
            "review_items": review_items,
            "errors": ["ordered_segments must be a list"],
            "warnings": warnings,
        }

    seen = set()

    for index, item in enumerate(segments):
        label = f"Segment {index}"

        if not isinstance(item, dict):
            errors.append(f"{label}: expected an object")
            continue

        if item.get("decision") != "keep":
            continue

        clip_id = item.get("clip_id")
        if clip_id not in by_id:
            errors.append(f"{label}: unknown clip_id {clip_id!r}")
            continue

        try:
            start = float(item["start"])
            end = float(item["end"])
            duration = float(by_id[clip_id]["duration"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{label}: invalid or missing time values")
            continue

        if start < 0:
            errors.append(f"{label}: negative start time")
            continue

        if end <= start:
            errors.append(f"{label}: end must be after start")
            continue

        if end - start < min_segment_duration:
            review_items.append({
                **item,
                "reason": "Segment is extremely short; review before export",
            })
            continue

        if end > duration + tolerance:
            errors.append(
                f"{label}: end {end} exceeds "
                f"{clip_id} duration {duration}"
            )
            continue

        # Clamp tiny floating-point overrun only.
        end = min(end, duration)

        key = (clip_id, round(start, 3), round(end, 3))
        if key in seen:
            warnings.append(f"{label}: duplicate source range skipped")
            continue

        seen.add(key)

        valid_segments.append({
            **item,
            "clip_id": clip_id,
            "start": start,
            "end": end,
        })

    if not valid_segments:
        errors.append("No valid segments remain for export")

    # Flag repeated source ranges and potential accidental overlap.
    # Intentional reuse may be valid, so these are warnings.
    by_source = {}

    for item in valid_segments:
        by_source.setdefault(item["clip_id"], []).append(item)

    for clip_id, source_segments in by_source.items():
        source_segments.sort(key=lambda x: x["start"])

        for previous, current in zip(
            source_segments, source_segments[1:]
        ):
            if current["start"] < previous["end"] - 0.01:
                warnings.append(
                    f"{clip_id}: selected source ranges overlap; "
                    "check whether reuse is intentional"
                )

    return {
        "valid": len(errors) == 0,
        "valid_segments": valid_segments,
        "review_items": review_items,
        "errors": errors,
        "warnings": warnings,
    }

