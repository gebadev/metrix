"""
温度変換のテストモジュール
"""

import pytest
from converters.temperature import convert_temperature, get_temperature_units


class TestGetTemperatureUnits:
    """get_temperature_units関数のテスト"""

    def test_returns_list(self):
        """リストを返すことを確認"""
        units = get_temperature_units()
        assert isinstance(units, list)

    def test_contains_all_units(self):
        """すべての対応単位が含まれることを確認"""
        units = get_temperature_units()
        expected_units = ['celsius', 'fahrenheit', 'kelvin']
        for unit in expected_units:
            assert unit in units


class TestConvertTemperature:
    """convert_temperature関数のテスト"""

    def test_same_unit_conversion(self):
        """同じ単位間の変換（値が変わらない）"""
        assert convert_temperature(100, 'celsius', 'celsius') == 100
        assert convert_temperature(212, 'fahrenheit', 'fahrenheit') == 212
        assert convert_temperature(373.15, 'kelvin', 'kelvin') == 373.15

    def test_celsius_to_fahrenheit(self):
        """セルシウスから華氏への変換"""
        assert convert_temperature(0, 'celsius', 'fahrenheit') == 32
        assert convert_temperature(100, 'celsius', 'fahrenheit') == 212
        assert convert_temperature(-40, 'celsius', 'fahrenheit') == -40
        assert convert_temperature(37, 'celsius', 'fahrenheit') == pytest.approx(98.6, rel=1e-4)

    def test_fahrenheit_to_celsius(self):
        """華氏からセルシウスへの変換"""
        assert convert_temperature(32, 'fahrenheit', 'celsius') == 0
        assert convert_temperature(212, 'fahrenheit', 'celsius') == 100
        assert convert_temperature(-40, 'fahrenheit', 'celsius') == -40
        assert convert_temperature(98.6, 'fahrenheit', 'celsius') == pytest.approx(37, rel=1e-4)

    def test_celsius_to_kelvin(self):
        """セルシウスからケルビンへの変換"""
        assert convert_temperature(0, 'celsius', 'kelvin') == 273.15
        assert convert_temperature(100, 'celsius', 'kelvin') == 373.15
        assert convert_temperature(-273.15, 'celsius', 'kelvin') == 0
        assert convert_temperature(25, 'celsius', 'kelvin') == 298.15

    def test_kelvin_to_celsius(self):
        """ケルビンからセルシウスへの変換"""
        assert convert_temperature(273.15, 'kelvin', 'celsius') == 0
        assert convert_temperature(373.15, 'kelvin', 'celsius') == 100
        assert convert_temperature(0, 'kelvin', 'celsius') == -273.15
        assert convert_temperature(298.15, 'kelvin', 'celsius') == 25

    def test_fahrenheit_to_kelvin(self):
        """華氏からケルビンへの変換"""
        assert convert_temperature(32, 'fahrenheit', 'kelvin') == pytest.approx(273.15, rel=1e-4)
        assert convert_temperature(212, 'fahrenheit', 'kelvin') == pytest.approx(373.15, rel=1e-4)
        assert convert_temperature(-459.67, 'fahrenheit', 'kelvin') == pytest.approx(0, rel=1e-4)

    def test_kelvin_to_fahrenheit(self):
        """ケルビンから華氏への変換"""
        assert convert_temperature(273.15, 'kelvin', 'fahrenheit') == pytest.approx(32, rel=1e-4)
        assert convert_temperature(373.15, 'kelvin', 'fahrenheit') == pytest.approx(212, rel=1e-4)
        assert convert_temperature(0, 'kelvin', 'fahrenheit') == pytest.approx(-459.67, rel=1e-4)

    def test_absolute_zero(self):
        """絶対零度（0K = -273.15°C = -459.67°F）のテスト"""
        # 絶対零度の変換
        assert convert_temperature(0, 'kelvin', 'celsius') == -273.15
        assert convert_temperature(0, 'kelvin', 'fahrenheit') == pytest.approx(-459.67, rel=1e-4)
        assert convert_temperature(-273.15, 'celsius', 'kelvin') == 0
        assert convert_temperature(-459.67, 'fahrenheit', 'kelvin') == pytest.approx(0, rel=1e-4)

    def test_freezing_point(self):
        """氷点（0°C = 32°F = 273.15K）のテスト"""
        assert convert_temperature(0, 'celsius', 'fahrenheit') == 32
        assert convert_temperature(0, 'celsius', 'kelvin') == 273.15
        assert convert_temperature(32, 'fahrenheit', 'celsius') == 0
        assert convert_temperature(32, 'fahrenheit', 'kelvin') == pytest.approx(273.15, rel=1e-4)
        assert convert_temperature(273.15, 'kelvin', 'celsius') == 0
        assert convert_temperature(273.15, 'kelvin', 'fahrenheit') == pytest.approx(32, rel=1e-4)

    def test_boiling_point(self):
        """沸点（100°C = 212°F = 373.15K）のテスト"""
        assert convert_temperature(100, 'celsius', 'fahrenheit') == 212
        assert convert_temperature(100, 'celsius', 'kelvin') == 373.15
        assert convert_temperature(212, 'fahrenheit', 'celsius') == 100
        assert convert_temperature(212, 'fahrenheit', 'kelvin') == pytest.approx(373.15, rel=1e-4)
        assert convert_temperature(373.15, 'kelvin', 'celsius') == 100
        assert convert_temperature(373.15, 'kelvin', 'fahrenheit') == pytest.approx(212, rel=1e-4)

    def test_zero_value(self):
        """0の値の変換"""
        assert convert_temperature(0, 'celsius', 'fahrenheit') == 32
        assert convert_temperature(0, 'celsius', 'kelvin') == 273.15

    def test_negative_value(self):
        """負の値の変換"""
        assert convert_temperature(-10, 'celsius', 'fahrenheit') == 14
        assert convert_temperature(-20, 'celsius', 'kelvin') == pytest.approx(253.15, rel=1e-4)

    def test_decimal_value(self):
        """小数の値の変換"""
        assert convert_temperature(36.5, 'celsius', 'fahrenheit') == pytest.approx(97.7, rel=1e-4)
        assert convert_temperature(98.6, 'fahrenheit', 'celsius') == pytest.approx(37, rel=1e-4)

    def test_large_value(self):
        """大きな値の変換"""
        assert convert_temperature(1000, 'celsius', 'kelvin') == 1273.15
        assert convert_temperature(5000, 'kelvin', 'celsius') == 4726.85

    def test_invalid_from_unit(self):
        """無効な変換元単位でValueErrorが発生することを確認"""
        with pytest.raises(ValueError, match="Invalid unit: xyz"):
            convert_temperature(100, 'xyz', 'celsius')

    def test_invalid_to_unit(self):
        """無効な変換先単位でValueErrorが発生することを確認"""
        with pytest.raises(ValueError, match="Invalid unit: abc"):
            convert_temperature(100, 'celsius', 'abc')

    def test_invalid_both_units(self):
        """両方の単位が無効な場合にValueErrorが発生することを確認"""
        with pytest.raises(ValueError):
            convert_temperature(100, 'xyz', 'abc')
