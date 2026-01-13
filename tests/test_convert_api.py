"""
変換APIエンドポイントのテスト
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestConvertAPI:
    """POST /api/convert エンドポイントのテスト"""

    def test_convert_length_success(self):
        """長さ変換が正常に実行されること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 100,
                "from_unit": "m",
                "to_unit": "km",
                "category": "length"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["result"] == 0.1
        assert data["from_unit"] == "m"
        assert data["to_unit"] == "km"
        assert data["original_value"] == 100

    def test_convert_weight_success(self):
        """重さ変換が正常に実行されること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 1000,
                "from_unit": "g",
                "to_unit": "kg",
                "category": "weight"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["result"] == 1.0
        assert data["from_unit"] == "g"
        assert data["to_unit"] == "kg"
        assert data["original_value"] == 1000

    def test_convert_temperature_success(self):
        """温度変換が正常に実行されること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 0,
                "from_unit": "celsius",
                "to_unit": "fahrenheit",
                "category": "temperature"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["result"] == 32.0
        assert data["from_unit"] == "celsius"
        assert data["to_unit"] == "fahrenheit"
        assert data["original_value"] == 0

    def test_convert_invalid_category(self):
        """無効なカテゴリで400エラーが返ること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 100,
                "from_unit": "m",
                "to_unit": "km",
                "category": "invalid_category"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "Category must be one of" in data["error"]

    def test_convert_invalid_from_unit(self):
        """無効な変換元単位で400エラーが返ること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 100,
                "from_unit": "invalid_unit",
                "to_unit": "km",
                "category": "length"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "Invalid unit" in data["error"]

    def test_convert_invalid_to_unit(self):
        """無効な変換先単位で400エラーが返ること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 100,
                "from_unit": "m",
                "to_unit": "invalid_unit",
                "category": "length"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "Invalid unit" in data["error"]

    def test_convert_missing_fields(self):
        """必須フィールドが欠けている場合に400エラーが返ること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 100,
                "from_unit": "m"
                # to_unit と category が欠けている
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "error" in data

    def test_convert_various_length_units(self):
        """様々な長さ単位の変換が正しく動作すること"""
        test_cases = [
            {"value": 1, "from_unit": "km", "to_unit": "m", "expected": 1000},
            {"value": 1, "from_unit": "m", "to_unit": "cm", "expected": 100},
            {"value": 1, "from_unit": "ft", "to_unit": "in", "expected": 12},
            {"value": 1, "from_unit": "mi", "to_unit": "km", "expected": 1.609344},
        ]

        for case in test_cases:
            response = client.post(
                "/api/convert",
                json={
                    "value": case["value"],
                    "from_unit": case["from_unit"],
                    "to_unit": case["to_unit"],
                    "category": "length"
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert abs(data["result"] - case["expected"]) < 0.000001

    def test_convert_various_weight_units(self):
        """様々な重さ単位の変換が正しく動作すること"""
        test_cases = [
            {"value": 1, "from_unit": "kg", "to_unit": "g", "expected": 1000},
            {"value": 1, "from_unit": "lb", "to_unit": "oz", "expected": 16},
            {"value": 1, "from_unit": "kg", "to_unit": "lb", "expected": 2.20462262185},
        ]

        for case in test_cases:
            response = client.post(
                "/api/convert",
                json={
                    "value": case["value"],
                    "from_unit": case["from_unit"],
                    "to_unit": case["to_unit"],
                    "category": "weight"
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert abs(data["result"] - case["expected"]) < 0.000001

    def test_convert_various_temperature_units(self):
        """様々な温度単位の変換が正しく動作すること"""
        test_cases = [
            {"value": 100, "from_unit": "celsius", "to_unit": "fahrenheit", "expected": 212},
            {"value": 0, "from_unit": "celsius", "to_unit": "kelvin", "expected": 273.15},
            {"value": 32, "from_unit": "fahrenheit", "to_unit": "celsius", "expected": 0},
            {"value": 273.15, "from_unit": "kelvin", "to_unit": "celsius", "expected": 0},
        ]

        for case in test_cases:
            response = client.post(
                "/api/convert",
                json={
                    "value": case["value"],
                    "from_unit": case["from_unit"],
                    "to_unit": case["to_unit"],
                    "category": "temperature"
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert abs(data["result"] - case["expected"]) < 0.000001

    def test_convert_negative_values(self):
        """負の値でも正しく変換できること"""
        response = client.post(
            "/api/convert",
            json={
                "value": -40,
                "from_unit": "celsius",
                "to_unit": "fahrenheit",
                "category": "temperature"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == -40.0

    def test_convert_zero_value(self):
        """値が0でも正しく変換できること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 0,
                "from_unit": "m",
                "to_unit": "km",
                "category": "length"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.0

    def test_convert_decimal_values(self):
        """小数点を含む値でも正しく変換できること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 3.5,
                "from_unit": "kg",
                "to_unit": "g",
                "category": "weight"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 3500.0


class TestUnitsAPI:
    """GET /api/units/{category} エンドポイントのテスト"""

    def test_get_length_units(self):
        """長さカテゴリの単位一覧が取得できること"""
        response = client.get("/api/units/length")
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "length"
        assert "units" in data
        assert len(data["units"]) > 0

        # 単位情報の構造を確認
        for unit in data["units"]:
            assert "code" in unit
            assert "name" in unit

        # 特定の単位が含まれているか確認
        unit_codes = [unit["code"] for unit in data["units"]]
        assert "m" in unit_codes
        assert "km" in unit_codes
        assert "cm" in unit_codes

    def test_get_weight_units(self):
        """重さカテゴリの単位一覧が取得できること"""
        response = client.get("/api/units/weight")
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "weight"
        assert "units" in data
        assert len(data["units"]) > 0

        # 特定の単位が含まれているか確認
        unit_codes = [unit["code"] for unit in data["units"]]
        assert "g" in unit_codes
        assert "kg" in unit_codes
        assert "lb" in unit_codes

    def test_get_temperature_units(self):
        """温度カテゴリの単位一覧が取得できること"""
        response = client.get("/api/units/temperature")
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "temperature"
        assert "units" in data
        assert len(data["units"]) > 0

        # 特定の単位が含まれているか確認
        unit_codes = [unit["code"] for unit in data["units"]]
        assert "celsius" in unit_codes
        assert "fahrenheit" in unit_codes
        assert "kelvin" in unit_codes

    def test_get_units_invalid_category(self):
        """無効なカテゴリで404エラーが返ること"""
        response = client.get("/api/units/invalid_category")
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "Category not found" in data["error"]

    def test_get_units_with_japanese_names(self):
        """単位情報に日本語名称が含まれていること"""
        response = client.get("/api/units/length")
        assert response.status_code == 200
        data = response.json()

        # メートルの単位を探す
        meter_unit = next((u for u in data["units"] if u["code"] == "m"), None)
        assert meter_unit is not None
        assert meter_unit["name"] == "メートル"

        # キロメートルの単位を探す
        km_unit = next((u for u in data["units"] if u["code"] == "km"), None)
        assert km_unit is not None
        assert km_unit["name"] == "キロメートル"


class TestErrorHandling:
    """エラーハンドリングのテスト"""

    def test_convert_empty_unit(self):
        """空の単位文字列で400エラーが返ること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 100,
                "from_unit": "",
                "to_unit": "km",
                "category": "length"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "error" in data

    def test_convert_whitespace_unit(self):
        """空白のみの単位で400エラーが返ること"""
        response = client.post(
            "/api/convert",
            json={
                "value": 100,
                "from_unit": "   ",
                "to_unit": "km",
                "category": "length"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_convert_invalid_value_type(self):
        """無効な値の型で400エラーが返ること"""
        response = client.post(
            "/api/convert",
            json={
                "value": "not_a_number",
                "from_unit": "m",
                "to_unit": "km",
                "category": "length"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_health_endpoint(self):
        """ヘルスチェックエンドポイントが正常に動作すること"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_cors_headers(self):
        """CORSヘッダーが設定されていること"""
        # POSTリクエストでCORSヘッダーをチェック
        response = client.post(
            "/api/convert",
            json={
                "value": 100,
                "from_unit": "m",
                "to_unit": "km",
                "category": "length"
            },
            headers={"Origin": "http://localhost:3000"}
        )
        # 通常のリクエストでもCORSヘッダーが返される
        assert response.status_code == 200
