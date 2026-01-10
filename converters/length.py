"""
長さの単位変換モジュール

対応単位: m, km, cm, mm, in, ft, yd, mi
"""

# 各単位からメートルへの変換係数
UNITS_TO_METERS = {
    'm': 1.0,
    'km': 1000.0,
    'cm': 0.01,
    'mm': 0.001,
    'in': 0.0254,
    'ft': 0.3048,
    'yd': 0.9144,
    'mi': 1609.344
}


def get_length_units() -> list[str]:
    """
    利用可能な長さの単位一覧を返す

    Returns:
        list[str]: 利用可能な単位のリスト
    """
    return list(UNITS_TO_METERS.keys())


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """
    長さの単位変換を行う

    Args:
        value: 変換する値
        from_unit: 変換元の単位
        to_unit: 変換先の単位

    Returns:
        float: 変換後の値

    Raises:
        ValueError: 無効な単位が指定された場合
    """
    if from_unit not in UNITS_TO_METERS:
        raise ValueError(f"Invalid unit: {from_unit}")

    if to_unit not in UNITS_TO_METERS:
        raise ValueError(f"Invalid unit: {to_unit}")

    # from_unitからメートルに変換
    meters = value * UNITS_TO_METERS[from_unit]

    # メートルからto_unitに変換
    result = meters / UNITS_TO_METERS[to_unit]

    return result
