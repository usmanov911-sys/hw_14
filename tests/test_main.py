import json
import pytest
from src.main import Product, Category, load_products_from_json


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
        # Обращаемся к приватному атрибуту через name mangling для проверки
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
        # Обращаемся к приватному атрибуту через name mangling
        assert len(categories[0]._Category__products) == 1


class TestProductEncapsulation:
    """Тесты инкапсуляции класса Product (Задание 4)."""

    def test_price_is_private(self):
        """Цена должна быть приватным атрибутом."""
        product = Product("Тест", "Описание", 100.0, 5)
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_price_getter(self):
        """Геттер должен возвращать корректную цену."""
        product = Product("Тест", "Описание", 100.0, 5)
        assert product.price == 100.0

    def test_price_setter_rejects_zero(self):
        """Сеттер не должен устанавливать нулевую цену."""
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = 0
        assert product.price == 100.0

    def test_price_setter_rejects_negative(self):
        """Сеттер не должен устанавливать отрицательную цену."""
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = -50
        assert product.price == 100.0

    def test_price_setter_accepts_positive(self, monkeypatch):
        """Сеттер принимает положительную цену."""
        product = Product("Тест", "Описание", 100.0, 5)
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        product.price = 200.0
        assert product.price == 200.0


class TestCategoryEncapsulation:
    """Тесты инкапсуляции класса Category (Задания 1 и 2)."""

    def test_products_is_private(self):
        """Список товаров должен быть приватным атрибутом."""
        category = Category("Тест", "Описание", [])
        with pytest.raises(AttributeError):
            _ = category.__products

    def test_add_product(self):
        """Метод add_product добавляет товар в категорию."""
        category = Category("Тест", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)
        category.add_product(product)
        assert len(category._Category__products) == 1
        assert category._Category__products[0].name == "Товар"

    def test_add_product_increments_counter(self):
        """add_product увеличивает счетчик product_count."""
        Category.product_count = 0
        category = Category("Тест", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)
        category.add_product(product)
        assert Category.product_count == 1

    def test_add_product_rejects_non_product(self):
        """add_product отклоняет объекты не класса Product."""
        category = Category("Тест", "Описание", [])
        with pytest.raises(TypeError):
            category.add_product("не продукт")

    def test_products_returns_string(self):
        """Геттер products возвращает строку в правильном формате."""
        product = Product("Молоко", "Молочный продукт", 80.0, 15)
        category = Category("Продукты", "Еда", [product])
        result = category.products
        assert isinstance(result, str)
        assert result == "Молоко, 80.0 руб. Остаток: 15 шт.\n"

    def test_products_multiple_items(self):
        """Геттер products корректно выводит несколько товаров."""
        p1 = Product("Молоко", "Молочный продукт", 80.0, 15)
        p2 = Product("Хлеб", "Хлебобулочное", 50.0, 10)
        category = Category("Продукты", "Еда", [p1, p2])
        result = category.products
        assert "Молоко, 80.0 руб. Остаток: 15 шт." in result
        assert "Хлеб, 50.0 руб. Остаток: 10 шт." in result


class TestNewProduct:
    """Тесты класс-метода new_product (Задание 3)."""

    def test_new_product_creates_from_dict(self):
        """new_product создает объект из словаря."""
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
        """При дубликате количество должно суммироваться."""
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
        """При дубликате должна выбираться максимальная цена."""
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
        """Если новая цена ниже, старая сохраняется."""
        existing = [Product("Товар", "Описание", 200.0, 5)]
        data = {
            "name": "Товар",
            "description": "Описание",
            "price": 100.0,
            "quantity": 3
        }
        product = Product.new_product(data, existing)
        assert product.price == 200.0