from uplink import Consumer, get, returns, Query
from src.models import Ingredient


class IngredientsClient(Consumer):
    @returns.json()
    @get("api/ingredients")
    def get_ingredients(self, name: Query("name") = None) -> list[Ingredient]:
        pass


cli = IngredientsClient(base_url="https://hellchicken.ru/")

if __name__ == '__main__':
    res = cli.get_ingredients(name='Абрикос')
    # result = map(lambda x: x.name, res)
    # names = [x.name for x in res]
    print(res)