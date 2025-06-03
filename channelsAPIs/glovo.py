import random

from channelsAPIs.base import BaseAPI
from exceptions import ValidationException


class GlovoAPI(BaseAPI):
    @staticmethod
    def validate_menu(menu: dict):
        if not menu.get("categories"):
            raise ValidationException("Each menu must have at least on category in 'categories'")

        for category in menu["categories"]:
            if not category.get("name"):
                raise ValidationException("Each category must have a 'name'")

            if not category.get("products"):
                raise ValidationException(f"Each category must have 'products' (category={category['name']})")

            for sub_item in category["products"]:
                if not sub_item.get("plu"):
                    raise ValidationException(f"Each product must have a 'plu' (category={category['name']})")

                for prop in ["price", "description", "calories", "name"]:
                    if not sub_item.get(prop):
                        raise ValidationException(
                            f"Each product must have a '{prop}' (category={category['name']}, product={sub_item['name']})"
                        )

            if not category.get("menu_weight"):
                raise ValidationException(f"Each category must have a 'menu_weight' (category={category['name']})")

        return True

    @staticmethod
    def generate_order(menu: dict):
        order = []
        num_categories_selected = random.randint(1, len(menu["categories"]))
        categories = random.choices(menu["categories"], k=num_categories_selected)
        for category in categories:
            num_items_bought = random.randint(1, len(category["products"]))
            items = random.choices(category["products"], k=num_items_bought)
            for item in items:
                quantity = random.randint(1, 5)
                order.append({"plu": item["plu"], "price_per_item": item["price"], "number_bought": quantity})

        return order
