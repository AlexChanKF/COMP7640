from database import Database
from db_config import read_db_config

def get_customer_info():
    contact_number = input("[1/2] Enter the customer number: ")
    shipping_details = input("[1/2] Enter the shipping details: ")
    return contact_number, shipping_details

def add_customer_info(database):
    contact_number, shipping_details = get_customer_info()
    database.insert_customer(contact_number, shipping_details)
    print("Customer has been added successfully.")

def list_customers(database):
    customers = database.show_customers()

    header_top =    "| ID        | Contact Number     | Shipping Details                    |"
    divider = "+" + "-" * (len(header_top) - 2) + "+"

    print(divider)
    print(header_top)
    print(divider)

    if not customers:
        empty_row_msg = "No customers found."
        empty_row = "|" + empty_row_msg.center(len(header_top) - 2) + "|"
        print(empty_row)
    else:
        for customer in customers:
            customer_id = customer.get('CustomerID', 'N/A')
            contact_number = customer.get('ContactNumber', 'N/A')
            shipping_details = customer.get('ShippingDetails', 'N/A')
            contact_number = (contact_number[:16] + '..') if len(contact_number) > 18 else contact_number
            shipping_details = (shipping_details[:33] + '..') if len(shipping_details) > 35 else shipping_details
            print(f"| {customer_id:<9} | {contact_number:<18} | {shipping_details:<35} |")

    print(divider)

def main():
    db_config = read_db_config()
    db = Database(**db_config)
    add_customer_info(db)
    list_customers(db)

if __name__ == '__main__':
    main()