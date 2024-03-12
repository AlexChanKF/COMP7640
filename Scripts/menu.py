# menu.py

import os
from database import Database
from db_config import read_db_config
from vendor_management import add_verdor_info, show_vendors
from product_management import add_product_info, show_products, search_products_by_vendor_id, search_products_by_tag_value
from customer_management import add_customer_info, list_customers
from order_management import create_order
from transaction_management import add_transaction_info, delete_transaction, show_transactions

# Initialize the database connection
db_config = read_db_config()
db = Database(**db_config)

# Function to clear the screen
def clear_screen():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def vendor_management_screen():
    while True:
        clear_screen()
        print("\nVendor Management:")
        print("1. Add Vendor")
        print("2. Show Vendors")
        print("3. Return to Main Menu")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            add_verdor_info(db)
        elif choice == '2':
            show_vendors(db)
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")

def product_management_screen():
    while True:
        clear_screen()
        print("\nProduct Management:")
        print("1. Add Product")
        print("2. Show Products")
        print("3. Return to Main Menu")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            add_product_info(db)
        elif choice == '2':
            show_products(db)
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")
        
def search_management_screen():
    while True:
        clear_screen()
        print("\nSearch Management:")
        print("1. Search Products By Vendor ID")
        print("2. Search Products By Tag")
        print("3. Return to Main Menu")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            search_products_by_vendor_id(db)
        elif choice == '2':
            search_products_by_tag_value(db)
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")
        
def customer_management_screen():
    while True:
        clear_screen()
        print("\nCustomer Management:")
        print("1. Add Customer")
        print("2. Show Customers")
        print("3. Return to Main Menu")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            add_customer_info(db)
        elif choice == '2':
            list_customers(db)
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")
        
def order_management_screen():
    while True:
        clear_screen()
        print("\nOrder Management:")
        print("1. New Order")
        print("2. Modify Order")
        print("3. View Order History")
        print("4. Cancel Order")
        print("5. Return to Main Menu")
        choice = input("Enter your choice (1/2/3/4/5): ")
        
        if choice == '1':
            customer_id = input("Enter the Customer ID: ")
            transaction_management(customer_id)
        elif choice == '2':
            list_all_customers(db)
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")
        
def transaction_management(customer_id):
    transaction_list = []
    while True:
        clear_screen()
        print(f"\nTracsaction Management [Customer ID: {customer_id}]:")
        print("1. New Transaction")
        print("2. Delete Transaction")
        print("3. Show Current Transactions")
        print("4. Complete Transaction and Order")
        print("5. Return to Main Menu")
        choice = input("Enter your choice (1/2/3/4/5): ")
        
        if choice == '1':
            transaction_list = add_transaction_info(customer_id, transaction_list)
        elif choice == '2':
            transaction_list = delete_transaction(customer_id, transaction_list)
        elif choice == '3':
            show_transactions(customer_id, transaction_list)
        elif choice == '4':
            create_order(db, customer_id, transaction_list)
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")
        
def main_menu():
    while True:
        clear_screen()
        print("\nMain Menu:")
        print("1. Vendor Management")
        print("2. Product Management")
        print("3. Search Management")
        print("4. Customer Management")
        print("5. Order Management")
        print("6. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6): ")
        
        if choice == '1':
            vendor_management_screen()
        elif choice == '2':
            product_management_screen()
        elif choice == '3':
            search_management_screen()
        elif choice == '4':
            customer_management_screen()
        elif choice == '5':
            order_management_screen()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main_menu()