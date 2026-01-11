"""
重さ変換のテストモジュール
"""

import pytest
from converters.weight import convert_weight, get_weight_units


class TestGetWeightUnits:
    """get_weight_units関数のテスト"""

    def test_returns_list(self):
        """リストを返すことを確認"""
        units = get_weight_units()
        assert isinstance(units, list)

    def test_contains_all_units(self):
        """すべての対応単位が含まれることを確認"""
        units = get_weight_units()
        expected_units = ['g', 'kg', 'mg', 'lb', 'oz']
        for unit in expected_units:
            assert unit in units


class TestConvertWeight:
    """convert_weight関数のテスト"""

    def test_same_unit_conversion(self):
        """同じ単位間の変換（値が変わらない）"""
        assert convert_weight(100, 'g', 'g') == 100
        assert convert_weight(5, 'kg', 'kg') == 5
        assert convert_weight(10, 'lb', 'lb') == 10

    def test_gram_conversions(self):
        """グラムから他の単位への変換"""
        assert convert_weight(1, 'g', 'kg') == 0.001
        assert convert_weight(1, 'g', 'mg') == 1000
        assert convert_weight(1000, 'g', 'kg') == 1
        assert convert_weight(453.59237, 'g', 'lb') == pytest.approx(1, rel=1e-4)

    def test_kilogram_conversions(self):
        """キログラムから他の単位への変換"""
        assert convert_weight(1, 'kg', 'g') == 1000
        assert convert_weight(1, 'kg', 'mg') == 1000000
        assert convert_weight(1, 'kg', 'lb') == pytest.approx(2.20462, rel=1e-4)
        assert convert_weight(1, 'kg', 'oz') == pytest.approx(35.274, rel=1e-3)

    def test_milligram_conversions(self):
        """ミリグラムから他の単位への変換"""
        assert convert_weight(1000, 'mg', 'g') == 1
        assert convert_weight(1000000, 'mg', 'kg') == 1
        assert convert_weight(1, 'mg', 'g') == 0.001

    def test_pound_conversions(self):
        """ポンドから他の単位への変換"""
        assert convert_weight(1, 'lb', 'g') == pytest.approx(453.59237, rel=1e-4)
        assert convert_weight(1, 'lb', 'kg') == pytest.approx(0.45359237, rel=1e-4)
        assert convert_weight(1, 'lb', 'oz') == pytest.approx(16, rel=1e-4)

    def test_ounce_conversions(self):
        """オンスから他の単位への変換"""
        assert convert_weight(1, 'oz', 'g') == pytest.approx(28.349523125, rel=1e-4)
        assert convert_weight(16, 'oz', 'lb') == pytest.approx(1, rel=1e-4)
        assert convert_weight(1, 'oz', 'kg') == pytest.approx(0.0283495, rel=1e-4)

    def test_zero_value(self):
        """0の値の変換"""
        assert convert_weight(0, 'g', 'kg') == 0
        assert convert_weight(0, 'lb', 'oz') == 0

    def test_negative_value(self):
        """負の値の変換"""
        assert convert_weight(-10, 'g', 'kg') == -0.01
        assert convert_weight(-5, 'kg', 'g') == -5000

    def test_decimal_value(self):
        """小数の値の変換"""
        assert convert_weight(1.5, 'kg', 'g') == 1500
        assert convert_weight(0.5, 'lb', 'oz') == pytest.approx(8, rel=1e-4)

    def test_large_value(self):
        """大きな値の変換"""
        assert convert_weight(1000000, 'g', 'kg') == 1000
        assert convert_weight(10000, 'lb', 'kg') == pytest.approx(4535.9237, rel=1e-4)

    def test_invalid_from_unit(self):
        """無効な変換元単位でValueErrorが発生することを確認"""
        with pytest.raises(ValueError, match="Invalid unit: xyz"):
            convert_weight(100, 'xyz', 'g')

    def test_invalid_to_unit(self):
        """無効な変換先単位でValueErrorが発生することを確認"""
        with pytest.raises(ValueError, match="Invalid unit: abc"):
            convert_weight(100, 'g', 'abc')

    def test_invalid_both_units(self):
        """両方の単位が無効な場合にValueErrorが発生することを確認"""
        with pytest.raises(ValueError):
            convert_weight(100, 'xyz', 'abc')
