"""Ядро интернет-магазина: классы Product, Smartphone, LawnGrass и Category."""

import json
from typing import List, Optional


class Product:
    """Базовый класс товара интернет-магазина."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
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
            f"{self.__class__.__name__}(name={self.name!r}, price={self.price}, quantity={self.quantity})"
        )

    def __add__(self, other: 'Product') -> float:
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
        color: str
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        return f"{self.name} ({self.model}), {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return (
            f"Smartphone(name={self.name!r}, model={self.model!r}, "
            f"price={self.price}, quantity={self.quantity})"
        )


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
        color: str
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return (
            f"LawnGrass(name={self.name!r}, country={self.country!r}, "
            f"price={self.price}, quantity={self.quantity})"
        )


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


if __name__ == '__main__':
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                         "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print(smartphone1.name)
    print(smartphone1.description)
    print(smartphone1.price)
    print(smartphone1.quantity)
    print(smartphone1.efficiency)
    print(smartphone1.model)
    print(smartphone1.memory)
    print(smartphone1.color)

    print(smartphone2.name)
    print(smartphone2.description)
    print(smartphone2.price)
    print(smartphone2.quantity)
    print(smartphone2.efficiency)
    print(smartphone2.model)
    print(smartphone2.memory)
    print(smartphone2.color)

    print(smartphone3.name)
    print(smartphone3.description)
    print(smartphone3.price)
    print(smartphone3.quantity)
    print(smartphone3.efficiency)
    print(smartphone3.model)
    print(smartphone3.memory)
    print(smartphone3.color)

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print(grass1.name)
    print(grass1.description)
    print(grass1.price)
    print(grass1.quantity)
    print(grass1.country)
    print(grass1.germination_period)
    print(grass1.color)

    print(grass2.name)
    print(grass2.description)
    print(grass2.price)
    print(grass2.quantity)
    print(grass2.country)
    print(grass2.germination_period)
    print(grass2.color)

    smartphone_sum = smartphone1 + smartphone2
    print(smartphone_sum)

    grass_sum = grass1 + grass2
    print(grass_sum)

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError:
        print("Возникла ошибка TypeError при попытке сложения")
    else:
        print("Не возникла ошибка TypeError при попытке сложения")

    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])

    category_smartphones.add_product(smartphone3)

    print(category_smartphones.products)

    print(Category.product_count)

    try:
        category_smartphones.add_product("Not a product")
    except TypeError:
        print("Возникла ошибка TypeError при добавлении не продукта")
    else:
        print("Не возникла ошибка TypeError при добавлении не продукта")