from database import Database
from db_config import read_db_config

def create_order(database, customer_id, transaction_list):
    order_id, completed_transaction_id_list = database.insert_order(customer_id, transaction_list)
    print(f"Order#{order_id} has been added successfully.")

def main():
    db_config = read_db_config()
    db = Database(**db_config)
    add_order_info(db)

if __name__ == '__main__':
    main()