import json
import pytest
from src.main import Product, Category, CategoryIterator, load_products_from_json


class TestProduct:
    def test_product_initialization(self):
        product = Product("Товар", "Описание", 100.0, 5)
        assert product.name == "Товар"
        assert product.description == "Описание"
        assert product.price == 100.0
        assert product.quantity == 5

    def test_product_types(self):
        product = Product("Товар", "Описание", "100.5", "5")
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)


class TestCategory:
    def test_category_initialization(self):
        products = [Product("Товар 1", "Описание", 100.0, 1)]
        category = Category("Тестовая категория", "Описание категории", products)
        assert category.name == "Тестовая категория"
        assert category.description == "Описание категории"
        assert len(category._Category__products) == 1


class TestCounters:
    def test_category_count_increments(self):
        Category.category_count = 0
        Category("Категория 1", "Описание", [])
        Category("Категория 2", "Описание", [])
        assert Category.category_count == 2

    def test_product_count_increments(self):
        Category.product_count = 0
        products = [Product("Товар 1", "Описание", 100.0, 1)]
        Category("Категория", "Описание", products)
        assert Category.product_count == 1


class TestJsonLoader:
    def test_load_from_json(self, tmp_path):
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
        assert len(categories[0]._Category__products) == 1


class TestProductEncapsulation:
    """Тесты инкапсуляции класса Product."""

    def test_price_is_private(self):
        product = Product("Тест", "Описание", 100.0, 5)
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_price_getter(self):
        product = Product("Тест", "Описание", 100.0, 5)
        assert product.price == 100.0

    def test_price_setter_rejects_zero(self):
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = 0
        assert product.price == 100.0

    def test_price_setter_rejects_negative(self):
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = -50
        assert product.price == 100.0

    def test_price_setter_accepts_positive(self, monkeypatch):
        product = Product("Тест", "Описание", 100.0, 5)
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        product.price = 200.0
        assert product.price == 200.0


class TestCategoryEncapsulation:
    """Тесты инкапсуляции класса Category."""

    def test_products_is_private(self):
        category = Category("Тест", "Описание", [])
        with pytest.raises(AttributeError):
            _ = category.__products

    def test_add_product(self):
        category = Category("Тест", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)
        category.add_product(product)
        assert len(category._Category__products) == 1
        assert category._Category__products[0].name == "Товар"

    def test_add_product_increments_counter(self):
        Category.product_count = 0
        category = Category("Тест", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)
        category.add_product(product)
        assert Category.product_count == 1

    def test_add_product_rejects_non_product(self):
        category = Category("Тест", "Описание", [])
        with pytest.raises(TypeError):
            category.add_product("не продукт")

    def test_products_returns_string(self):
        product = Product("Молоко", "Молочный продукт", 80.0, 15)
        category = Category("Продукты", "Еда", [product])
        result = category.products
        assert isinstance(result, str)
        assert result == "Молоко, 80.0 руб. Остаток: 15 шт.\n"


class TestNewProduct:
    """Тесты класс-метода new_product."""

    def test_new_product_creates_from_dict(self):
        data = {
            "name": "Товар",
            "description": "Описание",
            "price": 100.0,
            "quantity": 5
        }
        product = Product.new_product(data)
        assert product.name == "Товар"
        assert product.price == 100.0
        assert product.quantity == 5

    def test_new_product_duplicate_sum_quantity(self):
        existing = [Product("Товар", "Описание", 100.0, 5)]
        data = {
            "name": "Товар",
            "description": "Описание",
            "price": 100.0,
            "quantity": 3
        }
        product = Product.new_product(data, existing)
        assert product.quantity == 8
        assert product is existing[0]

    def test_new_product_duplicate_max_price(self):
        existing = [Product("Товар", "Описание", 100.0, 5)]
        data = {
            "name": "Товар",
            "description": "Описание",
            "price": 150.0,
            "quantity": 3
        }
        product = Product.new_product(data, existing)
        assert product.price == 150.0

    def test_new_product_duplicate_keeps_higher_price(self):
        existing = [Product("Товар", "Описание", 200.0, 5)]
        data = {
            "name": "Товар",
            "description": "Описание",
            "price": 100.0,
            "quantity": 3
        }
        product = Product.new_product(data, existing)
        assert product.price == 200.0


