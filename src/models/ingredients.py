from pydantic import BaseModel


class Ingredient(BaseModel):
    id: str
    name: str
    measurement_unit: str

    def __str__(self):
        return "Ingredient(id=%s, name=%s, measurement_unit=%s)" % (
            self.id,
            self.name,
            self.measurement_unit,
        )
