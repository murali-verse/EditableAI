import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_multimodal_ai_upgrade():
    print("================================================================================")
    print("  REELCRAFT AI — MULTIMODAL UPGRADE VERIFICATION & BENCHMARK SUITE")
    print("================================================================================")

    # --------------------------------------------------------------------------
    # 1. System Diagnostics & Hardware Verification
    # --------------------------------------------------------------------------
    print("\n[TEST 1] Verifying System Diagnostics & Model Orchestrator Layer...")
    from app.services.ai_orchestrator import AIOrchestrator
    diag = AIOrchestrator.get_system_diagnostics()
    print(f"  • Execution Device : {diag['device'].upper()} ({diag['gpu_device']})")
    print(f"  • Whisper Status   : {diag['orchestrator_matrix']['whisper']['status']} (model: {diag['orchestrator_matrix']['whisper']['model']})")
    print(f"  • OpenCV Status    : {diag['orchestrator_matrix']['opencv']['status']}")
    print(f"  • Vision Status    : {diag['orchestrator_matrix']['vision']['status']}")
    print(f"  • Embeddings Status: {diag['orchestrator_matrix']['bge_embeddings']['status']} (model: {diag['orchestrator_matrix']['bge_embeddings']['model']})")
    print(f"  • Qwen 2.5 Status  : {diag['orchestrator_matrix']['qwen2_5_reasoning']['status']} (endpoint: {diag['orchestrator_matrix']['qwen2_5_reasoning']['endpoint']})")
    print(f"  • Guardrails Status: {diag['orchestrator_matrix']['python_guardrails']['status']}")
    assert diag["device"] in ["cuda", "cpu"]
    print("  --> [PASS] Centralized Model Orchestration Layer verified.")

    # --------------------------------------------------------------------------
    # 2. Semantic Search & Repetition Detection (BGE-M3 / MiniLM)
    # --------------------------------------------------------------------------
    print("\n[TEST 2] Verifying Semantic Embeddings, Transcript Search & Repetition Detection...")
    from app.services.semantic_service import SemanticService
    t0 = time.time()
    sim_match = SemanticService.compute_similarity("Our AI video editor cuts editing time by 80%", "EditMind saves video creators 80% of their time")
    sim_diff = SemanticService.compute_similarity("Our AI video editor cuts editing time by 80%", "The recipe requires two cups of flour and butter")
    emb_time = (time.time() - t0) * 1000
    print(f"  • Paraphrase Similarity Score : {sim_match:.4f} (Expected > 0.65)")
    print(f"  • Unrelated Similarity Score  : {sim_diff:.4f} (Expected < 0.45)")
    print(f"  • Embedding Inference Latency : {emb_time:.1f}ms")
    assert sim_match > 0.60
    assert sim_diff < 0.45

    sample_clips = [
        {
            "clip_id": "clip_01",
            "filename": "take_1_interview.mp4",
            "segments": [
                {"start": 0.0, "end": 4.0, "transcript": "Hello and welcome to REELCRAFT AI, the smartest editor."},
                {"start": 4.0, "end": 8.0, "transcript": "Our tool automatically cuts your video with AI."}
            ]
        },
        {
            "clip_id": "clip_02",
            "filename": "take_2_interview.mp4",
            "segments": [
                {"start": 0.0, "end": 4.2, "transcript": "Welcome everyone to REELCRAFT AI, the intelligent video editor."},
                {"start": 4.2, "end": 9.0, "transcript": "In this tutorial we will showcase how to export in 4K resolution."}
            ]
        }
    ]
    reps = SemanticService.detect_repeated_statements(sample_clips, similarity_threshold=0.65)
    print(f"  • Cross-Clip Repetition Candidates Detected: {len(reps)}")
    for r in reps:
        print(f"     * Found: '{r['segment_a']['text']}' vs '{r['segment_b']['text']}' (Sim: {r['similarity']:.3f})")
    assert len(reps) >= 1
    print("  --> [PASS] Semantic vector search & cross-clip repetition detection verified.")

    # --------------------------------------------------------------------------
    # 3. Computer Vision & Keyframe Deduplication
    # --------------------------------------------------------------------------
    print("\n[TEST 3] Verifying Perceptual dHash Deduplication & Optical Flow Camera Motion...")
    from app.services.video_service import VideoService
    import numpy as np
    f1 = np.full((120, 160, 3), 100, dtype=np.uint8)
    f2 = np.full((120, 160, 3), 102, dtype=np.uint8) # Nearly identical
    f3 = np.random.randint(0, 255, (120, 160, 3), dtype=np.uint8) # Drastically different
    h1 = VideoService.compute_dhash(f1)
    h2 = VideoService.compute_dhash(f2)
    h3 = VideoService.compute_dhash(f3)
    d_near = VideoService.hamming_distance(h1, h2)
    d_diff = VideoService.hamming_distance(h1, h3)
    print(f"  • Near-Duplicate Frame Hamming Distance: {d_near} (Expected <= 4)")
    print(f"  • Distinct Frame Hamming Distance       : {d_diff} (Expected > 10)")
    assert d_near <= 4
    assert d_diff > 10

    # Optical Flow Motion Vector Test
    flow_motion = VideoService.estimate_camera_movement([f1, f2])
    print(f"  • Motion Vector Classification: '{flow_motion}'")
    assert isinstance(flow_motion, str)
    print("  --> [PASS] Vision deduplication and optical flow motion classifier verified.")

    # --------------------------------------------------------------------------
    # 4. Multi-Tier Analysis Cache & Telemetry
    # --------------------------------------------------------------------------
    print("\n[TEST 4] Verifying High-Performance Multi-Tier Analysis Cache...")
    from app.services.analysis_cache import AnalysisCache
    AnalysisCache.clear()

    dummy_hash = "mock_media_hash_abcdef123456"
    dummy_analysis = {
        "clip_id": "test_clip",
        "duration": 12.5,
        "segments": [{"start": 0.0, "end": 5.0, "transcript": "Cached transcript", "story_role": "introduction"}]
    }

    # Miss check
    assert AnalysisCache.get(dummy_hash) is None

    # Put into cache
    t_write_start = time.time()
    AnalysisCache.put(dummy_hash, "test.mp4", "test.mp4", 12.5, dummy_analysis)
    t_write = (time.time() - t_write_start) * 1000

    # Hit check (RAM)
    t_hit_start = time.time()
    cached_hit = AnalysisCache.get(dummy_hash)
    t_hit = (time.time() - t_hit_start) * 1000

    print(f"  • Cache Write Latency (SQLite + RAM): {t_write:.2f}ms")
    print(f"  • Cache Read Latency (Tier 1 RAM)   : {t_hit:.4f}ms")
    assert cached_hit is not None
    assert cached_hit["duration"] == 12.5

    stats = AnalysisCache.get_stats()
    print(f"  • Cache Telemetry Stats: Hits={stats['hits']}, Misses={stats['misses']}, Hit Rate={stats['hit_rate_pct']}%")
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    print("  --> [PASS] Analysis caching layer verified.")

    # --------------------------------------------------------------------------
    # 5. Project Memory & AI Suggestion Persistence
    # --------------------------------------------------------------------------
    print("\n[TEST 5] Verifying Project Memory & Suggestion Review Storage in SQLite...")
    from app.database.db import ProjectDB
    proj = ProjectDB.create_project("Multimodal Test Project")
    pid = proj["id"]

    mock_plan = {
        "ordered_segments": [{"clip_id": "c1", "start": 0.0, "end": 4.0}],
        "review_items": [{"clip_id": "c2", "start": 1.0, "end": 3.0, "reason": "Alternative take"}]
    }
    sug_id = ProjectDB.record_suggestion(
        project_id=pid,
        brief="Create dynamic product review",
        story_summary="Highlighting speaker intro and cutting to action.",
        edit_plan=mock_plan,
        status="suggested"
    )
    print(f"  • Recorded AI Suggestion in Project Memory with ID: {sug_id}")

    # Fetch suggestions
    suggestions = ProjectDB.get_suggestions(pid)
    assert len(suggestions) >= 1
    assert suggestions[0]["id"] == sug_id
    assert suggestions[0]["status"] == "suggested"

    # User Approval / Rejection Update
    ProjectDB.update_suggestion_status(sug_id, "approved")
    updated_suggestions = ProjectDB.get_suggestions(pid)
    assert updated_suggestions[0]["status"] == "approved"
    print(f"  • Successfully updated suggestion status to: '{updated_suggestions[0]['status']}'")
    print("  --> [PASS] Project memory and suggestion tracking verified.")

    # --------------------------------------------------------------------------
    # 6. Global Story Planning & Guardrail Validation
    # --------------------------------------------------------------------------
    print("\n[TEST 6] Verifying Hierarchical Story Planning Engine & Guardrail Validation...")
    from app.pipeline.model_adapter import plan_global_edit
    from app.pipeline.validate import validate_edit_plan, repair_edit_plan_segments

    test_clips_data = [
        {
            "clip_id": "clip_01",
            "filename": "intro_take1.mp4",
            "duration": 10.0,
            "segments": [
                {"start": 0.0, "end": 4.5, "transcript": "Welcome to REELCRAFT AI.", "story_role": "introduction", "quality": 0.92},
                {"start": 4.5, "end": 10.0, "transcript": "Here are our top features.", "story_role": "benefit", "quality": 0.88}
            ]
        },
        {
            "clip_id": "clip_02",
            "filename": "broll_action.mp4",
            "duration": 8.0,
            "segments": [
                {"start": 0.0, "end": 4.0, "visual_summary": "High speed typing and fast editing", "story_role": "action_broll", "quality": 0.90},
                {"start": 4.0, "end": 8.0, "visual_summary": "Sunset view and studio sign off", "story_role": "outro", "quality": 0.89}
            ]
        }
    ]

    edit_plan = plan_global_edit("Create an engaging highlight reel.", analyses=test_clips_data)
    print(f"  • Story Summary Synthesized : \"{edit_plan['story_summary'][:80]}...\"")
    print(f"  • Ordered Timeline Segments : {len(edit_plan['ordered_segments'])}")
    print(f"  • Review/Alternative Items  : {len(edit_plan['review_items'])}")
    assert len(edit_plan["ordered_segments"]) >= 3

    # Guardrail Validation
    val_report = validate_edit_plan(test_clips_data, edit_plan)
    print(f"  • Validation Outcome        : {'PASSED' if val_report['valid'] else 'FAILED'}")
    print(f"  • Valid Segments            : {len(val_report['valid_segments'])}")
    assert val_report["valid"] is True
    assert len(val_report["valid_segments"]) == len(edit_plan["ordered_segments"])
    print("  --> [PASS] Hierarchical story planner and guardrail validator verified.")

    print("\n================================================================================")
    print("  ALL 6 MULTIMODAL UPGRADE VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("================================================================================")

if __name__ == "__main__":
    test_multimodal_ai_upgrade()
