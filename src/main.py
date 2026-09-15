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
        # Проверка дубликатов
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

    def __repr__(self) -> str:
        return (
            f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"
        )


class Category:
    """Категория товаров.

    Класс-атрибуты:
        category_count — общее количество созданных категорий.
        product_count  — суммарное количество товаров во всех созданных категориях.
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = list(products)  # Приватный атрибут списка товаров

        # Автоматическое обновление счетчиков при инициализации
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
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result



def load_products_from_json(file_path: str) -> List[Category]:
    """Загружает категории и товары из JSON-файла и создает объекты классов."""
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
    # Пример локального запуска
    p1 = Product("Смартфон", "Хороший телефон", 50000.0, 10)
    cat1 = Category("Электроника", "Гаджеты", [p1])
    print(f"Категорий: {Category.category_count}, Товаров: {Category.product_count}")

    # Тест добавления товара
    p2 = Product("Ноутбук", "Мощный ноут", 100000.0, 5)
    cat1.add_product(p2)
    print(cat1.get_products_string())

    # Тест класс-метода
    new_p = Product.new_product({
        "name": "Планшет",
        "description": "Большой экран",
        "price": 30000.0,
        "quantity": 7
    })
    print(new_p)