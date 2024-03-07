from uplink import Consumer, get, returns, Query
from src.models import Ingredient


class IngredientsClient(Consumer):
    @returns.json()
    @get("api/ingredients")
    def get_ingredients(self, name: Query("name") = None) -> list[Ingredient]:
        pass


if __name__ == '__main__':
    cli = IngredientsClient(base_url="https://hellchicken.ru/")
    res = cli.get_ingredients(name='Абрикос')
    print(res)