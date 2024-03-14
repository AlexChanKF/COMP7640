from database import Database
from db_config import read_db_config

def create_order(database, customer_id, transaction_list):
    order_id, completed_transaction_id_list = database.insert_order(customer_id, transaction_list)
    print(f"Order#{order_id} has been added successfully.")

def cancel_order(database):
    customer_id = input("[1/2] Enter the Customer ID: ")
    list_all_orders(database, customer_id)
    order_id = input("[2/2] Enter the Order ID: ")
    order_id = database.cancel_order(order_id)
    print(f"Order#{order_id} has been cancelled successfully.")

def list_all_orders(database, customer_id=None):
    if customer_id == None:
        customer_id = input("[1/1] Enter the Customer ID: ")
    order_list = database.show_orders(customer_id)

    header = "| OrderID | CustomerID | OrderDate  | OrderStatus  | TransactionID  | ProductID | Quantity | Date       |"
    divider = "+" + "-" * (len(header) - 2) + "+"

    print(divider)
    print(header)
    print(divider)

    prvious_order_id = None
    for order in order_list:
        transaction_list = database.show_transactions(order['OrderID'], customer_id)
        for transaction in transaction_list:
            order_id = order['OrderID'] if order['OrderID'] is not None else 'N/A'
            order_date = order['OrderDate'].strftime('%Y-%m-%d') if order['OrderDate'] is not None else 'N/A'
            order_status = order['OrderStatus'] if order['OrderStatus'] is not None else 'N/A'
            transaction_id = transaction['TransactionID'] if transaction['TransactionID'] is not None else 'N/A'
            product_id = transaction['ProductID'] if transaction['ProductID'] is not None else 'N/A'
            quantity = transaction['Quantity'] if transaction['Quantity'] is not None else 'N/A'
            date = transaction['Date'].strftime('%Y-%m-%d') if transaction['Date'] is not None else 'N/A'
            if order_id == prvious_order_id or prvious_order_id == None:
                prvious_order_id = order_id
            else:
                prvious_order_id = order_id
                print(divider)
            print(f"| {order_id:7} | {int(customer_id):10} | {order_date:10} | "
                  f"{order_status:<12} | {transaction_id:14} | "
                  f"{product_id:9} | {quantity:8} | {date:10} |")
    print(divider)

def main():
    db_config = read_db_config()
    db = Database(**db_config)
    add_order_info(db)

if __name__ == '__main__':
    main()