from datetime import datetime
from pydantic import BaseModel

class Order(BaseModel):
    id: str
    date: datetime
    inventory_id: str
    product_id: str
    count: int
    status: str
