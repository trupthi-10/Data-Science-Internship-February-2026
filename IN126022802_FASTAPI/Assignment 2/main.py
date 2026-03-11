from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List
from collections import defaultdict

app = FastAPI()

# -------------------------
# PRODUCTS DATABASE
# -------------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]

# -------------------------
# DAY 1 ENDPOINTS
# -------------------------

@app.get("/")
def home():
    return {"message": "FastAPI Store API Running"}

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    result = [p for p in products if p["category"].lower() == category_name.lower()]
    if not result:
        return {"error": "No products found in this category"}
    return {"category": category_name, "products": result, "total": len(result)}

@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p["in_stock"]]
    return {"in_stock_products": available, "count": len(available)}

@app.get("/store/summary")
def store_summary():
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }

@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    results = [p for p in products if keyword.lower() in p["name"].lower()]
    if not results:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }

@app.get("/products/deals")
def get_deals():
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])
    return {"best_deal": cheapest, "premium_pick": expensive}

# -------------------------
# DAY 2 TASK 1
# FILTER WITH QUERY PARAMS
# -------------------------

@app.get("/products/filter")
def filter_products(min_price: int = None, max_price: int = None, category: str = None):

    result = products

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]

    return {"filtered_products": result, "total": len(result)}

# -------------------------
# DAY 2 TASK 2
# PRICE ONLY ENDPOINT
# -------------------------

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return {"name": p["name"], "price": p["price"]}

    return {"error": "Product not found"}

# -------------------------
# DAY 2 TASK 3
# CUSTOMER FEEDBACK
# -------------------------

feedback = []

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    feedback.append(data)

    return {
        "message": "Feedback submitted successfully",
        "feedback": data,
        "total_feedback": len(feedback)
    }

# -------------------------
# DAY 2 TASK 4
# PRODUCT DASHBOARD
# -------------------------

@app.get("/products/summary")
def product_summary():

    total_products = len(products)
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = total_products - in_stock_count

    most_expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])

    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {"name": most_expensive["name"], "price": most_expensive["price"]},
        "cheapest": {"name": cheapest["name"], "price": cheapest["price"]},
        "categories": categories
    }

# -------------------------
# DAY 2 TASK 5
# BULK ORDER SYSTEM
# -------------------------

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
            continue

        if not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# -------------------------
# BONUS ORDER TRACKING
# -------------------------

orders = []
order_counter = 1

class SimpleOrder(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders")
def create_order(order: SimpleOrder):

    global order_counter

    new_order = {
        "order_id": order_counter,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending"
    }

    orders.append(new_order)
    order_counter += 1

    return new_order

@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for o in orders:
        if o["order_id"] == order_id:
            return o

    return {"error": "Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for o in orders:
        if o["order_id"] == order_id:
            o["status"] = "confirmed"
            return {"message": "Order confirmed", "order": o}

    return {"error": "Order not found"}