from pydantic import BaseModel


from typing import List,Optional


class Product(BaseModel):
    id: int
    additives: int
    categories: Optional[List[str]] = None
    image_url: Optional[str] = None
    ecoscore: Optional[str] = None
    nutriscore_grade: Optional[str] = None
    nova_group: Optional[int] = None  
    allergens:Optional[str] = None
    product_name:Optional[str] =None
    ingredients_tags:Optional[List[str]]=None

