from database import Database
from db_config import read_db_config

def get_vendor_info():
    business_name = input("Enter the business name of the vendor [Alex]: ")
    customer_feedback_score = input("Enter the customer feedback score of the vendor [0-100]: ")
    geographical_presence = input("Enter the geographical presence of the vendor [HK,JP,TW]: ")
    return business_name, customer_feedback_score, geographical_presence

def add_verdor_info(database):
    business_name, customer_feedback_score, geographical_presence = get_vendor_info()
    database.insert_vendor(business_name, customer_feedback_score, geographical_presence)
    print("Vendor has been added successfully.")
    
def show_vendors(database):
    vendors = database.show_vendors()
    print(f"ID, Business Name, Customer Feedback Score, Geographical Presence")
    if vendors:
        for vendor in vendors:
            print(f"{vendor['VendorID']}, {vendor['BusinessName']}, {vendor['CustomerFeedbackScore']}, {vendor['GeographicalPresence']}")
    else:
        print("No vendors found.")

def main():
    db_config = read_db_config()
    db = Database(**db_config)
    add_verdor_info(db)
    list_all_vendors(db)

if __name__ == '__main__':
    main()