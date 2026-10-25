from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    ApiResponse,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services import ProjectService


router = APIRouter()
experience_projects_router = APIRouter()


@router.get(
    "",
    response_model=ApiResponse[list[ProjectResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get all projects",
)
def get_projects(
    db: Session = Depends(get_db),
) -> ApiResponse[list[ProjectResponse]]:
    """Retrieve all projects, ordered by display order."""

    service = ProjectService(db)
    projects = service.get_all()

    return ApiResponse(
        success=True,
        message="Projects retrieved successfully.",
        data=[
            ProjectResponse.model_validate(project)
            for project in projects
        ],
    )


@router.get(
    "/{project_id}",
    response_model=ApiResponse[ProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Get project by ID",
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[ProjectResponse]:
    """Retrieve a project by its ID."""

    service = ProjectService(db)
    project = service.get_by_id(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return ApiResponse(
        success=True,
        message="Project retrieved successfully.",
        data=ProjectResponse.model_validate(project),
    )


@experience_projects_router.get(
    "/{experience_id}/projects",
    response_model=ApiResponse[list[ProjectResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get projects associated with an experience",
)
def get_experience_projects(
    experience_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[list[ProjectResponse]]:
    """Retrieve projects belonging to a specific experience."""

    service = ProjectService(db)

    try:
        projects = service.get_by_experience_id(experience_id)
    except ValueError as exc:
        if str(exc) == "Experience not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Experience projects retrieved successfully.",
        data=[
            ProjectResponse.model_validate(project)
            for project in projects
        ],
    )


@router.post(
    "",
    response_model=ApiResponse[ProjectResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create project",
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[ProjectResponse]:
    """Create a project associated with an existing experience."""

    service = ProjectService(db)

    try:
        project = service.create(project_data)
    except ValueError as exc:
        if str(exc) == "Experience not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Project created successfully.",
        data=ProjectResponse.model_validate(project),
    )


@router.put(
    "/{project_id}",
    response_model=ApiResponse[ProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Update project",
)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[ProjectResponse]:
    """Update an existing project."""

    service = ProjectService(db)

    try:
        project = service.update(project_id, project_data)
    except ValueError as exc:
        message = str(exc)

        if message == "Project not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        if message == "Experience not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Project updated successfully.",
        data=ProjectResponse.model_validate(project),
    )


@router.delete(
    "/{project_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete project",
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """Delete an existing project."""

    service = ProjectService(db)

    try:
        service.delete(project_id)
    except ValueError as exc:
        if str(exc) == "Project not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Project deleted successfully.",
        data=None,
    )
