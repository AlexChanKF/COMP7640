from database import Database
from db_config import read_db_config

def get_product_info():
    vendor_id = input("Please enter the vendor ID: ")
    name = input("Please enter the product name: ")
    price = input("Please enter the product price: ")
    tags = [input(f"Enter tag {i+1} (or leave blank): ") for i in range(3)]
    return vendor_id, name, price, tags

def add_product_info(database):
    vendor_id, name, price, tags = get_product_info()
    database.insert_product(vendor_id, name, price, tags)
    print("Product has been added successfully.")
    
def show_products(database):
    products = database.list_products()
    print(f"ProductID, VendorID, Name, Price, Tag1, Tag2, Tag3")
    if products:
        for product in products:
            print(f"{product['ProductID']}, {product['VendorID']}, {product['Name']}, {product['Price']}, {product['Tag1']}, {product['Tag2']}, {product['Tag3']}")
    else:
        print("No products found.")
        
def get_vendor_info():
    vendor_id = input("Enter the Vendor ID to search products: ")
    return vendor_id
    
def get_tag_value_info():
    tag_value = input("Enter the Tag value to search products: ")
    return tag_value

def search_products_by_vendor_id(database):
    vendor_id = get_vendor_info()
    products = database.search_products_by_vendor_id(vendor_id)
    print(f"ProductID, Name, Price, Tag1, Tag2, Tag3")
    if products:
        for product in products:
            print(f"{product['ProductID']}, {product['Name']}, {product['Price']}, {product['Tag1']}, {product['Tag2']}, {product['Tag3']}")
    else:
        print(f"No products found for Vendor ID {vendor_id}.")
        
def search_products_by_tag_value(database):
    tag_value = get_tag_value_info()
    products = database.search_products_by_tag_value(tag_value)
    print(f"ProductID, Name, Price, Tag1, Tag2, Tag3")
    if products:
        for product in products:
            print(f"{product['ProductID']}, {product['Name']}, {product['Price']}, {product['Tag1']}, {product['Tag2']}, {product['Tag3']}")
    else:
        print(f"No products found for Tag Value {tag_value}.")

def main():
    db_config = read_db_config()
    db = Database(**db_config)
    add_product_info(db)
    show_products(db)
    search_products_by_vendor_id(db)
    search_products_by_tag(db)

if __name__ == '__main__':
    main()