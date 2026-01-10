"""
長さ変換のテストモジュール
"""

import pytest
from converters.length import convert_length, get_length_units


class TestGetLengthUnits:
    """get_length_units関数のテスト"""

    def test_returns_list(self):
        """リストを返すことを確認"""
        units = get_length_units()
        assert isinstance(units, list)

    def test_contains_all_units(self):
        """すべての対応単位が含まれることを確認"""
        units = get_length_units()
        expected_units = ['m', 'km', 'cm', 'mm', 'in', 'ft', 'yd', 'mi']
        for unit in expected_units:
            assert unit in units


class TestConvertLength:
    """convert_length関数のテスト"""

    def test_same_unit_conversion(self):
        """同じ単位間の変換（値が変わらない）"""
        assert convert_length(100, 'm', 'm') == 100
        assert convert_length(5, 'km', 'km') == 5
        assert convert_length(10, 'in', 'in') == 10

    def test_meter_conversions(self):
        """メートルから他の単位への変換"""
        assert convert_length(1, 'm', 'km') == 0.001
        assert convert_length(1, 'm', 'cm') == 100
        assert convert_length(1, 'm', 'mm') == 1000
        assert convert_length(1, 'm', 'ft') == pytest.approx(3.28084, rel=1e-4)
        assert convert_length(1, 'm', 'in') == pytest.approx(39.3701, rel=1e-4)

    def test_kilometer_conversions(self):
        """キロメートルから他の単位への変換"""
        assert convert_length(1, 'km', 'm') == 1000
        assert convert_length(1, 'km', 'cm') == 100000
        assert convert_length(1, 'km', 'mi') == pytest.approx(0.621371, rel=1e-4)

    def test_inch_conversions(self):
        """インチから他の単位への変換"""
        assert convert_length(12, 'in', 'ft') == pytest.approx(1, rel=1e-4)
        assert convert_length(1, 'in', 'cm') == pytest.approx(2.54, rel=1e-4)
        assert convert_length(1, 'in', 'm') == pytest.approx(0.0254, rel=1e-4)

    def test_foot_conversions(self):
        """フィートから他の単位への変換"""
        assert convert_length(1, 'ft', 'in') == pytest.approx(12, rel=1e-4)
        assert convert_length(1, 'ft', 'm') == pytest.approx(0.3048, rel=1e-4)
        assert convert_length(3, 'ft', 'yd') == pytest.approx(1, rel=1e-4)

    def test_yard_conversions(self):
        """ヤードから他の単位への変換"""
        assert convert_length(1, 'yd', 'ft') == pytest.approx(3, rel=1e-4)
        assert convert_length(1, 'yd', 'm') == pytest.approx(0.9144, rel=1e-4)

    def test_mile_conversions(self):
        """マイルから他の単位への変換"""
        assert convert_length(1, 'mi', 'km') == pytest.approx(1.609344, rel=1e-4)
        assert convert_length(1, 'mi', 'm') == pytest.approx(1609.344, rel=1e-4)
        assert convert_length(1, 'mi', 'ft') == pytest.approx(5280, rel=1e-4)

    def test_zero_value(self):
        """0の値の変換"""
        assert convert_length(0, 'm', 'km') == 0
        assert convert_length(0, 'in', 'cm') == 0

    def test_negative_value(self):
        """負の値の変換"""
        assert convert_length(-10, 'm', 'cm') == -1000
        assert convert_length(-5, 'km', 'm') == -5000

    def test_decimal_value(self):
        """小数の値の変換"""
        assert convert_length(1.5, 'm', 'cm') == 150
        assert convert_length(0.5, 'km', 'm') == 500

    def test_large_value(self):
        """大きな値の変換"""
        assert convert_length(1000000, 'm', 'km') == 1000
        assert convert_length(10000, 'mi', 'km') == pytest.approx(16093.44, rel=1e-4)

    def test_invalid_from_unit(self):
        """無効な変換元単位でValueErrorが発生することを確認"""
        with pytest.raises(ValueError, match="Invalid unit: xyz"):
            convert_length(100, 'xyz', 'm')

    def test_invalid_to_unit(self):
        """無効な変換先単位でValueErrorが発生することを確認"""
        with pytest.raises(ValueError, match="Invalid unit: abc"):
            convert_length(100, 'm', 'abc')

    def test_invalid_both_units(self):
        """両方の単位が無効な場合にValueErrorが発生することを確認"""
        with pytest.raises(ValueError):
            convert_length(100, 'xyz', 'abc')
