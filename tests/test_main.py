import json
import pytest
from src.main import Product, Smartphone, LawnGrass, Category, CategoryIterator, load_products_from_json


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


class TestProductStr:
    """Тесты строкового представления Product."""

    def test_product_str(self):
        product = Product("Молоко", "Молочный продукт", 80.0, 15)
        assert str(product) == "Молоко, 80.0 руб. Остаток: 15 шт."


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


class TestProductAdd:
    """Тесты магического метода __add__ для Product."""

    def test_product_add(self):
        p1 = Product("A", "Описание", 100.0, 10)
        p2 = Product("B", "Описание", 200.0, 2)
        assert p1 + p2 == 1400.0

    def test_product_add_type_error(self):
        p1 = Product("A", "Описание", 100.0, 10)
        with pytest.raises(TypeError):
            _ = p1 + 100


class TestCategoryIterator:
    """Тесты итератора для Category."""

    def test_iterator_basic(self):
        p1 = Product("A", "Описание", 100.0, 10)
        p2 = Product("B", "Описание", 200.0, 2)
        category = Category("Тест", "Описание", [p1, p2])
        iterator = CategoryIterator(category)
        products = list(iterator)
        assert len(products) == 2


# ==========================================================
# НОВЫЕ ТЕСТЫ ДЛЯ ДЗ 16.1 (НАСЛЕДОВАНИЕ)
# ==========================================================

class TestSmartphone:
    """Тесты класса Smartphone."""

    def test_smartphone_initialization(self):
        smartphone = Smartphone(
            "Samsung Galaxy S23", "Описание", 100000.0, 5,
            95.5, "S23", 256, "Серый"
        )
        assert smartphone.name == "Samsung Galaxy S23"
        assert smartphone.price == 100000.0
        assert smartphone.quantity == 5
        assert smartphone.efficiency == 95.5
        assert smartphone.model == "S23"
        assert smartphone.memory == 256
        assert smartphone.color == "Серый"

    def test_smartphone_inheritance(self):
        smartphone = Smartphone(
            "Samsung", "Описание", 100000.0, 5,
            95.5, "S23", 256, "Серый"
        )
        assert isinstance(smartphone, Product)
        assert isinstance(smartphone, Smartphone)

    def test_smartphone_add(self):
        s1 = Smartphone("A", "Описание", 100.0, 10, 95.0, "M1", 128, "Черный")
        s2 = Smartphone("B", "Описание", 200.0, 5, 90.0, "M2", 256, "Белый")
        # 100 * 10 + 200 * 5 = 1000 + 1000 = 2000
        assert s1 + s2 == 2000.0

    def test_smartphone_add_type_error(self):
        s1 = Smartphone("A", "Описание", 100.0, 10, 95.0, "M1", 128, "Черный")
        g1 = LawnGrass("B", "Описание", 50.0, 20, "Россия", "7 дней", "Зеленый")
        with pytest.raises(TypeError):
            _ = s1 + g1


class TestLawnGrass:
    """Тесты класса LawnGrass."""

    def test_lawn_grass_initialization(self):
        grass = LawnGrass(
            "Газонная трава", "Описание", 500.0, 20,
            "Россия", "7 дней", "Зеленый"
        )
        assert grass.name == "Газонная трава"
        assert grass.price == 500.0
        assert grass.quantity == 20
        assert grass.country == "Россия"
        assert grass.germination_period == "7 дней"
        assert grass.color == "Зеленый"

    def test_lawn_grass_inheritance(self):
        grass = LawnGrass(
            "Трава", "Описание", 500.0, 20,
            "Россия", "7 дней", "Зеленый"
        )
        assert isinstance(grass, Product)
        assert isinstance(grass, LawnGrass)

    def test_lawn_grass_add(self):
        g1 = LawnGrass("A", "Описание", 100.0, 10, "Россия", "7 дней", "Зеленый")
        g2 = LawnGrass("B", "Описание", 200.0, 5, "США", "5 дней", "Темно-зеленый")
        # 100 * 10 + 200 * 5 = 1000 + 1000 = 2000
        assert g1 + g2 == 2000.0

    def test_lawn_grass_add_type_error(self):
        g1 = LawnGrass("A", "Описание", 100.0, 10, "Россия", "7 дней", "Зеленый")
        s1 = Smartphone("B", "Описание", 200.0, 5, 95.0, "M1", 128, "Черный")
        with pytest.raises(TypeError):
            _ = g1 + s1


class TestAddProductRestrictions:
    """Тесты ограничений на добавление продуктов в категорию."""

    def test_add_product_accepts_product(self):
        category = Category("Тест", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)
        category.add_product(product)
        assert len(category._Category__products) == 1

    def test_add_product_accepts_smartphone(self):
        category = Category("Тест", "Описание", [])
        smartphone = Smartphone(
            "Samsung", "Описание", 100000.0, 5,
            95.5, "S23", 256, "Серый"
        )
        category.add_product(smartphone)
        assert len(category._Category__products) == 1

    def test_add_product_accepts_lawn_grass(self):
        category = Category("Тест", "Описание", [])
        grass = LawnGrass(
            "Трава", "Описание", 500.0, 20,
            "Россия", "7 дней", "Зеленый"
        )
        category.add_product(grass)
        assert len(category._Category__products) == 1

    def test_add_product_rejects_string(self):
        category = Category("Тест", "Описание", [])
        with pytest.raises(TypeError):
            category.add_product("не продукт")

    def test_add_product_rejects_dict(self):
        category = Category("Тест", "Описание", [])
        with pytest.raises(TypeError):
            category.add_product({"name": "Товар"})

    def test_add_product_rejects_number(self):
        category = Category("Тест", "Описание", [])
        with pytest.raises(TypeError):
            category.add_product(123)