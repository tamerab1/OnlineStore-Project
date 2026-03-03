import random
from datetime import datetime
from sqlalchemy import text # חשוב לאיפוס המונים
from core.db import get_db_session
from core.models import User, CustomerDetails, Product, Order, OrderItem

def seed_data():
    print("Starting fresh seed...")
    
    with get_db_session() as db:
        try:
            print("Resetting database and IDs...")
            # הפקודה הזו מוחקת הכל ומאפסת את ה-ID ל-1
            db.execute(text("TRUNCATE TABLE order_items, orders, customer_details, products, users RESTART IDENTITY CASCADE;"))
            db.commit()

            print("Inserting new players (Starting from ID 1)...")
            
            # 1. משתמשים
            users = [
                User(username="tamer_pro", email="tamer@example.com"),  # ID: 1
                User(username="john_doe", email="john@example.com"),    # ID: 2
                User(username="sarah_dev", email="sarah@example.com"),  # ID: 3
                User(username="MangoIl", email="mango@example.com"),    # ID: 4
                User(username="jeseb2", email="Evan@example.com"),      # ID: 5
                User(username="Miki3", email="miki@hotmail.com")        # ID: 6

            ]
            db.add_all(users)
            db.commit() 

            # 2. User Details (1:1)
            details = [
                CustomerDetails(user_id=1, full_name="Tamer Pro", shipping_address="Haifa, Israel", phone_number="050-1111111"),
                CustomerDetails(user_id=2, full_name="John Doe", shipping_address="New York, USA", phone_number="1-555-999"),
                CustomerDetails(user_id=3, full_name="Sarah Ex", shipping_address="Tel Aviv, Israel", phone_number="1-555-222"),
                CustomerDetails(user_id=4, full_name="Mango Lolo", shipping_address="Tokyo, Japan", phone_number="2-6665-140"),
                CustomerDetails(user_id=5, full_name="Jese Rodri", shipping_address="Madrid, Spain", phone_number="77-4523-55"),
                CustomerDetails(user_id=6, full_name="Miki Roj'o", shipping_address="Roma, Italy", phone_number="992-9843-445")
            ]
            db.add_all(details)

            # 3. Products
            products = [
                Product(name="Gaming Laptop", price=3500.0, description="RTX 5080 Performance"), # ID: 1
                Product(name="Gaming Mouse", price=25.0, description="Wireless RGB"),            # ID: 2
                Product(name="Mechanical Keyboard", price=40.0, description="Blue Switches"),    # ID: 3
                Product(name="Television", price=650.0, description="Normal Tv"),                # ID: 4
                Product(name="Smart Television", price=1300.0, description="Smart Tv"),          # ID: 5
                Product(name="Iphone 4", price=3000.0, description="Rare Iphone"),               # ID: 6
                Product(name="Iphone 17 Pro", price=1250.0, description="Newest Iphone"),        # ID: 7
                Product(name="Airpods 3", price=135.0, description="For The Best Sound")         # ID:8
                
            ]
            db.add_all(products)
            db.commit()

            # 4. הזמנות (1:N)
            orders = [
                Order(user_id=1, status="Delivered"),
                Order(user_id=2, status="Pending"),
                Order(user_id=3, status="Delivered"),
                Order(user_id=4, status="Pending"),
                Order(user_id=1, status="Pending"),
                Order(user_id=2, status="Shipped"),
                Order(user_id=5, status="Shipped")
            ]
            db.add_all(orders)
            db.commit()

            # 5. פריטים (N:M)
            items = [
                OrderItem(order_id=1, product_id=1, quantity=1),
                OrderItem(order_id=1, product_id=2, quantity=1),
                OrderItem(order_id=2, product_id=3, quantity=2),
                OrderItem(order_id=3, product_id=5, quantity=2),
                OrderItem(order_id=4, product_id=4, quantity=4),
                OrderItem(order_id=7, product_id=3, quantity=1)
            ]
            db.add_all(items)
            db.commit()

            print("✅ Database Seeded Successfully! IDs reset to 1.")

        except Exception as e:
            db.rollback()
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    seed_data()