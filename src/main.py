"""Ядро интернет-магазина: классы Product и Category."""

import json
from typing import List, Optional


class Product:
    """Товар интернет-магазина."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = float(price)  # Приватный атрибут цены
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

        # Подтверждение при понижении цены
        if value < self.__price:
            user_input = input(
                f"Цена понижается с {self.__price} до {value}. Подтвердите (y/n): "
            )
            if user_input.lower() != 'y':
                return

        self.__price = value

    @classmethod
    def new_product(
        cls,
        product_data: dict,
        existing_products: Optional[List['Product']] = None
    ) -> 'Product':
        """Создает продукт из словаря с проверкой дубликатов."""
        if existing_products:
            for prod in existing_products:
                if prod.name == product_data['name']:
                    prod.quantity += product_data['quantity']
                    if product_data['price'] > prod.price:
                        prod.price = product_data['price']
                    return prod

        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    def __str__(self) -> str:
        """Строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return (
            f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"
        )

    def __add__(self, other: 'Product') -> float:
        """Сложение двух товаров: сумма произведений цены на количество."""
        if not isinstance(other, Product):
            raise TypeError(
                f"Нельзя сложить Product с объектом типа {type(other).__name__}"
            )
        return self.price * self.quantity + other.price * other.quantity


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
        """Добавляет товар в категорию."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер списка товаров в формате строки."""
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result

    def __str__(self) -> str:
        """Строковое представление категории с общим количеством товаров."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __repr__(self) -> str:
        return f"Category(name={self.name!r}, products_count={len(self.__products)})"


class CategoryIterator:
    """Итератор для перебора товаров категории."""

    def __init__(self, category: Category) -> None:
        self._products = category._Category__products
        self._index = 0

    def __iter__(self) -> 'CategoryIterator':
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


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)

    # Демонстрация работы итератора
    print("\nПеребор товаров через итератор:")
    for product in CategoryIterator(category1):
        print(f"  - {product.name}")