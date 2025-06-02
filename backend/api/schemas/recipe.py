from pydantic import BaseModel

from typing import List

class Recipe(BaseModel):

    recipe: List[str]