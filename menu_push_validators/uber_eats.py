from exceptions import ValidationException


def validate_menu(menu: dict):
    if not menu.get("sections"):
        raise ValidationException("Each menu must have at least on category in 'sections'")

    for section in menu["sections"]:
        if not section.get("name"):
            raise ValidationException("Each section must have a 'name'")

        if not section.get("items"):
            raise ValidationException(f"Each section must have 'items' (category={section['name']})")

        for sub_item in section["items"]:
            if not sub_item.get("name"):
                raise ValidationException(f"Each product must have a 'name' (category={section['name']})")

            for prop in ["price", "description", "kcal"]:
                if not sub_item.get(prop):
                    raise ValidationException(
                        f"Each product must have a '{prop}' (category={section['name']}, product={sub_item['name']})"
                    )

    return True