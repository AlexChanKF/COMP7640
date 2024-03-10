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

    def modify_order(self, order_id, action, product_id=None):
        with self.conn.cursor() as cursor:
            if action == 'cancel':
                sql = "DELETE FROM Order WHERE OrderID = %s"
                cursor.execute(sql, (order_id,))
            elif action == 'add_product' and product_id is not None:
                sql = "UPDATE Order SET ProductID = %s WHERE OrderID = %s"
                cursor.execute(sql, (product_id, order_id))
            elif action == 'remove_product':
                sql = "UPDATE Order SET ProductID = NULL WHERE OrderID = %s"
                cursor.execute(sql, (order_id,))
            else:
                raise ValueError("Invalid action or missing product_id for 'add_product'")
            self.conn.commit()