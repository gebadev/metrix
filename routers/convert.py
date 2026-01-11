"""
変換APIルーター

単位変換のためのAPIエンドポイントを提供
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from converters.length import convert_length
from converters.weight import convert_weight
from converters.temperature import convert_temperature

router = APIRouter(prefix="/api", tags=["convert"])


class ConvertRequest(BaseModel):
    """変換リクエストのモデル"""
    value: float = Field(..., description="変換する値")
    from_unit: str = Field(..., description="変換元の単位")
    to_unit: str = Field(..., description="変換先の単位")
    category: str = Field(..., description="変換カテゴリ (length, weight, temperature)")


class ConvertResponse(BaseModel):
    """変換レスポンスのモデル (成功時)"""
    success: bool = Field(default=True, description="変換が成功したかどうか")
    result: float = Field(..., description="変換後の値")
    from_unit: str = Field(..., description="変換元の単位")
    to_unit: str = Field(..., description="変換先の単位")
    original_value: float = Field(..., description="変換前の値")


class ErrorResponse(BaseModel):
    """エラーレスポンスのモデル"""
    success: bool = Field(default=False, description="変換が成功したかどうか")
    error: str = Field(..., description="エラーメッセージ")


@router.post("/convert", response_model=ConvertResponse, responses={400: {"model": ErrorResponse}})
async def convert_unit(request: ConvertRequest):
    """
    単位変換を実行するAPIエンドポイント

    Args:
        request: 変換リクエスト

    Returns:
        ConvertResponse: 変換結果

    Raises:
        HTTPException: 無効なカテゴリまたは単位が指定された場合
    """
    try:
        # カテゴリに応じて適切な変換関数を呼び出す
        if request.category == "length":
            result = convert_length(request.value, request.from_unit, request.to_unit)
        elif request.category == "weight":
            result = convert_weight(request.value, request.from_unit, request.to_unit)
        elif request.category == "temperature":
            result = convert_temperature(request.value, request.from_unit, request.to_unit)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category: {request.category}"
            )

        return ConvertResponse(
            success=True,
            result=result,
            from_unit=request.from_unit,
            to_unit=request.to_unit,
            original_value=request.value
        )

    except ValueError as e:
        # 変換関数からのValueErrorをHTTP 400エラーに変換
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