# ==========================================================
# НОВЫЕ ТЕСТЫ ДЛЯ ДЗ 15.1 (МАГИЧЕСКИЕ МЕТОДЫ)
# ==========================================================

class TestProductStr:
    """Тесты строкового представления Product."""

    def test_product_str(self):
        product = Product("Молоко", "Молочный продукт", 80.0, 15)
        assert str(product) == "Молоко, 80.0 руб. Остаток: 15 шт."

    def test_product_str_integer_price(self):
        product = Product("Хлеб", "Хлебобулочное", 50.0, 10)
        assert str(product) == "Хлеб, 50.0 руб. Остаток: 10 шт."


class TestCategoryStr:
    """Тесты строкового представления Category."""

    def test_category_str(self):
        p1 = Product("Молоко", "Молочный продукт", 80.0, 15)
        p2 = Product("Хлеб", "Хлебобулочное", 50.0, 10)
        category = Category("Продукты", "Еда", [p1, p2])
        assert str(category) == "Продукты, количество продуктов: 25 шт."

    def test_category_str_empty(self):
        category = Category("Пустая", "Без товаров", [])
        assert str(category) == "Пустая, количество продуктов: 0 шт."

    def test_category_str_single_product(self):
        p = Product("Товар", "Описание", 100.0, 7)
        category = Category("Тест", "Описание", [p])
        assert str(category) == "Тест, количество продуктов: 7 шт."


class TestProductAdd:
    """Тесты магического метода __add__ для Product."""

    def test_product_add(self):
        p1 = Product("A", "Описание", 100.0, 10)
        p2 = Product("B", "Описание", 200.0, 2)
        # 100 * 10 + 200 * 2 = 1000 + 400 = 1400
        assert p1 + p2 == 1400.0

    def test_product_add_commutative(self):
        p1 = Product("A", "Описание", 100.0, 10)
        p2 = Product("B", "Описание", 200.0, 2)
        assert p1 + p2 == p2 + p1

    def test_product_add_type_error(self):
        p1 = Product("A", "Описание", 100.0, 10)
        with pytest.raises(TypeError):
            _ = p1 + 100
        with pytest.raises(TypeError):
            _ = p1 + "строка"

    def test_product_add_with_zero_quantity(self):
        p1 = Product("A", "Описание", 100.0, 0)
        p2 = Product("B", "Описание", 200.0, 5)
        # 100 * 0 + 200 * 5 = 0 + 1000 = 1000
        assert p1 + p2 == 1000.0


class TestCategoryIterator:
    """Тесты итератора для Category."""

    def test_iterator_basic(self):
        p1 = Product("A", "Описание", 100.0, 10)
        p2 = Product("B", "Описание", 200.0, 2)
        category = Category("Тест", "Описание", [p1, p2])
        iterator = CategoryIterator(category)
        products = list(iterator)
        assert len(products) == 2
        assert products[0].name == "A"
        assert products[1].name == "B"

    def test_iterator_empty_category(self):
        category = Category("Пустая", "Описание", [])
        iterator = CategoryIterator(category)
        products = list(iterator)
        assert len(products) == 0

    def test_iterator_in_for_loop(self):
        p1 = Product("A", "Описание", 100.0, 10)
        p2 = Product("B", "Описание", 200.0, 2)
        p3 = Product("C", "Описание", 300.0, 3)
        category = Category("Тест", "Описание", [p1, p2, p3])

        names = []
        for product in CategoryIterator(category):
            names.append(product.name)

        assert names == ["A", "B", "C"]

    def test_iterator_stop_iteration(self):
        p1 = Product("A", "Описание", 100.0, 10)
        category = Category("Тест", "Описание", [p1])
        iterator = CategoryIterator(category)

        next(iterator)  # Первый товар
        with pytest.raises(StopIteration):
            next(iterator)  # Должен поднять StopIteration