from fastapi import FastAPI, HTTPException
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# Mock product database
products = [{
    "id": i + 1,
    "name": f"Product {i + 1}",
    "description": f"Description for product {i + 1}",
    "price": (i + 1) * 10,
} for i in range(50)]

class Product(BaseModel):
    name: str
    description: str
    price: float

# API to list all products with pagination
@app.get("/product/list")
def list_products(page: int = 1, limit: int = 10):
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_products = products[start_index:end_index]
    return {
        "page": page,
        "totalPages": len(products) // limit + (1 if len(products) % limit > 0 else 0),
        "products": paginated_products,
    }

# API to get product info by ID
@app.get("/product/{pid}/info")
def get_product_info(pid: int):
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# API to add a new product
@app.post("/product/add")
def add_product(product: Product):
    new_id = max(p["id"] for p in products) + 1 if products else 1
    new_product = {"id": new_id, **product.dict()}
    products.append(new_product)
    return {"message": "Product added successfully", "product": new_product}

# API to update an existing product by ID
@app.put("/product/{pid}/update")
def update_product(pid: int, updated_product: Product):
    for product in products:
        if product["id"] == pid:
            product.update(updated_product.dict())
            return {"message": "Product updated successfully", "product": product}
    raise HTTPException(status_code=404, detail="Product not found")
