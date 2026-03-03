from core.models import User, CustomerDetails, Product, Order, OrderItem
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from core.models import User, Order
from sqlalchemy import asc, desc
from typing import Optional
from sqlalchemy import func

def get_filtered_users(db: Session, search: str = None, min_orders: int = 0):
    # שאילתה בסיסית שמחברת משתמשים והזמנות ומחשבת כמות
    query = db.query(
        User, 
        func.count(Order.id).label("order_count")
    ).outerjoin(Order).group_by(User.id)
    
    # פילטור לפי שם (אם הוזן)
    if search:
        query = query.filter(User.username.contains(search))
    
    # פילטור לפי כמות הזמנות מינימלית (HAVING כי זה aggregation)
    if min_orders > 0:
        query = query.having(func.count(Order.id) >= min_orders)
    
    # מיון לפי כמות ההזמנות מהגבוה לנמוך
    query = query.order_by(func.count(Order.id).desc())
    
    return query.all()

def get_users_with_stats(db: Session, search_name: str = None):
    query = db.query(
        User, 
        func.count(Order.id).label("order_count")
    ).outerjoin(Order).group_by(User.id)
    
    if search_name:
        query = query.filter(User.username.contains(search_name))
    
    return query.all()

# ==========================================
# 1. CORE CRUD OPERATIONS (Users as Example)
# ==========================================

def create_user(db: Session, username: str, email: str):
    """Create a new user with error handling for duplicates."""
    try:
        new_user = User(username=username, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user, None  # Return the user and None for error
    except IntegrityError:
        db.rollback() # Cancel the transaction if unique constraint fails
        return None, "Username or email already exists in the system."
    except Exception as e:
        db.rollback()
        return None, f"An unexpected error occurred: {str(e)}"  

def get_all_users(db: Session):
    """Retrieve all users."""
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    """Retrieve a single user by their ID."""
    return db.query(User).filter(User.id == user_id).first()

def update_user_email(db: Session, user_id: int, new_email: str):
    """Update a user's email with error handling."""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None, "User not found."
            
        user.email = new_email
        db.commit()
        db.refresh(user)
        return user, None
    except IntegrityError:
        db.rollback()
        return None, "This email is already in use by another user."

def delete_user(db: Session, user_id: int):
    """Delete a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

# ==========================================
# 2. BUSINESS QUESTIONS (Project Requirement)
# ==========================================

def bq1_get_user_with_details(db: Session, user_id: int):
    """
    Business Question 1: Show entity with its related 1:1 details using JOIN.
    Fetches a user and their customer details simultaneously.
    """
    result = db.query(User, CustomerDetails).join(
        CustomerDetails, User.id == CustomerDetails.user_id
    ).filter(User.id == user_id).first()
    
    return result

def bq2_get_order_with_products(db: Session, order_id: int):
    # מצטרפים ל-OrderItem ול-Product כדי לשלוף הכל במכה
    return db.query(Order, Product, OrderItem.quantity).join(
        OrderItem, Order.id == OrderItem.order_id
    ).join(
        Product, OrderItem.product_id == Product.id
    ).filter(Order.id == order_id).all()

def bq3_count_orders_per_user(db: Session):
    """
    Business Question 3: Count per category using JOIN + GROUP BY.
    Counts how many orders each user has placed.
    """
    results = db.query(
        User.username, 
        func.count(Order.id).label('total_orders')
    ).join(
        Order, User.id == Order.user_id
    ).group_by(User.username).all()
    
    return results

def bq4_calculate_order_total(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).all()
    if not order:
        return None
    
    # וודא שכאן כתוב order_items (לפי המודל שלך)
    total = sum(item.quantity * item.product.price for item in order.order_items)
    
    return {
        "id": order.id,
        "username": order.user.username,
        "total_revenue": total
    }

def bq5_get_expensive_products(db: Session, min_price: float):
    # כאן הלוגיקה הספציפית של BQ5
    return db.query(Product).filter(Product.price >= min_price).all()

def get_filtered_products(db: Session, min_price: float, search_term: Optional[str], sort_order: Optional[str]):
    print(f"DEBUG: Filtering with: Price={min_price}, Search='{search_term}', Sort='{sort_order}'") # <--- הוסף את זה

    query = db.query(Product).filter(Product.price >= min_price)
    
    if search_term:
        query = query.filter(Product.name.ilike(f"%{search_term}%"))

    if sort_order == "asc":
        query = query.order_by(asc(Product.price))
    elif sort_order == "desc":
        query = query.order_by(desc(Product.price))
    
    return query.all()