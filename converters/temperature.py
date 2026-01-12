"""
温度の単位変換モジュール

対応単位: celsius (°C), fahrenheit (°F), kelvin (K)
"""

# 対応する温度単位
TEMPERATURE_UNITS = ['celsius', 'fahrenheit', 'kelvin']

# 単位の日本語名称
UNIT_NAMES = {
    'celsius': '摂氏（℃）',
    'fahrenheit': '華氏（℉）',
    'kelvin': 'ケルビン（K）'
}


def get_temperature_units() -> list[str]:
    """
    利用可能な温度の単位一覧を返す

    Returns:
        list[str]: 利用可能な単位のリスト
    """
    return TEMPERATURE_UNITS.copy()


def get_temperature_units_info() -> list[dict[str, str]]:
    """
    利用可能な温度の単位情報（コードと名称）を返す

    Returns:
        list[dict[str, str]]: 単位情報のリスト [{"code": "celsius", "name": "摂氏（℃）"}, ...]
    """
    return [
        {"code": code, "name": UNIT_NAMES[code]}
        for code in TEMPERATURE_UNITS
    ]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    温度の単位変換を行う

    Args:
        value: 変換する値
        from_unit: 変換元の単位 (celsius, fahrenheit, kelvin)
        to_unit: 変換先の単位 (celsius, fahrenheit, kelvin)

    Returns:
        float: 変換後の値

    Raises:
        ValueError: 無効な単位が指定された場合
    """
    if from_unit not in TEMPERATURE_UNITS:
        raise ValueError(f"Invalid unit: {from_unit}")

    if to_unit not in TEMPERATURE_UNITS:
        raise ValueError(f"Invalid unit: {to_unit}")

    # 同じ単位の場合はそのまま返す
    if from_unit == to_unit:
        return value

    # まずすべてをセルシウスに変換
    celsius = _to_celsius(value, from_unit)

    # セルシウスから目的の単位に変換
    result = _from_celsius(celsius, to_unit)

    return result


def _to_celsius(value: float, from_unit: str) -> float:
    """
    任意の単位からセルシウスに変換

    Args:
        value: 変換する値
        from_unit: 変換元の単位

    Returns:
        float: セルシウスでの値
    """
    if from_unit == 'celsius':
        return value
    elif from_unit == 'fahrenheit':
        return (value - 32) * 5 / 9
    elif from_unit == 'kelvin':
        return value - 273.15
    else:
        raise ValueError(f"Invalid unit: {from_unit}")


def _from_celsius(celsius: float, to_unit: str) -> float:
    """
    セルシウスから任意の単位に変換

    Args:
        celsius: セルシウスでの値
        to_unit: 変換先の単位

    Returns:
        float: 変換後の値
    """
    if to_unit == 'celsius':
        return celsius
    elif to_unit == 'fahrenheit':
        return celsius * 9 / 5 + 32
    elif to_unit == 'kelvin':
        return celsius + 273.15
    else:
        raise ValueError(f"Invalid unit: {to_unit}")
