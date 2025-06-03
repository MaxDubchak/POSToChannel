from abc import ABC, abstractmethod


class BaseAPI(ABC):
    @staticmethod
    @abstractmethod
    def validate_menu(menu: dict) -> bool:
        ...

    @staticmethod
    @abstractmethod
    def generate_order(menu: dict) -> list[dict]:
        ...