"""
変換APIルーター

単位変換のためのAPIエンドポイントを提供
"""

import math
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

from converters.length import convert_length, get_length_units_info
from converters.weight import convert_weight, get_weight_units_info
from converters.temperature import convert_temperature, get_temperature_units_info
from exceptions import (
    ValidationError,
    InvalidCategoryError,
    InvalidUnitError,
    CategoryNotFoundError
)

router = APIRouter(prefix="/api", tags=["convert"])


class ConvertRequest(BaseModel):
    """変換リクエストのモデル"""
    value: float = Field(..., description="変換する値")
    from_unit: str = Field(..., description="変換元の単位")
    to_unit: str = Field(..., description="変換先の単位")
    category: str = Field(..., description="変換カテゴリ (length, weight, temperature)")

    @field_validator('value')
    @classmethod
    def validate_value(cls, v: float) -> float:
        """値のバリデーション"""
        if math.isnan(v) or math.isinf(v):
            raise ValueError("Value must be a finite number")
        return v

    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        """カテゴリのバリデーション"""
        valid_categories = {'length', 'weight', 'temperature'}
        if v not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v

    @field_validator('from_unit', 'to_unit')
    @classmethod
    def validate_unit(cls, v: str) -> str:
        """単位のバリデーション（空文字チェック）"""
        if not v or not v.strip():
            raise ValueError("Unit cannot be empty")
        return v.strip()


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


class UnitInfo(BaseModel):
    """単位情報のモデル"""
    code: str = Field(..., description="単位コード")
    name: str = Field(..., description="単位の名称")


class UnitsResponse(BaseModel):
    """単位一覧レスポンスのモデル"""
    category: str = Field(..., description="カテゴリ名")
    units: list[UnitInfo] = Field(..., description="利用可能な単位のリスト")


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
            raise InvalidCategoryError(request.category)

        return ConvertResponse(
            success=True,
            result=result,
            from_unit=request.from_unit,
            to_unit=request.to_unit,
            original_value=request.value
        )

    except ValueError as e:
        # 変換関数からのValueErrorをカスタム例外に変換
        error_msg = str(e)
        if "Invalid unit:" in error_msg:
            # 単位名を抽出
            unit = error_msg.split("Invalid unit:")[-1].strip()
            raise InvalidUnitError(unit)
        else:
            raise ValidationError(error_msg)


@router.get("/units/{category}", response_model=UnitsResponse, responses={404: {"model": ErrorResponse}})
async def get_units(category: str):
    """
    カテゴリ別の利用可能な単位一覧を取得するAPIエンドポイント

    Args:
        category: 単位カテゴリ (length, weight, temperature)

    Returns:
        UnitsResponse: 単位一覧

    Raises:
        CategoryNotFoundError: 無効なカテゴリが指定された場合 (404)
    """
    if category == "length":
        units_info = get_length_units_info()
    elif category == "weight":
        units_info = get_weight_units_info()
    elif category == "temperature":
        units_info = get_temperature_units_info()
    else:
        raise CategoryNotFoundError(category)

    return UnitsResponse(
        category=category,
        units=[UnitInfo(**unit) for unit in units_info]
    )
