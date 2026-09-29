"""Ядро интернет-магазина: абстрактные классы, миксины, наследование и обработка исключений."""

import json
from abc import ABC, abstractmethod
from typing import List, Optional


# ==========================================================
# ПОЛЬЗОВАТЕЛЬСКИЕ ИСКЛЮЧЕНИЯ (доп. задание)
# ==========================================================


class ZeroQuantityError(Exception):
    """Пользовательское исключение для товара с нулевым количеством."""

    pass


# ==========================================================
# АБСТРАКТНЫЕ КЛАССЫ И МИКСИНЫ
# ==========================================================


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @property
    @abstractmethod
    def price(self) -> float:
        """Абстрактный геттер цены."""
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        """Абстрактный сеттер цены."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод строкового представления."""
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        """Абстрактный метод сложения."""
        pass


class ReprMixin:
    """Миксин для вывода информации о создании объекта."""

    def __init__(self, *args, **kwargs):
        args_repr = ", ".join(repr(arg) for arg in args)
        print(f"{self.__class__.__name__}({args_repr})")
        super().__init__()


# ==========================================================
# КЛАССЫ ПРОДУКТОВ
# ==========================================================


class Product(ReprMixin, BaseProduct):
    """Базовый класс товара интернет-магазина."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        # Задание 1: Проверка на нулевое количество
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        # Вызываем миксин для печати информации
        ReprMixin.__init__(self, name, description, price, quantity)

        # Инициализация атрибутов
        self.name = name
        self.description = description
        self.__price = float(price)
        self.quantity = int(quantity)

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Сеттер для цены с валидацией."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if value < self.__price:
            user_input = input(
                f"Цена понижается с {self.__price} до {value}. Подтвердите (y/n): "
            )
            if user_input.lower() != "y":
                return
        self.__price = value

    @classmethod
    def new_product(
        cls, product_data: dict, existing_products: Optional[List["Product"]] = None
    ) -> "Product":
        """Создает продукт из словаря с проверкой дубликатов."""
        if existing_products:
            for prod in existing_products:
                if prod.name == product_data["name"]:
                    prod.quantity += product_data["quantity"]
                    if product_data["price"] > prod.price:
                        prod.price = product_data["price"]
                    return prod
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __str__(self) -> str:
        """Строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, price={self.price}, quantity={self.quantity})"

    def __add__(self, other: "Product") -> float:
        """Сложение двух товаров: сумма произведений цены на количество."""
        if type(self) != type(other):
            raise TypeError(
                f"Нельзя складывать товары разных типов: {self.__class__.__name__} и {other.__class__.__name__}"
            )
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс смартфона — наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        return f"{self.name} ({self.model}), {self.price} руб. Остаток: {self.quantity} шт."


class LawnGrass(Product):
    """Класс газонной травы — наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


# ==========================================================
# КЛАСС КАТЕГОРИИ
# ==========================================================


class Category:
    """Категория товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию с проверкой типа."""
        if not isinstance(product, Product):
            raise TypeError(
                f"Можно добавлять только объекты класса Product или его наследников, "
                f"получен тип: {type(product).__name__}"
            )

        # Дополнительное задание: обработка нулевого количества
        try:
            if product.quantity == 0:
                raise ZeroQuantityError(
                    "Товар с нулевым количеством не может быть добавлен в категорию"
                )
            self.__products.append(product)
            Category.product_count += 1
            print(f"Товар '{product.name}' успешно добавлен в категорию")
        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
        finally:
            print("Обработка добавления товара завершена")

    @property
    def products(self) -> str:
        """Геттер списка товаров в формате строки."""
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result

    def middle_price(self) -> float:
        """
        Задание 2: Подсчёт среднего ценника всех товаров в категории.
        Если товаров нет — возвращает 0.
        """
        try:
            total_price = sum(product.price for product in self.__products)
            average = total_price / len(self.__products)
            return average
        except ZeroDivisionError:
            return 0.0

    def __str__(self) -> str:
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __repr__(self) -> str:
        return f"Category(name={self.name!r}, products_count={len(self.__products)})"


# ==========================================================
# ИТЕРАТОР И ЗАГРУЗКА ИЗ JSON
# ==========================================================


class CategoryIterator:
    """Итератор для перебора товаров категории."""

    def __init__(self, category: Category) -> None:
        self._products = category._Category__products
        self._index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product


def load_products_from_json(file_path: str) -> List[Category]:
    """Загружает категории и товары из JSON-файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    categories: List[Category] = []
    for cat_data in data:
        products = [
            Product(
                name=p["name"],
                description=p["description"],
                price=p["price"],
                quantity=p["quantity"],
            )
            for p in cat_data.get("products", [])
        ]
        categories.append(
            Category(
                name=cat_data["name"],
                description=cat_data["description"],
                products=products,
            )
        )
    return categories


# ==========================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ==========================================================

if __name__ == "__main__":
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством"
        )
    else:
        print(
            "Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством"
        )

    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны", "Категория смартфонов", [product1, product2, product3]
    )

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())
