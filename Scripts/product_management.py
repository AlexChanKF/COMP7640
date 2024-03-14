from database import Database
from db_config import read_db_config

def get_product_info():
    vendor_id = input("[1/6] Please enter the vendor ID: ")
    name = input("[2/6] Please enter the product name: ")
    price = input("[3/6] Please enter the product price: ")
    tags = [input(f"[{i+4}/6] Enter tag {i+1} (or leave blank): ") for i in range(3)]
    return vendor_id, name, price, tags

def add_product_info(database):
    vendor_id, name, price, tags = get_product_info()
    database.insert_product(vendor_id, name, price, tags)
    print("Product has been added successfully.")

def show_products(database):
    products = database.list_products()
    print_products_table(products, f"All Vendors")

def get_vendor_info():
    vendor_id = input("[1/1] Enter the Vendor ID to search products: ")
    return vendor_id

def get_tag_value_info():
    tag_value = input("[1/1] Enter the Tag value to search products: ")
    return tag_value

def print_products_table(products, search_criteria):
    header_top = "| ProductID | VendorID | Name                         | Price      | Tag1         | Tag2         | Tag3         |"
    divider = "+" + "-" * (len(header_top) - 2) + "+"

    print(divider)
    print(header_top)
    print(divider)

    if not products:
        empty_row_msg = f"No products found for {search_criteria}."
        empty_row = "|" + empty_row_msg.center(len(header_top) - 2) + "|"
        print(empty_row)
    else:
        for product in products:
            product_id = str(product.get('ProductID', 'N/A'))
            vendor_id = str(product.get('VendorID', 'N/A'))
            name = str(product.get('Name', 'N/A'))
            price = str(product.get('Price', 'N/A'))
            tag1 = str(product.get('Tag1', 'N/A'))
            tag2 = str(product.get('Tag2', 'N/A'))
            tag3 = str(product.get('Tag3', 'N/A'))

            name = (name[:26] + '..') if len(name) > 28 else name
            tag1 = (tag1[:10] + '..') if len(tag1) > 12 else tag1
            tag2 = (tag2[:10] + '..') if len(tag2) > 12 else tag2
            tag3 = (tag3[:10] + '..') if len(tag3) > 12 else tag3

            print(f"| {product_id:<9} | {vendor_id:<8} | {name:<28} | {price:<10} | {tag1:<12} | {tag2:<12} | {tag3:<12} |")

    print(divider)

def search_products_by_vendor_id(database):
    vendor_id = get_vendor_info()
    products = database.search_products_by_vendor_id(vendor_id)
    print_products_table(products, f"Vendor ID {vendor_id}")

def search_products_by_tag_value(database):
    tag_value = get_tag_value_info()
    products = database.search_products_by_tag_value(tag_value)
    print_products_table(products, f"Tag Value {tag_value}")

def main():
    db_config = read_db_config()
    db = Database(**db_config)
    add_product_info(db)
    show_products(db)
    search_products_by_vendor_id(db)
    search_products_by_tag(db)

if __name__ == '__main__':
    main()