from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# a different application is allowed to call our FastAPI app, only if it is coming from these urls
origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
        
# using pydantic
class Product(BaseModel):
    id: int
    name: str
    category: str 
    description: str 
    price: float 
    
    # def __init__(self, id, name, category, description, price):
    #     self.id = id
    #     self.name = name 
    #     self.category = category 
    #     self.description = description 
    #     self.price = price
        
class ProductRequest(BaseModel): 
    id: Optional[int] = None # TODO how to get an id included in a create
    name: str = Field(min_length=1) 
    category: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0) # price must be greater than 0
    
    class Config:
        from_attributes = True
        ## this auto fills in the fastAPI endpoint for posting
        # json_schema_extra = {
        #     'example': {
        #         'name': 'Innovative Widget',
        #         'category': 'Widgets',
        #         'description': 'An innovative widget that solves all your widget needs',
        #         'price': 19.99,
        #     }
        # }
        
# example products list
PRODUCTS = [
    Product(1, 'Widget Pro', 'Widgets', 'A high-quality widget', 29.99),
    Product(2, 'Gadget Max', 'Gadgets', 'A versatile gadget for all your needs', 49.99),
]

#  create a product
@app.post('/products/', status_code=status.HTTP_201_CREATED)
async def create_product(product_request: ProductRequest):
    new_product = Product(**product_request.model_dump())
    PRODUCTS.append(new_product)
    return new_product

# read all products
@app.get('/products/', status_code=status.HTTP_200_OK)
async def read_all_products():
    return PRODUCTS

# Read a product by ID
@app.get('/products/{product_id}', status_code=status.HTTP_200_OK)
async def read_product(product_id: int = Path(gt=0)):
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

# update a product
@app.put('/products/{product_id}', status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product_request: ProductRequest):
    for i, product in enumerate(PRODUCTS):
        if product.id == product_id:
            updated_product = Product(id=product_id, **product_request.model_dump())
            PRODUCTS[i] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

#  delete a product
@app.put('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    for i, product in enumerate(PRODUCTS):
        if product.id == product_id:
            PRODUCTS.pop(i)
            return 
    raise HTTPException(status_code=404, detail="Product not found")
