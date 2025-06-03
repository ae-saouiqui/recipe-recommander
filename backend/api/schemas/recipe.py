from pydantic import BaseModel

from typing import List,Optional

class Recipe(BaseModel):

    recipe: str
    country : str
