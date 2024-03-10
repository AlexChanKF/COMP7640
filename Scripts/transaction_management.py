from database import Database
from db_config import read_db_config

def get_index_of_transaction_to_delete():
    row = input("Enter the index of the transaction to delete: ")
    return row

def get_transaction_info():
    product_id = input("Enter the Product ID: ")
    quantity = input("Enter the Quantity: ")
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
    
def show_transactions(customer_id, transaction_list):
    if not transaction_list:
        print("There are no transactions to display.")
        return
    print("\nCurrent Transactions:")
    print("Row, Customer ID, Product ID, Quantity")
    row = 0
    for transaction in transaction_list:
        product_id, quantity = transaction
        print(f"{row}, {customer_id}, {product_id}, {quantity}")
        row += 1
        
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