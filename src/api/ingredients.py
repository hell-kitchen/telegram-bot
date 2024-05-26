from uplink import Consumer, get, returns, Query

from src.models import Ingredient
from src.settings import settings


class IngredientsClient(Consumer):
    @returns.json()
    @get("api/ingredients")
    def get_ingredients(self, name: Query("name") = None) -> list[Ingredient]:
        pass


cli = IngredientsClient(base_url=settings.base_url)
