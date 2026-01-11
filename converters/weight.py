"""
重さの単位変換モジュール

対応単位: g, kg, mg, lb, oz
"""

# 各単位からグラムへの変換係数
UNITS_TO_GRAMS = {
    'g': 1.0,
    'kg': 1000.0,
    'mg': 0.001,
    'lb': 453.59237,
    'oz': 28.349523125
}


def get_weight_units() -> list[str]:
    """
    利用可能な重さの単位一覧を返す

    Returns:
        list[str]: 利用可能な単位のリスト
    """
    return list(UNITS_TO_GRAMS.keys())


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """
    重さの単位変換を行う

    Args:
        value: 変換する値
        from_unit: 変換元の単位
        to_unit: 変換先の単位

    Returns:
        float: 変換後の値

    Raises:
        ValueError: 無効な単位が指定された場合
    """
    if from_unit not in UNITS_TO_GRAMS:
        raise ValueError(f"Invalid unit: {from_unit}")

    if to_unit not in UNITS_TO_GRAMS:
        raise ValueError(f"Invalid unit: {to_unit}")

    # from_unitからグラムに変換
    grams = value * UNITS_TO_GRAMS[from_unit]

    # グラムからto_unitに変換
    result = grams / UNITS_TO_GRAMS[to_unit]

    return result
