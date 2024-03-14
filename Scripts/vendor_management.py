from database import Database
from db_config import read_db_config

def get_vendor_info():
    business_name = input("[1/3] Enter the business name of the vendor: ")
    customer_feedback_score = input("[2/3] Enter the customer feedback score of the vendor: ")
    geographical_presence = input("[3/3] Enter the geographical presence of the vendor: ")
    return business_name, customer_feedback_score, geographical_presence

def add_verdor_info(database):
    business_name, customer_feedback_score, geographical_presence = get_vendor_info()
    database.insert_vendor(business_name, customer_feedback_score, geographical_presence)
    print("Vendor has been added successfully.")

def show_vendors(database):
    vendors = database.show_vendors()

    header_top =    "| ID     | Business Name                        | Customer | Geographical  |"
    header_middle = "|        |                                      | Feedback | Presence      |"
    header_bottom = "|        |                                      | Score    |               |"
    divider = "+" + "-" * (len(header_top) - 2) + "+"

    print(divider)
    print(header_top)
    print(header_middle)
    print(header_bottom)
    print(divider)

    if not vendors:
        empty_row_msg = "No vendors found."
        empty_row = "|" + empty_row_msg.center(len(header_top) - 2) + "|"
        print(empty_row)
    else:
        for vendor in vendors:
            vendor_id = vendor.get('VendorID', 'N/A')
            business_name = vendor.get('BusinessName', 'N/A')
            feedback_score = vendor.get('CustomerFeedbackScore', 'N/A')
            geo_presence = vendor.get('GeographicalPresence', 'N/A')
            business_name = (business_name[:34] + '..') if len(business_name) > 36 else business_name
            geo_presence = (geo_presence[:11] + '..') if len(geo_presence) > 13 else geo_presence
            print(f"| {vendor_id:<6} | {business_name:<36} | {feedback_score:<8} | {geo_presence:<13} |")

    print(divider)

def main():
    db_config = read_db_config()
    db = Database(**db_config)
    add_verdor_info(db)
    list_all_vendors(db)

if __name__ == '__main__':
    main()