"""Тесты для классов Product и Category."""

import json

import pytest

from src.main import Category, Product, load_products_from_json


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счетчики классов перед каждым тестом для изоляции."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


class TestProduct:
    def test_product_initialization(self):
        product = Product("Ноутбук", "Мощный", 150000.0, 5)
        assert product.name == "Ноутбук"
        assert product.description == "Мощный"
        assert product.price == 150000.0
        assert product.quantity == 5

    def test_product_types(self):
        product = Product("Тест", "Описание", "99.99", "10")
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)


class TestCategory:
    def test_category_initialization(self):
        products = [Product("Товар 1", "Описание", 100.0, 1)]
        category = Category("Тестовая категория", "Описание категории", products)
        assert category.name == "Тестовая категория"
        assert category.description == "Описание категории"
        assert len(category.products) == 1
        assert isinstance(category.products[0], Product)


class TestCounters:
    def test_category_count_increments(self):
        Category("Кат 1", "Опис 1", [])
        Category("Кат 2", "Опис 2", [])
        assert Category.category_count == 2

    def test_product_count_increments(self):
        products1 = [Product("Т1", "О1", 10.0, 2)]
        products2 = [Product("Т2", "О2", 20.0, 3), Product("Т3", "О3", 30.0, 1)]

        Category("Кат 1", "Опис 1", products1)
        Category("Кат 2", "Опис 2", products2)

        assert Category.product_count == 3  # 2 + 1


class TestJsonLoader:
    def test_load_from_json(self, tmp_path):
        # Создаем временный JSON файл для теста
        data = [
            {
                "name": "Загрузка",
                "description": "Тест загрузки",
                "products": [
                    {
                        "name": "Товар",
                        "description": "Опис",
                        "price": 50.0,
                        "quantity": 4,
                    }
                ],
            }
        ]
        file_path = tmp_path / "test_products.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        categories = load_products_from_json(str(file_path))

        assert len(categories) == 1
        assert isinstance(categories[0], Category)
        assert categories[0].name == "Загрузка"
        assert len(categories[0].products) == 1
        assert isinstance(categories[0].products[0], Product)
        assert categories[0].products[0].price == 50.0
