from pydantic import BaseModel


class Ingredient(BaseModel):
    id: int
    name: str
    measurement_unit: str

    def __str__(self):
        return "Ingredient(id=%d, name=%s, measurement_unit=%s)" % (
            self.id,
            self.name,
            self.measurement_unit,
        )
