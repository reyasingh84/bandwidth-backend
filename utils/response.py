from typing import Any

from fastapi.responses import JSONResponse


def api_response(
    *,
    success: bool,
    message: str | None = None,
    response: Any = None,
    status_code: int = 200,
) -> JSONResponse:
    return JSONResponse(
        {
            "error": None if success else True,
            "success": True if success else None,
            "message": message,
            "response": response,
        },
        status_code=status_code,
    )
