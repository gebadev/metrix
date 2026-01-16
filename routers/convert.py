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


class BatchConvertRequest(BaseModel):
    """一括変換リクエストのモデル"""
    value: float = Field(..., description="変換する値")
    from_unit: str = Field(..., description="変換元の単位")
    category: str = Field(..., description="変換カテゴリ (length, weight, temperature)")
    to_units: list[str] | None = Field(None, description="変換先の単位リスト（省略時はfrom_unitを除く全単位）")

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

    @field_validator('from_unit')
    @classmethod
    def validate_from_unit(cls, v: str) -> str:
        """from_unitのバリデーション（空文字チェック）"""
        if not v or not v.strip():
            raise ValueError("from_unit cannot be empty")
        return v.strip()

    @field_validator('to_units')
    @classmethod
    def validate_to_units(cls, v: list[str] | None) -> list[str] | None:
        """to_unitsのバリデーション"""
        if v is not None:
            if len(v) == 0:
                raise ValueError("to_units cannot be an empty list")
            # 空文字チェック
            for unit in v:
                if not unit or not unit.strip():
                    raise ValueError("to_units cannot contain empty strings")
        return v


class ConversionResult(BaseModel):
    """個別の変換結果"""
    to_unit: str = Field(..., description="変換先の単位")
    value: float = Field(..., description="変換後の値")


class BatchConvertResponse(BaseModel):
    """一括変換レスポンスのモデル"""
    success: bool = Field(default=True, description="変換が成功したかどうか")
    original_value: float = Field(..., description="変換前の値")
    from_unit: str = Field(..., description="変換元の単位")
    category: str = Field(..., description="変換カテゴリ")
    results: list[ConversionResult] = Field(..., description="変換結果のリスト")
    failed_units: list[str] = Field(default_factory=list, description="変換に失敗した単位のリスト")


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


def _get_unit_size_order(category: str, unit: str) -> float:
    """
    単位の大きさを取得（ソート用）

    Args:
        category: カテゴリ
        unit: 単位コード

    Returns:
        float: 単位の大きさ（基準単位に対する比率）
    """
    from converters.length import UNITS_TO_METERS
    from converters.weight import UNITS_TO_GRAMS

    if category == "length":
        return UNITS_TO_METERS.get(unit, 0)
    elif category == "weight":
        return UNITS_TO_GRAMS.get(unit, 0)
    elif category == "temperature":
        # 温度は変換係数がないため、定義順
        temp_order = {'kelvin': 3, 'celsius': 2, 'fahrenheit': 1}
        return temp_order.get(unit, 0)
    return 0


@router.post("/convert/batch", response_model=BatchConvertResponse, responses={400: {"model": ErrorResponse}})
async def batch_convert_unit(request: BatchConvertRequest):
    """
    一括単位変換を実行するAPIエンドポイント

    Args:
        request: 一括変換リクエスト

    Returns:
        BatchConvertResponse: 変換結果

    Raises:
        HTTPException: 無効なカテゴリまたは単位が指定された場合
    """
    try:
        # カテゴリに応じて適切な変換関数と単位一覧を取得
        if request.category == "length":
            convert_func = convert_length
            from converters.length import get_length_units
            all_units = get_length_units()
        elif request.category == "weight":
            convert_func = convert_weight
            from converters.weight import get_weight_units
            all_units = get_weight_units()
        elif request.category == "temperature":
            convert_func = convert_temperature
            from converters.temperature import get_temperature_units
            all_units = get_temperature_units()
        else:
            raise InvalidCategoryError(request.category)

        # from_unitの検証
        if request.from_unit not in all_units:
            raise InvalidUnitError(request.from_unit)

        # 変換先単位リストの決定
        if request.to_units is None:
            # to_unitsが省略された場合、from_unitを除く全単位
            target_units = [unit for unit in all_units if unit != request.from_unit]
        else:
            target_units = request.to_units

        # 各単位への変換を実行
        results = []
        failed_units = []

        for to_unit in target_units:
            try:
                converted_value = convert_func(request.value, request.from_unit, to_unit)
                results.append(ConversionResult(to_unit=to_unit, value=converted_value))
            except ValueError:
                # 変換に失敗した単位を記録
                failed_units.append(to_unit)

        # 結果を単位の大きさ順にソート（降順）
        results.sort(key=lambda r: _get_unit_size_order(request.category, r.to_unit), reverse=True)

        return BatchConvertResponse(
            success=True,
            original_value=request.value,
            from_unit=request.from_unit,
            category=request.category,
            results=results,
            failed_units=failed_units
        )

    except ValueError as e:
        # 変換関数からのValueErrorをカスタム例外に変換
        error_msg = str(e)
        if "Invalid unit:" in error_msg:
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
