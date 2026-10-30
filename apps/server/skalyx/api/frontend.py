from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

frontend_router = APIRouter(include_in_schema=False)

DIST_DIR = Path("assets/builded-frontend").resolve()

@frontend_router.get("/assets/{file_path:path}")
async def serve_assets(file_path: str):
    file_location = DIST_DIR / "assets" / file_path

    if not file_location.is_file():
        return HTMLResponse("Asset not found", status_code=404)

    return FileResponse(
        file_location,
        headers={
            "Cache-Control": "public, max-age=31536000, immutable"
        }
    )

@frontend_router.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_location = DIST_DIR / full_path
    if file_location.is_file():
        return FileResponse(file_location)

    index_path = DIST_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path, headers={"Cache-Control": "no-cache"})

    return HTMLResponse(
        "Frontend build not found. Please run 'npm run build' inside the frontend directory.",
        status_code=404
    )
