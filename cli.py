import sys
from core.db import get_db_session
import logic.crud as crud

# ==========================================
# CLI APPLICATION
# ==========================================
def print_main_menu():
    """Print the main CLI menu structure."""
    print("\n" + "="*45)
    print("       ONLINE STORE MANAGEMENT SYSTEM")
    print("="*45)
    print("1. View All Users (Read)")
    print("2. Add New User (Create)")
    print("3. Update User Email (Update)")
    print("4. Delete User (Delete)")
    print("5. Business Questions Menu")
    print("6. Exit")
    print("="*45)

def business_questions_menu():
    """Dedicated section for all 5 business queries."""
    while True:
        print("\n" + "-"*45)
        print("           BUSINESS QUESTIONS")
        print("-" * 45)
        print("1. Get User with Customer Details (1:1 JOIN)")
        print("2. Get Order with its Products (N:M JOIN)")
        print("3. Count Orders Per User (JOIN + GROUP BY)")
        print("4. Calculate Order Total Revenue (JOIN + GROUP BY)")
        print("5. Filter Expensive Products (Filter + Sort)")
        print("6. Return to Main Menu")
        
        choice = input("\nSelect an option (1-6): ")
        
        with get_db_session() as db:
            if choice == '1':
                user_id = input("Enter User ID to search: ")
                if user_id.isdigit(): 
                    result = crud.bq1_get_user_with_details(db, int(user_id))
                    if result:
                        user, details = result
                        print(f"\n[RESULT] User: {user.username} | Address: {details.shipping_address}")
                    else:
                        print("\n[ERROR] User not found or has no details.")
                else:
                    print("\n[ERROR] Invalid ID. Numbers only.")
                    
            elif choice == '2':
                order_id = input("Enter Order ID to view its products: ")
                if order_id.isdigit():
                    results = crud.bq2_get_order_with_products(db, int(order_id))
                    if results:
                        print(f"\n[RESULT] Products in Order #{order_id}:")
                        for order, product, quantity in results:
                            print(f"- {product.name} (Qty: {quantity})")
                    else:
                        print("\n[ERROR] Order not found or is empty.")
                else:
                    print("\n[ERROR] Invalid ID.")

            elif choice == '3':
                results = crud.bq3_count_orders_per_user(db)
                print("\n[RESULT] Orders per user:")
                for username, count in results:
                    print(f"- {username}: {count} total orders")
            
            elif choice == '4':
                order_id = input("Enter Order ID to calculate total revenue: ")
                if order_id.isdigit():
                    result = crud.bq4_calculate_order_total(db, int(order_id))
                    if result:
                        print(f"\n[RESULT] Total revenue for Order #{result.id}: ${result.total_revenue:.2f}")
                    else:
                        print("\n[ERROR] Order not found or has no products.")
                else:
                    print("\n[ERROR] Invalid ID.")
                    
            elif choice == '5':
                min_price = input("Enter minimum price to filter products: ")
                try:
                    price_float = float(min_price)
                    results = crud.bq5_get_expensive_products(db, price_float)
                    print(f"\n[RESULT] Products costing ${price_float} or more:")
                    for p in results:
                        print(f"- {p.name}: ${p.price}")
                except ValueError:
                    print("\n[ERROR] Please enter a valid number.")

            elif choice == '6':
                break
            else:
                print("\n[ERROR] Invalid option. Try again.")

def run_cli():
    """Main loop for the CLI application."""
    while True:
        print_main_menu()
        choice = input("\nSelect an option (1-6): ")
        
        if choice == '1':
            with get_db_session() as db:
                users = crud.get_all_users(db)
                print("\n--- All Users ---")
                for u in users:
                    print(f"ID: {u.id} | Username: {u.username} | Email: {u.email}")
        
        elif choice == '2':
            username = input("Enter new username: ").strip()
            email = input("Enter new email: ").strip()
            
            # Input validation
            if not username or not email:
                print("\n[ERROR] Username and email cannot be empty.")
            elif "@" not in email or "." not in email:
                print("\n[ERROR] Please enter a valid email address.")
            else:
                with get_db_session() as db:
                    new_user, error_msg = crud.create_user(db, username, email)
                    if error_msg:
                        print(f"\n[ERROR] {error_msg}")
                    else:
                        print(f"\n[SUCCESS] User '{new_user.username}' created successfully!")
                
        elif choice == '3':
            user_id = input("Enter User ID to update: ")
            if user_id.isdigit():
                with get_db_session() as db:
                    # First, fetch the current user to show their details
                    current_user = crud.get_user_by_id(db, int(user_id))
                    
                    if current_user:
                        print(f"\n[CURRENT DATA] Username: {current_user.username} | Email: {current_user.email}")
                        new_email = input("Enter new email (or press Enter to cancel): ").strip()
                        
                        if not new_email:
                            print("\n[INFO] Update cancelled.")
                        elif "@" not in new_email or "." not in new_email:
                            print("\n[ERROR] Invalid email format. Update failed.")
                        else:
                            # Perform the update
                            updated_user, error_msg = crud.update_user_email(db, int(user_id), new_email)
                            if error_msg:
                                print(f"\n[ERROR] {error_msg}")
                            else:
                                print(f"\n[SUCCESS] Email updated to: {updated_user.email}")
                    else:
                        print("\n[ERROR] User not found.")
            else:
                print("\n[ERROR] Invalid ID.")

        elif choice == '4':
            user_id = input("Enter User ID to delete: ")
            if user_id.isdigit():
                with get_db_session() as db:
                    # Fetch current user to show who is being deleted
                    current_user = crud.get_user_by_id(db, int(user_id))
                    
                    if current_user:
                        print(f"\n[WARNING] You are about to delete: {current_user.username} ({current_user.email})")
                        confirm = input(f"Are you sure you want to permanently delete this user? (y/n): ").strip().lower()
                        
                        if confirm == 'y':
                            success = crud.delete_user(db, int(user_id))
                            if success:
                                print(f"\n[SUCCESS] User {user_id} deleted successfully!")
                        else:
                            print("\n[INFO] Deletion cancelled.")
                    else:
                        print("\n[ERROR] User not found.")
            else:
                print("\n[ERROR] Invalid ID.")
                
        elif choice == '5':
            business_questions_menu()
            
        elif choice == '6':
            print("\nExiting system. Goodbye!")
            sys.exit()
            
        else:
            print("\n[ERROR] Invalid choice. Please enter a number between 1 and 6.")

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit()