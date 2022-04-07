from typing import Dict, Optional
from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get('/')
def home() -> Dict:
    return {'hello': 'world'}


@app.get("/items/{item_id}")
def read_item(item_id: int) -> Dict:
    return {"item_id": item_id}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item) -> Dict:
    return {"item_name": item.name, "item_id": item_id}