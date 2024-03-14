from database import Database
from db_config import read_db_config
from order_management import list_all_orders

def get_index_of_transaction_to_delete():
    row = input("[1/1] Enter the index of the transaction to delete: ")
    row = int(row) - 1
    return row

def get_transaction_info():
    product_id = input("[1/2] Enter the Product ID: ")
    quantity = input("[2/2] Enter the Quantity: ")
    return product_id, quantity

def add_transaction_info(customer_id, transaction_list):
    product_id, quantity = get_transaction_info()
    transaction = [product_id, quantity]
    transaction_list.append(transaction)
    print("Transaction has been added successfully.")
    show_transactions(customer_id, transaction_list)
    print("\nReminder: Please make sure to complete your order, "
          "as the transaction is not finalized until this step has been taken.")
    return transaction_list

def update_transaction(database):
    customer_id = input("[1/4] Enter the Customer ID: ")
    list_all_orders(database, customer_id)
    order_id = input("[2/4] Enter the Order ID: ")
    transaction_id = input("[3/4] Enter the Transaction ID: ")
    quantity = input("[4/4] Enter the Quantity (enter 0 to delete): ")
    if int(quantity) == 0:
        success = database.delete_transaction(order_id, customer_id, transaction_id)
        if success:
            print(f"Transaction #{transaction_id} for Order #{order_id} has been deleted successfully.")
        else:
            print(f"Failed to delete Transaction #{transaction_id} for Order #{order_id}.")
    else:
        success = database.update_transaction(order_id, customer_id, transaction_id, quantity)
        if success:
            print(f"Transaction #{transaction_id} for Order #{order_id} has been updated to quantity {quantity}.")
        else:
            print(f"Failed to update Transaction #{transaction_id} for Order #{order_id}.")

def show_transactions(customer_id, transaction_list):
    if not transaction_list:
        print("There are no transactions to display.")
        return

    header = "| Row | Customer ID | Product ID | Quantity |"
    divider = "+" + "-" * (len(header) - 2) + "+"

    print("\nCurrent Transactions:")
    print(divider)
    print(header)
    print(divider)

    row = 1  # Start row numbering at 1
    for transaction in transaction_list:
        product_id, quantity = transaction
        print(f"| {row:<3} | {customer_id:<11} | {product_id:<10} | {quantity:<8} |")
        row += 1

    print(divider)

def delete_transaction(customer_id, transaction_list):
    if not transaction_list:
        print("No transactions available to delete.")
        return transaction_list
    show_transactions(customer_id, transaction_list)
    try:
        row = int(get_index_of_transaction_to_delete())
        if 0 <= row < len(transaction_list):
            transaction_list.pop(row)
            print(f"Transaction at index {row} has been deleted.")
            show_transactions(customer_id, transaction_list)
        else:
            print("Invalid index. Please enter a valid transaction index.")
    except ValueError:
        print("Invalid input. Please enter an integer index.")
    return transaction_list

def main():
    db_config = read_db_config()
    db = Database(**db_config)

if __name__ == '__main__':
    main()