"""
カスタム例外クラス

API全体で使用するカスタム例外を定義
"""


class MetrixException(Exception):
    """metrixアプリケーションの基底例外クラス"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(MetrixException):
    """バリデーションエラー (400)"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class InvalidCategoryError(MetrixException):
    """無効なカテゴリエラー (400)"""
    def __init__(self, category: str):
        super().__init__(f"Invalid category: {category}", status_code=400)


class InvalidUnitError(MetrixException):
    """無効な単位エラー (400)"""
    def __init__(self, unit: str):
        super().__init__(f"Invalid unit: {unit}", status_code=400)


class CategoryNotFoundError(MetrixException):
    """カテゴリが見つからないエラー (404)"""
    def __init__(self, category: str):
        super().__init__(f"Category not found: {category}", status_code=404)
