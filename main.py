"""
metrix - Unit Conversion Web Application
FastAPI application entry point
"""

import logging
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError

from routers import convert
from exceptions import MetrixException

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="metrix",
    description="Simple unit conversion web application",
    version="0.1.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では特定のオリジンのみ許可すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# リクエスト・レスポンスのログ出力ミドルウェア
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """リクエストとレスポンスをログ出力"""
    start_time = time.time()

    # リクエストログ
    logger.info(f"Request: {request.method} {request.url.path}")

    # レスポンス処理
    response = await call_next(request)

    # レスポンスログ
    process_time = time.time() - start_time
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {process_time:.3f}s"
    )

    return response


# カスタム例外ハンドラー
@app.exception_handler(MetrixException)
async def metrix_exception_handler(request: Request, exc: MetrixException):
    """カスタム例外のハンドラー"""
    logger.error(f"MetrixException: {exc.message} (status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.message}
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """FastAPIリクエストバリデーションエラーのハンドラー"""
    errors = exc.errors()
    error_messages = []
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")

    error_detail = "; ".join(error_messages)
    logger.error(f"Validation error: {error_detail}")

    return JSONResponse(
        status_code=400,
        content={"success": False, "error": error_detail}
    )


@app.exception_handler(PydanticValidationError)
async def validation_exception_handler(request: Request, exc: PydanticValidationError):
    """Pydanticバリデーションエラーのハンドラー"""
    errors = exc.errors()
    error_messages = []
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")

    error_detail = "; ".join(error_messages)
    logger.error(f"Validation error: {error_detail}")

    return JSONResponse(
        status_code=400,
        content={"success": False, "error": error_detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """一般的な例外のハンドラー"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )


# Include routers
app.include_router(convert.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Render the main UI page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
