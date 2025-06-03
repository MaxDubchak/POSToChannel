import random

from channelsAPIs.base import BaseAPI
from exceptions import ValidationException


class UberEatsAPI(BaseAPI):
    @staticmethod
    def validate_menu(menu: dict):
        if not menu.get("sections"):
            raise ValidationException("Each menu must have at least on category in 'sections'")

        for section in menu["sections"]:
            if not section.get("name"):
                raise ValidationException("Each section must have a 'name'")

            if not section.get("items"):
                raise ValidationException(f"Each section must have 'items' (category={section['name']})")

            for sub_item in section["items"]:
                if not sub_item.get("plu"):
                    raise ValidationException(f"Each product must have a 'plu' (category={section['name']})")

                for prop in ["price", "description", "kcal", "name"]:
                    if not sub_item.get(prop):
                        raise ValidationException(
                            f"Each product must have a '{prop}' (category={section['name']}, product={sub_item['name']})"
                        )

        return True

    @staticmethod
    def generate_order(menu: dict):
        order = []
        num_categories_selected = random.randint(1, len(menu["sections"]))
        categories = random.choices(menu["sections"], k=num_categories_selected)
        for category in categories:
            num_items_bought = random.randint(1, len(category["items"]))
            items = random.choices(category["items"], k=num_items_bought)
            for item in items:
                quantity = random.randint(1, 5)
                order.append({"plu": item["plu"], "total_price": item["price"] * quantity, "quantity": quantity})

        return order