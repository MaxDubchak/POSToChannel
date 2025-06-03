import random

from exceptions import ValidationException


class DeliverooAPI:
    @staticmethod
    def validate_menu(menu: dict):
        if not menu.get("categories"):
            raise ValidationException("Each menu must have at least on category in 'categories'")

        for category in menu["categories"]:
            if not category.get("name"):
                raise ValidationException("Each category must have a 'name'")

            if not category.get("sub_products"):
                raise ValidationException(f"Each category must have 'sub_products' (category={category['name']})")

            for sub_item in category["sub_products"]:
                if not sub_item.get("plu"):
                    raise ValidationException(f"Each product must have a 'plu' (category={category['name']})")

                for prop in ["price", "description", "name"]:
                    if not sub_item.get(prop):
                        raise ValidationException(
                            f"Each product must have a '{prop}' (category={category['name']}, product={sub_item['plu']})"
                        )

            if not category["menu_weight"]:
                raise ValidationException(f"Each category must have a 'menu_weight' (category={category['name']})")

        return True

    @staticmethod
    def generate_order(menu: dict):
        order = []
        num_categories_selected = random.randint(1, len(menu["categories"]))
        categories = random.choices(menu["categories"], k=num_categories_selected)
        for category in categories:
            num_items_bought = random.randint(1, len(category["sub_products"]))
            items = random.choices(category["sub_products"], k=num_items_bought)
            for item in items:
                quantity = random.randint(1, 5)
                order.append({"plu": item["plu"], "price": item["price"] * quantity, "quantity": quantity})

        return order