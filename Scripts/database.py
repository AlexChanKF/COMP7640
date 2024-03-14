import pymysql
from datetime import date

class Database:
    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    database=database,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def insert_vendor(self, business_name, customer_feedback_score, geographical_presence):
        with self.conn.cursor() as cursor:
            sql = """
                INSERT INTO
                    Vendor (BusinessName, CustomerFeedbackScore, GeographicalPresence)
                VALUES
                    (%s, %s, %s)
                """
            cursor.execute(sql, (business_name, customer_feedback_score, geographical_presence))
            self.conn.commit()

    def show_vendors(self):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Vendor
                """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def insert_customer(self, contact_number, shipping_details):
        with self.conn.cursor() as cursor:
            sql = """
                INSERT INTO
                    Customer (ContactNumber, ShippingDetails)
                VALUES
                    (%s, %s)
                """
            cursor.execute(sql, (contact_number, shipping_details))
            self.conn.commit()

    def show_customers(self):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Customer
                """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def insert_product(self, vendor_id, name, price, tags):
        with self.conn.cursor() as cursor:
            sql = """
                INSERT INTO
                    Product (VendorID, Name, Price, Tag1, Tag2, Tag3)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
                """
            product_data = (vendor_id, name, price) + tuple(tags)
            cursor.execute(sql, product_data)
            self.conn.commit()

    def list_products(self):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Product
                """
            cursor.execute(sql, )
            result = cursor.fetchall()
            return result

    def search_products_by_vendor_id(self, vendor_id):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Product
                WHERE
                    VendorID = %s
                """
            cursor.execute(sql, (vendor_id,))
            result = cursor.fetchall()
            return result

    def search_products_by_tag_value(self, tag_value_pattern):
        search_pattern = f"%{tag_value_pattern}%"
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Product
                WHERE
                    Name LIKE %s
                    OR
                    Tag1 LIKE %s
                    OR
                    Tag2 LIKE %s
                    OR
                    Tag3 LIKE %s
                """
            cursor.execute(sql, (search_pattern, search_pattern, search_pattern, search_pattern))
            result = cursor.fetchall()
            return result

    def insert_order(self, customer_id, transaction_list):
        order_id = ""
        completed_transaction_id_list = []
        today = date.today()
        with self.conn.cursor() as cursor:
            sql = """
                INSERT INTO
                    `Order` (CustomerID, OrderDate)
                VALUES
                    (%s, %s)
                """
            cursor.execute(sql, (customer_id, today))
            self.conn.commit()
            order_id = cursor.lastrowid
        for transaction in transaction_list:
            product_id, quantity = transaction
            completed_transaction_id_list.append(self.insert_transaction(order_id, customer_id, product_id, quantity))
        return order_id, completed_transaction_id_list

    def insert_transaction(self, order_id, customer_id, product_id, quantity):
        with self.conn.cursor() as cursor:
            today = date.today()
            sql = """
                INSERT INTO
                    Transaction (OrderID, CustomerID, ProductID, Quantity, Date)
                VALUES
                    (%s, %s, %s, %s, %s)
                """
            cursor.execute(sql, (order_id, customer_id, product_id, quantity, today))
            self.conn.commit()
            transaction_id = cursor.lastrowid
            return transaction_id

    def update_transaction(self, order_id, customer_id, transaction_id, quantity):
        if int(quantity) < 0:
            raise ValueError("Quantity cannot be negative.")

        with self.conn.cursor() as cursor:
            today = date.today()
            sql = """
                UPDATE Transaction
                SET Quantity = %s,
                    Date = %s
                WHERE OrderID = %s AND CustomerID = %s AND TransactionID = %s
            """
            affected_rows = cursor.execute(sql, (quantity, today, order_id, customer_id, transaction_id))
            if affected_rows == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def delete_transaction(self, order_id, customer_id, transaction_id):
        with self.conn.cursor() as cursor:
            sql = """
                DELETE FROM
                    Transaction
                WHERE
                    OrderID = %s
                AND
                    CustomerID = %s
                AND
                    TransactionID = %s
            """
            affected_rows = cursor.execute(sql, (order_id, customer_id, transaction_id))
            if affected_rows == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def show_transactions(self, order_id, customer_id):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Transaction
                WHERE
                    OrderID = %s
                AND
                    CustomerID = %s
                """
            cursor.execute(sql, (order_id, customer_id))
            result = cursor.fetchall()
            return result

    def cancel_order(self, order_id):
        with self.conn.cursor() as cursor:
            sql = """
                UPDATE
                    `Order`
                SET
                    OrderStatus = %s
                WHERE
                    OrderID = %s
                """
            cursor.execute(sql, ("CANCELLED", order_id))
            self.conn.commit()

    def show_orders(self, customer_id):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    `Order`
                WHERE
                    CustomerID = %s
                """
            cursor.execute(sql, (customer_id,))
            result = cursor.fetchall()
            return result