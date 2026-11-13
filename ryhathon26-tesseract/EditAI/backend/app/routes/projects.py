from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.database.db import ProjectDB

router = APIRouter(prefix="/api/projects", tags=["Projects"])

class CreateProjectRequest(BaseModel):
    name: str = "New Project"
    settings: Optional[Dict[str, Any]] = None

class SaveProjectRequest(BaseModel):
    name: str
    settings: Optional[Dict[str, Any]] = {}
    clips: Optional[List[Dict[str, Any]]] = None
    subtitles: Optional[List[Dict[str, Any]]] = None
    timeline: Optional[Dict[str, Any]] = None
    brief: Optional[str] = None

@router.get("")
async def list_all_projects():
    """Lists all saved projects with timestamps."""
    return ProjectDB.list_projects()

@router.post("")
async def create_new_project(req: CreateProjectRequest):
    """Creates a new project record."""
    return ProjectDB.create_project(name=req.name, settings=req.settings)

@router.get("/{project_id}")
async def get_project_state(project_id: str):
    """Loads complete project state including timeline clips, subtitles, and history."""
    proj = ProjectDB.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj

@router.post("/{project_id}/save")
async def save_project_state(project_id: str, req: SaveProjectRequest):
    """Persists project changes, clips, and subtitles to SQLite."""
    clips = req.clips if req.clips is not None else (req.timeline.get("clips", []) if req.timeline else [])
    subtitles = req.subtitles if req.subtitles is not None else (req.timeline.get("subtitles", []) if req.timeline else [])
    settings = req.settings or {}
    if req.brief and "brief" not in settings:
        settings["brief"] = req.brief

    ProjectDB.save_project(
        proj_id=project_id,
        name=req.name,
        settings=settings,
        clips=clips,
        subtitles=subtitles
    )
    return {"success": True, "message": f"Project '{req.name}' saved successfully."}

@router.post("/{project_id}/autosave")
async def autosave_project(project_id: str, req: SaveProjectRequest):
    """Performs background autosave."""
    clips = req.clips if req.clips is not None else (req.timeline.get("clips", []) if req.timeline else [])
    subtitles = req.subtitles if req.subtitles is not None else (req.timeline.get("subtitles", []) if req.timeline else [])
    settings = req.settings or {}
    if req.brief and "brief" not in settings:
        settings["brief"] = req.brief

    ProjectDB.save_project(
        proj_id=project_id,
        name=req.name,
        settings=settings,
        clips=clips,
        subtitles=subtitles
    )
    return {"success": True, "autosaved": True}


class RecordSuggestionRequest(BaseModel):
    brief: str
    story_summary: str
    edit_plan: Dict[str, Any]
    status: Optional[str] = "suggested"

class UpdateSuggestionStatusRequest(BaseModel):
    status: str  # 'approved' or 'rejected'

@router.get("/{project_id}/suggestions")
async def get_project_suggestions(project_id: str):
    """Retrieves all previous AI suggestions and editorial memory for this project."""
    return ProjectDB.get_suggestions(project_id)

@router.post("/{project_id}/suggestions")
async def record_project_suggestion(project_id: str, req: RecordSuggestionRequest):
    """Records an AI suggestion into persistent project memory."""
    sug_id = ProjectDB.record_suggestion(
        project_id=project_id,
        brief=req.brief,
        story_summary=req.story_summary,
        edit_plan=req.edit_plan,
        status=req.status or "suggested"
    )
    return {"success": True, "suggestion_id": sug_id}

@router.patch("/{project_id}/suggestions/{suggestion_id}")
async def update_suggestion_status(project_id: str, suggestion_id: str, req: UpdateSuggestionStatusRequest):
    """Marks an AI suggestion as approved or rejected for project memory."""
    ProjectDB.update_suggestion_status(suggestion_id, req.status)
    return {"success": True, "suggestion_id": suggestion_id, "status": req.status}
