"""Ядро интернет-магазина: классы Product и Category."""

import json
from typing import List


class Product:
    """Товар интернет-магазина."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)

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
        self.products = products

        # Автоматическое обновление счетчиков при инициализации
        Category.category_count += 1
        Category.product_count += len(self.products)

    def __repr__(self) -> str:
        return f"Category(name={self.name!r}, products_count={len(self.products)})"


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
