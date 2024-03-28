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
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO
                        Vendor (BusinessName, CustomerFeedbackScore, GeographicalPresence)
                    VALUES
                        (%s, %s, %s)
                    """
                cursor.execute(sql, (business_name, customer_feedback_score, geographical_presence))
                vendor_id = cursor.lastrowid
                self.conn.commit()
                return True, vendor_id
        except Exception as e:
            self.conn.rollback()
            return False, None

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
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO
                        Customer (ContactNumber, ShippingDetails)
                    VALUES
                        (%s, %s)
                    """
                cursor.execute(sql, (contact_number, shipping_details))
                customer_id = cursor.lastrowid
                self.conn.commit()
                return True, customer_id
        except Exception as e:
            self.conn.rollback()
            return False, None

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
            
    def login_vendor(self, vendor_id):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Vendor
                WHERE
                    VendorID = %s
                """
            cursor.execute(sql, (vendor_id,))
            vendor_record = cursor.fetchone()
            if vendor_record:
                return True
            else:
                return False
            
    def login_customer(self, customer_id):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Customer
                WHERE
                    CustomerID = %s
                """
            cursor.execute(sql, (customer_id,))
            customer_record = cursor.fetchone()
            if customer_record:
                return True
            else:
                return False

    def insert_product(self, vendor_id, name, price, tag1, tag2, tag3):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO
                        Inventory_Product (VendorID, Name, Price, Tag1, Tag2, Tag3)
                    VALUES
                        (%s, %s, %s, %s, %s, %s)
                    """
                cursor.execute(sql, (vendor_id, name, price, tag1, tag2, tag3))
                product_id = cursor.lastrowid
                self.conn.commit()
                return True, product_id
        except Exception as e:
            self.conn.rollback()
            return False, None

    def list_products(self):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Inventory_Product
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
                    Inventory_Product
                WHERE
                    VendorID = %s
                """
            cursor.execute(sql, (vendor_id,))
            result = cursor.fetchall()
            return result

    def search_products_by_name_and_tag_value(self, name_tag_value_pattern):
        search_pattern = f"%{name_tag_value_pattern}%"
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Inventory_Product
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

    def insert_order(self, customer_id, order_details):
        order_ids = []
        transaction_ids = []

        # To get (last orderID + 1) and let this be the current orderID for the following order inserting
        with self.conn.cursor() as cursor1:
            get_orders = """
                                SELECT * from Place_Order
                                """
            cursor1.execute(get_orders)
            all_orders = cursor1.fetchall()
            last_auto_id = all_orders[-1]['Auto_ID']
            last_order_id = all_orders[-1]['OrderID']
            for order in order_details:
                product_id, quantity = order[0], order[4]
                today = date.today()
                with self.conn.cursor() as cursor:
                    sql = """
                        INSERT INTO
                            Place_Order (OrderID, ProductID, CustomerID, OrderDate, Quantity)
                        VALUES
                            (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, (last_order_id + 1, product_id, customer_id, today, quantity))
                    self.conn.commit()
            transaction_id = self.insert_transaction(last_auto_id + 1, last_order_id + 1)
            print('$$$$$$$$$$')
            order_ids.append(last_order_id + 1)
            transaction_ids.append(transaction_id)
        
        return order_ids, transaction_ids
        
    def update_order_quantity(self, order_id, quantity, product_id):
        if int(quantity) < 0:
            raise ValueError("Quantity cannot be negative.")

        with self.conn.cursor() as cursor:
            today = date.today()
            sql = """
                UPDATE Place_Order
                SET Quantity = %s,
                    OrderDate = %s
                WHERE OrderID = %s
                AND ProductID = %s
            """
            affected_rows = cursor.execute(sql, (quantity, today, order_id, product_id))
            if affected_rows == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True
                
    def insert_transaction(self, auto_id, order_id):
        with self.conn.cursor() as cursor:
            today = date.today()
            sql = """
                INSERT INTO
                    Transaction (Auto_ID, OrderID)
                VALUES
                    (%s, %s)
                """
            cursor.execute(sql, (auto_id, order_id))
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

    def delete_order(self, order_id):
        self.delete_transaction_by_order_id(order_id)
        with self.conn.cursor() as cursor:
            sql = """
                DELETE FROM
                    Place_Order
                WHERE
                    OrderID = %s
            """
            affected_rows = cursor.execute(sql, (order_id))
            if affected_rows == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def delete_transaction_by_order_id(self, order_id):
        with self.conn.cursor() as cursor:
            sql = """
                DELETE FROM
                    Transaction
                WHERE
                    OrderID = %s
            """
            affected_rows = cursor.execute(sql, (order_id))
            if affected_rows == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True
                
    def delete_transaction_by_transaction_id(self, transaction_id):
        with self.conn.cursor() as cursor:
            sql = """
                DELETE FROM
                    Transaction
                WHERE
                    TransactionID = %s
            """
            affected_rows = cursor.execute(sql, (transaction_id))
            if affected_rows == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def show_transactions_by_customer_id(self, customer_id):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    t.TransactionID AS "TransactionID" ,
                    t.OrderID AS "OrderID",
                    t.ShippedDate AS "ShippedDate",
                    t.ArrivalDate AS "ArrivalDate"
                FROM
                    `Transaction` t, Place_Order po
                WHERE
                    t.Auto_ID = po.Auto_ID
                AND
                    CustomerID = %s
                """
            cursor.execute(sql, (customer_id))
            result = cursor.fetchall()
            return result

    def cancel_order(self, order_id):
        with self.conn.cursor() as cursor:
            sql = """
                UPDATE
                    Place_Order
                SET
                    OrderStatus = %s
                WHERE
                    OrderID = %s
                """
            cursor.execute(sql, ("Cancelled", order_id))
            self.conn.commit()

    def show_orders(self, customer_id):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Place_Order
                WHERE
                    CustomerID = %s
                """
            cursor.execute(sql, (customer_id,))
            result = cursor.fetchall()
            return result

    def list_transition(self):
        with self.conn.cursor() as cursor:
            sql = """
                SELECT
                    *
                FROM
                    Transaction
                """
            cursor.execute(sql, )
            result = cursor.fetchall()
            return result