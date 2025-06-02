from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
from typing import List, Optional, Dict, Union
from entities import *
from operations import *
import time

app = FastAPI(
    title="Торговый центр API", 
    description="Полный API для управления торговым центром",
    version="1.0.0"
)

mall = ShoppingMall("МегаVМолл API", "ул. Центральная, 123")

# Pydantic модели
class CustomerModel(BaseModel):
    name: str
    contact_info: str
    balance: float
    purchases: List[Dict] = []

class ProductModel(BaseModel):
    name: str
    price: float
    quantity: int
    category: str
    specifications: Dict[str, str] = {}

class ShopModel(BaseModel):
    name: str
    category: str
    area: float
    rent_price: float
    return_policy_days: int
    products: List[ProductModel] = []
    sellers: List[Dict] = []

class SellerModel(BaseModel):
    name: str
    position: str
    rating: float

class PurchaseRequest(BaseModel):
    customer_name: str
    product_name: str
    quantity: int
    seller_name: Optional[str] = None

class ReturnRequest(BaseModel):
    customer_name: str
    purchase_index: int

class PromotionModel(BaseModel):
    name: str
    description: str
    discount: float

class RentRequest(BaseModel):
    shop_name: str
    category: str
    area: float
    months: int

class RatingRequest(BaseModel):
    seller_name: str
    rating: int
    purchase_index: int

class AnnouncementRequest(BaseModel):
    message: str

customers_db = {}
current_customer = None

def find_customer(name: str) -> Customer:
    if name not in customers_db:
        raise HTTPException(status_code=404, detail="Покупатель не найден")
    return customers_db[name]

def find_product(name: str) -> tuple[Product, Shop]:
    results = ProductSearch.search_by_name(mall, name)
    if not results:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return results[0]

# Роутеры
@app.post("/customers/", response_model=CustomerModel)
def create_customer(name: str, contact_info: str, initial_balance: float = 0):
    """Создать нового покупателя"""
    if name in customers_db:
        raise HTTPException(status_code=400, detail="Покупатель уже существует")
    
    customer = Customer(name, contact_info)
    customer.add_funds(initial_balance)
    customers_db[name] = customer
    return customer

@app.get("/customers/current", response_model=CustomerModel)
def get_current_customer():
    """Получить текущего покупателя"""
    if not current_customer:
        raise HTTPException(status_code=404, detail="Текущий покупатель не установлен")
    return current_customer

@app.post("/customers/current")
def set_current_customer(name: str):
    """Установить текущего покупателя"""
    global current_customer
    current_customer = find_customer(name)
    return {"message": f"Текущий покупатель установлен: {name}"}

@app.get("/shops/", response_model=List[ShopModel])
def list_shops():
    """Получить список всех магазинов с полной информацией"""
    return mall.shops

@app.get("/products/", response_model=List[ProductModel])
def list_products(shop_name: Optional[str] = None):
    """Получить список товаров (опционально фильтр по магазину)"""
    if shop_name:
        shop = next((s for s in mall.shops if s.name == shop_name), None)
        if not shop:
            raise HTTPException(status_code=404, detail="Магазин не найден")
        return shop.products
    return [product for shop in mall.shops for product in shop.products]

@app.post("/purchases/", response_model=Dict)
def make_purchase(request: PurchaseRequest):
    """Совершить покупку"""
    customer = find_customer(request.customer_name)
    product, shop = find_product(request.product_name)
    
    seller = None
    if request.seller_name:
        seller = next((s for s in shop.sellers if s.name == request.seller_name), None)
    
    success, message, purchase_record = PurchaseOperation.make_purchase(
        customer, product, shop, request.quantity, seller
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "message": message,
        "balance": customer.balance,
        "purchase": purchase_record
    }

@app.post("/returns/", response_model=Dict)
def process_return(request: ReturnRequest):
    """Обработать возврат товара"""
    customer = find_customer(request.customer_name)
    success, message = ReturnOperation.return_product(customer, request.purchase_index)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "message": message,
        "balance": customer.balance,
        "remaining_purchases": len(customer.purchases)
    }

@app.get("/promotions/", response_model=List[PromotionModel])
def list_promotions():
    """Получить список всех акций"""
    return mall.promotions

@app.post("/promotions/apply/", response_model=Dict)
def apply_promotion(customer_name: str, promotion_name: str, purchase_index: int):
    """Применить акцию к покупке"""
    customer = find_customer(customer_name)
    promotion = next((p for p in mall.promotions if p.name == promotion_name), None)
    
    if not promotion:
        raise HTTPException(status_code=404, detail="Акция не найдена")
    
    if purchase_index < 0 or purchase_index >= len(customer.purchases):
        raise HTTPException(status_code=400, detail="Неверный индекс покупки")
    
    purchase = customer.purchases[purchase_index]
    updated_purchase = PromotionOperation.apply_promotion(purchase, promotion)
    
    return {
        "message": f"Акция '{promotion.name}' применена",
        "new_price": updated_purchase['total_price']
    }

@app.post("/rent/", response_model=Dict)
def rent_space(request: RentRequest):
    """Арендовать торговое пространство"""
    new_shop = Shop(request.shop_name, request.category, request.area, request.area * 500)
    rent_info = RentOperation.rent_space(mall, new_shop, request.months)
    mall.add_shop(new_shop)
    
    return {
        "message": "Аренда оформлена",
        "rent_info": rent_info,
        "shop": new_shop.name
    }

@app.post("/ratings/", response_model=Dict)
def rate_seller(request: RatingRequest):
    """Оценить продавца"""
    customer = find_customer(request.customer_name)
    
    if request.purchase_index < 0 or request.purchase_index >= len(customer.purchases):
        raise HTTPException(status_code=400, detail="Неверный индекс покупки")
    
    purchase = customer.purchases[request.purchase_index]
    seller_name = purchase.get('seller')
    
    if not seller_name:
        raise HTTPException(status_code=400, detail="В этой покупке нет информации о продавце")
    
    seller = None
    for shop in mall.shops:
        seller = next((s for s in shop.sellers if s.name == seller_name), None)
        if seller:
            break
    
    if not seller:
        raise HTTPException(status_code=404, detail="Продавец не найден")
    
    success, message = ServiceRating.rate_seller(seller, request.rating)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "message": message,
        "seller": seller.name,
        "new_rating": seller.rating
    }

@app.post("/announcements/", response_model=Dict)
def send_announcement(request: AnnouncementRequest):
    """Отправить оповещение"""
    return {
        "message": "Оповещение отправлено",
        "content": request.message
    }

@app.get("/product_details/", response_model=Dict)
def get_product_details(product_name: str):
    """Получить детальную информацию о товаре"""
    product, shop = find_product(product_name)
    
    response = {
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "category": product.category,
        "shop": shop.name,
        "specifications": product.specifications
    }
    
    if product.category == "Бытовая техника":
        response["standard_specs"] = {
            "Гарантия": "2 года",
            "Страна производства": "зависит от модели"
        }
        if "стиральная" in product.name.lower():
            response["standard_specs"].update({
                "Количество оборотов": "1200 об/мин",
                "Режимы стирки": "хлопок, синтетика, деликатная"
            })
        elif "холодильник" in product.name.lower():
            response["standard_specs"].update({
                "Объем": "300 л",
                "Класс энергопотребления": "A++"
            })
    
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)