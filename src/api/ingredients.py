from uplink import Consumer, get, returns, Query
from src.models import Ingredient


class IngredientsClient(Consumer):
    @returns.json()
    @get("api/ingredients")
    def get_ingredients(self, name: Query("name") = None) -> list[Ingredient]:
        pass


cli = IngredientsClient(base_url="https://hellchicken.ru/")
