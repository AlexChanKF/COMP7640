from database import Database
from db_config import read_db_config

def get_customer_info():
    contact_number = input("Enter the customer number: ")
    shipping_details = input("Enter the shipping details: ")
    return contact_number, shipping_details

def add_customer_info(database):
    contact_number, shipping_details = get_customer_info()
    database.insert_customer(contact_number, shipping_details)
    print("Customer has been added successfully.")
    
def list_customers(database):
    customers = database.show_customers()
    print(f"ID, Contact Number, Shipping Details")
    if customers:
        for vendor in customers:
            print(f"{vendor['CustomerID']}, {vendor['ContactNumber']}, {vendor['ShippingDetails']}")
    else:
        print("No customers found.")

def main():
    db_config = read_db_config()
    db = Database(**db_config)
    add_customer_info(db)
    list_customers(db)

if __name__ == '__main__':
    main()