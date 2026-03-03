from fastapi import FastAPI, Depends, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from typing import List

# Import our local modules
from core.db import get_db_fastapi
import core.schemas as schemas
import logic.crud as crud
from core.models import Product
import os

# Initialize FastAPI with metadata
app = FastAPI(
    title="Pro Store Dashboard",
    description="Full Web Interface and REST API for Store Management"
)

# Setup templates directory for HTML rendering
current_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# ==========================================
# WEB INTERFACE ROUTES (HTML)
# ==========================================

# --- Welcome / Home Page ---
@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    """Renders the main landing page of the application."""
    return templates.TemplateResponse("home.html", {"request": request})

# --- Product Catalog (Moved from / to /products-catalog) ---
@app.get("/products-catalog", response_class=HTMLResponse)
def products_catalog(
    request: Request,
    min_price: float = 0,
    search_term: Optional[str] = None,
    sort_order: Optional[str] = None,
    db: Session = Depends(get_db_fastapi)
):
    """Renders the product catalog with filtering."""
    products = crud.get_filtered_products(db, min_price, search_term, sort_order)
    print(f"DEBUG: I am sending {len(products)} products to the template.")

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "products": products, 
        "min_price": min_price,
        "search_term": search_term,
        "sort_order": sort_order
    })

@app.get("/product/{product_id}")
def product_details(request: Request, product_id: int, db: Session = Depends(get_db_fastapi)):
    # שליפת מוצר בודד מה-DB
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        # כאן אפשר להוסיף טיפול בשגיאה אם המוצר לא קיים
        return {"error": "Product not found"}
        
    return templates.TemplateResponse("product_details.html", {
        "request": request,
        "product": product
    })

@app.get("/manage-users", response_class=HTMLResponse)
def web_list_users(
    request: Request, 
    search: str = None, 
    min_orders: int = 0, 
    db: Session = Depends(get_db_fastapi)
):
    # הפעלת הפונקציה עם כל הפרמטרים
    users_data = crud.get_filtered_users(db, search=search, min_orders=min_orders)
    
    return templates.TemplateResponse("users.html", {
        "request": request, 
        "users_data": users_data,
        "search_query": search or "",
        "min_orders": min_orders
    })

@app.get("/analytics", response_class=HTMLResponse)
def analytics_page(request: Request, db: Session = Depends(get_db_fastapi)):
    """
    Renders the Business Intelligence page using complex JOIN queries.
    """
    # BQ3: Get orders per user
    orders_per_user = crud.bq3_count_orders_per_user(db)
    
    # BQ4: Get revenue for all orders (Modified to show all)
    # Note: You can loop through order IDs or adjust crud.py to return all
    from core.models import Order
    order_ids = [o.id for o in db.query(Order).all()]
    revenue_stats = [crud.bq4_calculate_order_total(db, oid) for oid in order_ids if crud.bq4_calculate_order_total(db, oid)]
    
    # BQ1: Get users with their shipping details
    from core.models import User
    users_with_details = [crud.bq1_get_user_with_details(db, u.id) for u in db.query(User).all() if crud.bq1_get_user_with_details(db, u.id)]

    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "orders_per_user": orders_per_user,
        "revenue_stats": revenue_stats,
        "users_with_details": users_with_details
    })

@app.get("/business-queries", response_class=HTMLResponse)
def business_queries_page(
    request: Request, 
    q_id: int = None, 
    order_id: int = None, 
    min_price: float = 20.0,
    db: Session = Depends(get_db_fastapi)
):
    results = None
    query_title = ""
    description = ""

    if q_id == 1:
        query_title = "User & Shipping Details (1:1 JOIN)"
        description = "Connecting Users table with CustomerDetails to see shipping addresses."
        from core.models import User
        results = [crud.bq1_get_user_with_details(db, u.id) for u in db.query(User).all() if crud.bq1_get_user_with_details(db, u.id)]
    
    elif q_id == 2:
        query_title = "Order Content (N:M)"
        # משתמש ב-order_id שמגיע מה-URL, ואם אין - ברירת מחדל 1
        current_order = order_id if order_id else 1
        results = crud.bq2_get_order_with_products(db, order_id=current_order)

    elif q_id == 3:
        query_title = "Orders Per User (GROUP BY + COUNT)"
        description = "Calculating how many orders each user has placed."
        results = crud.bq3_count_orders_per_user(db)
        
    elif q_id == 4:
        query_title = "Order Revenue Calculation (SUM + JOIN)"
        description = "Calculating the total price for a specific order."
        if order_id:
            results = crud.bq4_calculate_order_total(db, order_id)
        
    elif q_id == 5:
        query_title = "High-Value Products (FILTER + SORT)"
        description = f"Showing products more expensive than ${min_price}."
        results = crud.bq5_get_expensive_products(db, min_price)

    return templates.TemplateResponse("queries.html", {
        "request": request,
        "q_id": q_id,
        "query_title": query_title,
        "description": description,
        "results": results,
        "order_id": order_id,
        "min_price": min_price
    })

@app.post("/manage-users/add")
def web_create_user(
    username: str = Form(...), 
    email: str = Form(...), 
    db: Session = Depends(get_db_fastapi)
):
    """
    Action: Handles the form submission to create a new user.
    """
    new_user, error = crud.create_user(db, username, email)
    if error:
        # In a real app, we would pass this error back to the UI
        return HTMLResponse(content=f"<h1>Error: {error}</h1><a href='/manage-users'>Back</a>", status_code=400)
    
    return RedirectResponse(url="/manage-users", status_code=303)

@app.post("/manage-users/delete/{user_id}")
def web_delete_user(user_id: int, db: Session = Depends(get_db_fastapi)):
    """
    Action: Handles user deletion from the web interface.
    """
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return RedirectResponse(url="/manage-users", status_code=303)

# ==========================================
# REST API ENDPOINTS (JSON)
# ==========================================

@app.get("/api/products", response_model=List[schemas.ProductResponse], tags=["API"])
def get_products_api(db: Session = Depends(get_db_fastapi)):
    """API endpoint to get all products."""
    return db.query(Product).all()

@app.get("/api/users", response_model=List[schemas.UserResponse], tags=["API"])
def get_users_api(db: Session = Depends(get_db_fastapi)):
    """API endpoint to get all users."""
    return crud.get_all_users(db)

@app.post("/api/users", response_model=schemas.UserResponse, tags=["API"])
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db_fastapi)):
    """API endpoint to create a user."""
    new_user, error = crud.create_user(db, user.username, user.email)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_user

@app.put("/api/users/{user_id}", response_model=schemas.UserResponse, tags=["API"])
def update_user_api(user_id: int, email_data: schemas.UserUpdate, db: Session = Depends(get_db_fastapi)):
    """API endpoint to update user email."""
    updated_user, error = crud.update_user_email(db, user_id, email_data.email)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return updated_user

@app.delete("/api/users/{user_id}", tags=["API"])
def delete_user_api(user_id: int, db: Session = Depends(get_db_fastapi)):
    """API endpoint to delete a user."""
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted successfully"}