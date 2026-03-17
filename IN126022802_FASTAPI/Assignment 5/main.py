from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Sample Product Data
# -----------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics"},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics"},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics"},
]

# -----------------------------
# Orders Storage
# -----------------------------
orders = []
order_id_counter = 1

# -----------------------------
# Request Model
# -----------------------------
class OrderRequest(BaseModel):
    customer_name: str
    product_id: int
    quantity: int


# -----------------------------
# Create Order (for testing Q4 & Bonus)
# -----------------------------
@app.post("/orders")
def create_order(data: OrderRequest):
    global order_id_counter

    product = next((p for p in products if p["id"] == data.product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = product["price"] * data.quantity

    order = {
        "order_id": order_id_counter,
        "customer_name": data.customer_name,
        "product": product["name"],
        "quantity": data.quantity,
        "total_price": total_price
    }

    orders.append(order)
    order_id_counter += 1

    return {"message": "Order placed", "order": order}


# =====================================================
# ✅ Q1 — SEARCH PRODUCTS
# =====================================================
@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(results),
        "products": results
    }


# =====================================================
# ✅ Q2 — SORT PRODUCTS
# =====================================================
@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):
    if sort_by not in ["price", "name"]:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be 'price' or 'name'"
        )

    reverse = (order == "desc")

    sorted_products = sorted(
        products,
        key=lambda p: p[sort_by],
        reverse=reverse
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }


# =====================================================
# ✅ Q3 — PAGINATION
# =====================================================
@app.get("/products/page")
def paginate_products(
    page: int = Query(1, ge=1),
    limit: int = Query(2, ge=1)
):
    total = len(products)

    start = (page - 1) * limit
    paginated = products[start:start + limit]

    total_pages = -(-total // limit)

    return {
        "page": page,
        "limit": limit,
        "total_products": total,
        "total_pages": total_pages,
        "products": paginated
    }


# =====================================================
# ✅ Q4 — SEARCH ORDERS
# =====================================================
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    results = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }


# =====================================================
# ✅ Q5 — SORT BY CATEGORY THEN PRICE
# =====================================================
@app.get("/products/sort-by-category")
def sort_by_category():
    result = sorted(
        products,
        key=lambda p: (p["category"], p["price"])
    )

    return {
        "products": result,
        "total": len(result)
    }


# =====================================================
# ✅ Q6 — SEARCH + SORT + PAGINATION
# =====================================================
@app.get("/products/browse")
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20),
):
    result = products

    # 🔍 Step 1: Search
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # ↕ Step 2: Sort
    if sort_by in ["price", "name"]:
        result = sorted(
            result,
            key=lambda p: p[sort_by],
            reverse=(order == "desc")
        )

    # 📄 Step 3: Pagination
    total = len(result)
    start = (page - 1) * limit
    paginated = result[start:start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paginated
    }


# =====================================================
# ⭐ BONUS — PAGINATE ORDERS
# =====================================================
@app.get("/orders/page")
def paginate_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20),
):
    total = len(orders)
    start = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "total_orders": total,
        "total_pages": -(-total // limit),
        "orders": orders[start:start + limit]
    }


# -----------------------------
# GET PRODUCT BY ID (keep last)
# -----------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product