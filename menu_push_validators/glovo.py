from exceptions import ValidationException


def validate_menu(menu: dict):
    if not menu.get("categories"):
        raise ValidationException("Each menu must have at least on category in 'categories'")

    for category in menu["categories"]:
        if not category.get("name"):
            raise ValidationException("Each category must have a 'name'")

        if not category.get("products"):
            raise ValidationException(f"Each category must have 'products' (category={category['name']})")

        for sub_item in category["products"]:
            if not sub_item.get("name"):
                raise ValidationException(f"Each product must have a 'name' (category={category['name']})")

            for prop in ["price", "description", "calories"]:
                if not sub_item.get(prop):
                    raise ValidationException(
                        f"Each product must have a '{prop}' (category={category['name']}, product={sub_item['name']})"
                    )

        if not category.get("menu_weight"):
            raise ValidationException(f"Each category must have a 'menu_weight' (category={category['name']})")

    return True