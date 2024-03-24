import tkinter as tk
import os
from database import Database
from db_config import read_db_config
from tkinter import ttk
from tkinter import messagebox

db_config = read_db_config()
db = Database(**db_config)
CUSTOMER_ID = None
VENDOR_ID = None

def center_window(parent, popup):
    parent.update_idletasks()
    px = parent.winfo_rootx()
    py = parent.winfo_rooty()
    pwidth = parent.winfo_width()
    pheight = parent.winfo_height()

    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()

    x = px + (pwidth // 2) - (width // 2)
    y = py + (pheight // 2) - (height // 2)

    popup.geometry(f'+{x}+{y}')

def update_status(message, color):
    status_bar.config(text=message, fg=color)
    
def update_login_status(message, color):
    login_status_bar.config(text=message, fg=color)
    update_status("", None)

#Vendor
def add_vendor(parent):

    popup = tk.Toplevel(parent)
    popup.title("Add Vendors")

    # 添加标签和输入框
    tk.Label(popup, text="Enter the Business Name of the Vendor:").pack(anchor='w')
    business_entry = tk.Entry(popup)
    business_entry.pack(fill='x')

    tk.Label(popup, text="Enter the Customer Feedback Score of the Vendor [0 - 100]:").pack(anchor='w')
    customer_score = tk.Entry(popup)
    customer_score.pack(fill='x')

    tk.Label(popup, text="Enter the Geographical Presence of the Vendor [HK, JP, etc.]: ").pack(anchor='w')
    geographical_entry = tk.Entry(popup)
    geographical_entry.pack(fill='x')

    # 提交按钮
    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_info())
    submit_button.pack()
    center_window(parent, popup)

    # 提交按钮的功能
    def submit_info():
        business_name = business_entry.get()
        customer_feedback_score = customer_score.get()
        geographical_presence = geographical_entry.get()
        success, vendor_id = db.insert_vendor(business_name, customer_feedback_score, geographical_presence)

        if success:
            status_message = "Success: The record was inserted. ID: {}, Name: {}, Score: {}, Presence: {}.".format(vendor_id, business_name, customer_feedback_score, geographical_presence)
            update_status(status_message, "green")
        else:
            status_message = "Error: Failed to insert the record."
            update_status(status_message, "red")

        # 关闭弹窗
        popup.destroy()
        
def login_vendor(parent):

    popup = tk.Toplevel(parent)
    popup.title("Login as a Vendor")
    tk.Label(popup, text="Enter Vendor ID:").pack(anchor='w')
    vendor_id_entry = tk.Entry(popup)
    vendor_id_entry.pack(fill='x')
    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_vendor_id())
    submit_button.pack()
    center_window(parent, popup)

    # 提交按钮的功能
    def submit_vendor_id():
        vendor_id = vendor_id_entry.get()
        success = db.login_vendor(vendor_id)
        if success:
            status_message = "Login with Vendor ID: {}.".format(vendor_id)
            global CUSTOMER_ID
            CUSTOMER_ID = None
            global VENDOR_ID
            VENDOR_ID = vendor_id
            update_login_status(status_message, "green")
            refresh_ui()
        else:
            status_message = "Error: Failed to Login."
            update_login_status(status_message, "red")

        # 关闭弹窗
        popup.destroy()

def show_vendors(parent, database):
    # 创建弹窗
    db_window = tk.Toplevel(parent)
    db_window.title("Show Vendors")

    # 设置树形控件以显示表格数据
    columns = ("Vendor ID","Business Name", "Cutomer Feedback Score", "Geographical Presence")
    tree = ttk.Treeview(db_window, columns=columns, show='headings')

    # 定义表头
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # 将树形控件放置在弹窗布局中
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 添加滚动条
    scrollbar = ttk.Scrollbar(db_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    vendors = database.show_vendors()
    list=[]
    for vendor in vendors:
        list = (f"{vendor['VendorID']}", f"{vendor['BusinessName']}", f"{vendor['CustomerFeedbackScore']}", f"{vendor['GeographicalPresence']}")
        tree.insert("",tk.END,values=list)
    center_window(parent, db_window)

def add_product(parent):
    popup = tk.Toplevel(parent)
    popup.title("Add Products")

    # 添加标签和输入框
    tk.Label(popup, text="Enter the Vendor ID of the Product:").pack(anchor='w')
    vendor_entry = tk.Entry(popup)
    vendor_entry.pack(fill='x')

    tk.Label(popup, text="Enter the Name of the Product:").pack(anchor='w')
    productname_entry = tk.Entry(popup)
    productname_entry.pack(fill='x')

    tk.Label(popup, text="Enter the Price of the Product:").pack(anchor='w')
    price_entry = tk.Entry(popup)
    price_entry.pack(fill='x')

    tk.Label(popup, text="Enter the Tag1:").pack(anchor='w')
    Tag1_entry= tk.Entry(popup)
    Tag1_entry.pack(fill='x')

    tk.Label(popup, text="Enter the Tag2 ").pack(anchor='w')
    Tag2_entry = tk.Entry(popup)
    Tag2_entry.pack(fill='x')

    tk.Label(popup, text="Enter the Tag3 ").pack(anchor='w')
    Tag3_entry = tk.Entry(popup)
    Tag3_entry.pack(fill='x')

    # 提交按钮
    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_info())
    submit_button.pack()
    center_window(parent, popup)

    # 提交按钮的功能
    def submit_info():
        vendor_id = vendor_entry.get()
        product_name = productname_entry.get()
        price = price_entry.get()
        Tag1 = Tag1_entry.get()
        Tag2 = Tag2_entry.get()
        Tag3 = Tag3_entry.get()
        success, product_id = db.insert_product(vendor_id, product_name, price, Tag1, Tag2 , Tag3)
        if success:
            status_message = "Success: The record was inserted. Product ID: {}, Name: {}, Price: {}, Tag[1,2,3]: [{},{},{}].".format(product_id, product_name, price, Tag1, Tag2, Tag3)
            update_status(status_message, "green")
        else:
            status_message = "Error: Failed to insert the record."
            update_status(status_message, "red")

        # 关闭弹窗
        popup.destroy()

def show_products(parent, database):
    if hasattr(parent, 'main_frame'):
        parent.main_frame.destroy()
        delattr(parent, 'main_frame')
        
    def populate_tree():
        try:
            products_list = fetch_products()
            for product in products_list:
                tree.insert('', 'end', values=product)
        except Exception as e:
            messagebox.showerror("Error", "Failed to load products.")

    def fetch_products():
        try:
            products = database.list_products()
            return [list(product.values()) for product in products]
        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch products from the database.")
            return []

    main_frame = tk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    parent.main_frame = main_frame

    tree_frame = tk.Frame(main_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    columns = ("Product ID", "Vendor ID", "Name", "Price", "Tag 1", "Tag 2", "Tag 3")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    populate_tree()

def search_products(parent, database):

    if hasattr(parent, 'main_frame'):
        parent.main_frame.destroy()
        delattr(parent, 'main_frame')
        
    def click_to_search():
        key_word = search_var.get()
        if key_word.strip():
            try:
                search_list = search(database, key_word)
                show(search_list)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "The search keyword cannot be empty.")

    def show(search_list):
        tree.delete(*tree.get_children())
        for product in search_list:
            tree.insert('', 'end', values=product)

    def search(database, word):
        try:
            products = database.search_products_by_tag_value(word)
            return [list(product.values()) for product in products]
        except Exception as e:
            messagebox.showerror("Error", "Failed to search the database.")
            return []

    main_frame = tk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    parent.main_frame = main_frame

    search_frame = tk.Frame(main_frame)
    search_frame.pack(fill=tk.X)

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    search_button = tk.Button(search_frame, text='Search', command=lambda: click_to_search())
    search_button.pack(side=tk.LEFT)

    tree_frame = tk.Frame(main_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    columns = ("Product ID", "Vendor ID", "Name", "Price", "Tag 1", "Tag 2", "Tag 3")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

#Customer
def add_customer(parent):
    popup = tk.Toplevel(parent)
    popup.title("Add Customer")

    # 添加标签和输入框
    tk.Label(popup, text="Enter the Phone Number: ").pack(anchor='w')
    contact_number_entry = tk.Entry(popup)
    contact_number_entry.pack(fill='x')

    tk.Label(popup, text="Enter the Shipping Details:").pack(anchor='w')
    shipping_details_entry = tk.Entry(popup)
    shipping_details_entry.pack(fill='x')
    # 提交按钮
    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_info())
    submit_button.pack()
    center_window(parent, popup)

    # 提交按钮的功能
    def submit_info():
        contact_number=contact_number_entry.get()
        shipping_details=shipping_details_entry.get()
        success, customer_id = db.insert_customer(contact_number, shipping_details)
        if success:
            status_message = "Success: The record was inserted. Customer ID: {}, Contact Number: {}, Shipping Details: {}.".format(customer_id, contact_number, shipping_details)
            update_status(status_message, "green")
        else:
            status_message = "Error: Failed to insert the record."
            update_status(status_message, "red")

        # 关闭弹窗
        popup.destroy()
        
def login_customer(parent):

    popup = tk.Toplevel(parent)
    popup.title("Login as a Customer")
    tk.Label(popup, text="Enter Customer ID:").pack(anchor='w')
    customer_id_entry = tk.Entry(popup)
    customer_id_entry.pack(fill='x')
    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_customer_id())
    submit_button.pack()
    center_window(parent, popup)

    # 提交按钮的功能
    def submit_customer_id():
        customer_id = customer_id_entry.get()
        success = db.login_customer(customer_id)
        if success:
            status_message = "Login with Customer ID: {}.".format(customer_id)
            global CUSTOMER_ID
            CUSTOMER_ID = customer_id
            global VENDOR_ID
            VENDOR_ID = None
            update_login_status(status_message, "green")
            refresh_ui()
        else:
            status_message = "Error: Failed to Login."
            update_login_status(status_message, "red")

        # 关闭弹窗
        popup.destroy()

def show_customers(parent, database):
    # 创建弹窗
    db_window = tk.Toplevel(parent)
    db_window.title("Customer Information")

    # 设置树形控件以显示表格数据
    columns = ("Cutomer ID","Contact Number", "Shipping Details")
    tree = ttk.Treeview(db_window, columns=columns, show='headings')

    # 定义表头
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # 将树形控件放置在弹窗布局中
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 添加滚动条
    scrollbar = ttk.Scrollbar(db_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    customers = database.show_customers()
    list=[]
    for customer in customers:
        list = (f"{customer['CustomerID']}", f"{customer['ContactNumber']}", f"{customer['ShippingDetails']}")
        tree.insert("",tk.END,values=list)
    center_window(parent, db_window)

#Order
def create_order(parent):
    popup = tk.Toplevel(parent)
    popup.title("Create Order")

    search_frame = tk.Frame(popup)
    search_frame.pack(pady=12)
    # 创建一个字符串变量
    search_va = tk.StringVar()
    # 设置树形控件以显示表格数据
    columns = ("Product ID","Vendor ID", "Name", "Price","Tag 1","Tag 2","Tag 3")
    columnsa = ("Product ID","Quantity")
    tk.Label(search_frame, text='Product Search By Name, Tags').pack(side=tk.LEFT, padx=6)
    tk.Entry(search_frame, relief='flat', width=10, textvariable=search_va).pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text='All Product',command=lambda:print_products_table(parent)).pack(side=tk.LEFT,padx=8)
    tk.Button(search_frame, text='Search',command=lambda:click()).pack(side=tk.LEFT,padx=8)
    # tk.Button(search_frame, text='Clear',command=lambda:delete()).pack(side=tk.LEFT,padx=8)
    tk.Button(search_frame, text='Add in Cart',command=lambda:listbox_selected(parent)).pack(side=tk.LEFT,padx=8)

    #search树状图
    tree = ttk.Treeview(search_frame, columns=columns, show='headings')
    # 定义表头
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # 将树形控件放置在弹窗布局中
    tree.pack(fill=tk.BOTH, expand=False, pady=10)
    tk.Label(search_frame, text='Cart').pack(side=tk.LEFT, padx=6)

     #购物车树状图
    tree1 = ttk.Treeview(search_frame, columns=columnsa, show='headings')
    # 定义表头
    for col in columnsa:
        tree1.heading(col, text=col)
        tree1.column(col, width=100, anchor="center")

    # 将树形控件放置在弹窗布局中
    tree1.pack(fill=tk.BOTH, expand=False, pady=10)

    tk.Button(search_frame, text='Order',command=lambda:order(parent)).pack(side=tk.LEFT,padx=8)
    tk.Button(search_frame, text='Delete',command=lambda:delete()).pack(side=tk.LEFT,padx=8)
    tk.Button(search_frame, text='Close',command=lambda:close()).pack(side=tk.LEFT,padx=8)
    center_window(parent, popup)

    def click():
        key_word = search_va.get()

        if key_word.strip():
            search_list = search(db, key_word)
            print(key_word)
            tree.delete(*tree.get_children())
            show(search_list)
        else:
            # Display an error message
            messagebox.showerror("Error", "The search keyword cannot be empty.")

    def show(search_list):
        # 往树状图中插入数据
        for li in enumerate(search_list):
            tuple = list(li[1])
            tree.insert('', 'end',values=(tuple[0], tuple[1], tuple[2],tuple[3], tuple[4],tuple[5],tuple[6]))

    def search(database,word):

        products = database.search_products_by_tag_value(word)
        search_list=[]
        for product in products:
            list1 = list(product.values())
            search_list.append(list1)
        return search_list

    def listbox_selected(parent):
        quantity = tk.StringVar()
        cart = tk.Toplevel(parent)
        cart.title("Create Order")
        tk.Label(cart, text="Select the quantity you want:").pack()
        tk.Spinbox(cart, from_=1, to=10, increment=1, textvariable=quantity).pack()
        tk.Button(cart, text='Add',command=lambda:add()).pack(side=tk.LEFT,padx=8)
        center_window(parent, cart)
        def add():
            selection = tree.selection()
            for item in selection:
                info=tree.item(item)['values'][0]
                tree1.insert('', 'end', values=(info,int(quantity.get())))
            cart.destroy()

    def order(parent):
        transaction_list = []
        for item in tree1.get_children():
            values = tree1.item(item)['values']
            # print( values[0]) ProductID
            # print( values[1]) Quantity
            db.insert_order(values[0], CUSTOMER_ID, values[1])

    def delete():
        selection = tree1.selection()
        tree1.delete(selection)

    def print_products_table(parent):
        all_pro= tk.Toplevel(parent)
        all_pro.title("Create Order")
        columns=('Product ID', 'Vendor ID', 'Name', 'Price', 'Tag 1', 'Tag 2','Tag 3')
        tree = ttk.Treeview(all_pro, columns=columns, show='headings')

        # 定义表头
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # 将树形控件：放置在弹窗布局中
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(all_pro, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        center_window(parent, all_pro)

        products = db.list_products()
        list=[]
        for product in products:
            list = (f"{product['ProductID']}", f"{product['VendorID']}", f"{product['Name']}", f"{product['Price']}",f"{product['Tag1']}",f"{product['Tag2']}",f"{product['Tag3']}")
            tree.insert("",tk.END,values=list)
    def close():
        popup.destroy()

def transaction_management(parent, datebase):

    all_transaction= tk.Toplevel()
    all_transaction.title("Modify Transaction")
    columns=('Transaction ID', 'Order ID', 'Shipped Date', 'Arrival Date')

    tree = ttk.Treeview(all_transaction, columns=columns, show='headings')
    tk.Button(all_transaction, text="Search", command=lambda:search_transactions(datebase, CUSTOMER_ID)).pack()
    tk.Button(all_transaction, text="Delete Transaction", command=lambda:delete_transaction(datebase)).pack()
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(all_transaction, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    center_window(parent, all_transaction)
    
    def search_transactions(datebase, customer_id):
        transactions = datebase.show_transactions_by_customer_id(customer_id)
        clear_tree()
        for transaction in transactions:
            add_transaction_to_tree(transaction)

    def clear_tree():
        tree.delete(*tree.get_children())

    def add_transaction_to_tree(transaction):
        transaction_values = (
            str(transaction['TransactionID']),
            str(transaction['OrderID']),
            str(transaction['ShippedDate']),
            str(transaction['ArrivalDate'])
        )
        tree.insert("", tk.END, values=transaction_values)

    def delete_transaction(datebase):
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            transaction_id = item["values"][0]
            datebase.delete_transaction_by_transaction_id(transaction_id)
            search_transactions(datebase, CUSTOMER_ID)

def order_management(parent, datebase):
    all_order= tk.Toplevel(parent)
    all_order.title("Modify Order")
    columns = ('Order ID', 'Product ID', 'Customer ID', 'Order Date', 'Quantity', 'Order Status')

    tree = ttk.Treeview(all_order, columns=columns, show='headings')
    tk.Button(all_order, text="Search", command=lambda:search_orders(datebase, CUSTOMER_ID)).pack()
    tk.Button(all_order, text="Modify Quantity", command=lambda:modify_order_quantity(parent, datebase)).pack()
    tk.Button(all_order, text="Cancel Order", command=lambda:cancel_order(datebase)).pack()
    tk.Button(all_order, text="Delete Order", command=lambda:delete_order(datebase)).pack()

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(all_order, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    center_window(parent, all_order)

    def search_orders(datebase, customer_id):
        orders = datebase.show_orders(customer_id)
        clear_tree()
        for order in orders:
            add_order_to_tree(order)

    def clear_tree():
        tree.delete(*tree.get_children())

    def add_order_to_tree(order):
        order_values = (
            str(order['OrderID']),
            str(order['ProductID']),
            str(order['CustomerID']),
            order['OrderDate'].isoformat(),
            order['Quantity'],
            order['OrderStatus']
        )
        tree.insert("", tk.END, values=order_values)

    def cancel_order(datebase):
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            order_id = item["values"][0]
            datebase.cancel_order(order_id)
            search_orders(datebase, CUSTOMER_ID)
            
    def delete_order(datebase):
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            order_id = item["values"][0]
            datebase.delete_order(order_id)
            search_orders(datebase, CUSTOMER_ID)

    def modify_order_quantity(parent, database):
        modify_order_window = tk.Toplevel(parent)
        modify_order_window.title("Modify Order Quantity")
        
        tk.Label(modify_order_window, text="Enter the Quantity you want to Modify:").pack()
        
        quantity_entry = tk.Entry(modify_order_window)
        quantity_entry.pack()
        
        def on_submit():
            quantity = quantity_entry.get()
            selection = tree.selection()
            
            if selection:
                item = tree.item(selection[0])
                order_id = item["values"][0]
                print(order_id)
                print(quantity)
                database.update_order_quantity(order_id, quantity)
                search_orders(database, CUSTOMER_ID)
                modify_order_window.destroy()

        submit_button = tk.Button(modify_order_window, text="Submit", command=on_submit)
        submit_button.pack()
        
        center_window(parent, modify_order_window)

def refresh_ui():
    create_menus(CUSTOMER_ID)

def create_menus(customer_id):
    menu_bar = tk.Menu(root)

    # 创建菜单栏
    menu_bar = tk.Menu(root)

    # Registration Dowpdown
    registration_menu = tk.Menu(menu_bar, tearoff=0)
    registration_menu.add_command(label="0.1. Register as a Vendor", command=lambda: add_vendor(root))
    registration_menu.add_command(label="0.2. Register as a Customer", command=lambda: add_customer(root))
    menu_bar.add_cascade(label="0. Registration", menu=registration_menu)

    # Login Dowpdown
    login_menu = tk.Menu(menu_bar, tearoff=0)
    login_menu.add_command(label="1.1. Login as a Vendor", command=lambda: login_vendor(root))
    login_menu.add_command(label="1.2. Login as a Customer", command=lambda: login_customer(root))
    menu_bar.add_cascade(label="1. Login", menu=login_menu)

    if CUSTOMER_ID is not None:
        # Vendor Dowpdown
        #vendor_menu = tk.Menu(menu_bar, tearoff=0)
        #vendor_menu.add_command(label="2.1. Add Vendor", command=lambda: add_vendor(root))
        #vendor_menu.add_command(label="2.2. Show Vendors", command=lambda: show_vendors(root, db))
        #menu_bar.add_cascade(label="2. Vendor", menu=vendor_menu)

        # Product Dowpdown
        product_menu = tk.Menu(menu_bar, tearoff=0)
        #product_menu.add_command(label="3.1. Add Product", command=lambda: add_product(root))
        product_menu.add_command(label="3.2. Show Products", command=lambda: show_products(root, db))
        product_menu.add_command(label="3.3. Search Product(s)", command=lambda: search_products(root, db))
        menu_bar.add_cascade(label="3. Product", menu=product_menu)

        # Customer Dropdown
        customer_menu = tk.Menu(menu_bar, tearoff=0)
        customer_menu.add_command(label="4.1. Add Customer", command=lambda: add_customer(root))
        customer_menu.add_command(label="4.2. Show Customers", command=lambda:show_customers(root, db))
        menu_bar.add_cascade(label="4. Customer", menu=customer_menu)

        # Product Dropdown
        order_menu = tk.Menu(menu_bar, tearoff=0)
        order_menu.add_command(label="5.1. Create Order", command=lambda: create_order(root))
        order_menu.add_command(label="5.2. Modify Transaction",command=lambda:transaction_management(root, db))
        order_menu.add_command(label="5.3. Modify Order",command=lambda: order_management(root, db))
        menu_bar.add_cascade(label="5. Order", menu=order_menu)
        
    if VENDOR_ID is not None:
        # Vendor Dowpdown
        vendor_menu = tk.Menu(menu_bar, tearoff=0)
        vendor_menu.add_command(label="2.1. Add Vendor", command=lambda: add_vendor(root))
        vendor_menu.add_command(label="2.2. Show Vendors", command=lambda: show_vendors(root, db))
        menu_bar.add_cascade(label="2. Vendor", menu=vendor_menu)

        # Product Dowpdown
        product_menu = tk.Menu(menu_bar, tearoff=0)
        product_menu.add_command(label="3.1. Add Product", command=lambda: add_product(root))
        product_menu.add_command(label="3.2. Show Products", command=lambda: show_products(root, db))
        menu_bar.add_cascade(label="3. Product", menu=product_menu)

        # Customer Dropdown
        customer_menu = tk.Menu(menu_bar, tearoff=0)
        #customer_menu.add_command(label="4.1. Add Customer", command=lambda: add_customer(root))
        customer_menu.add_command(label="4.2. Show Customers", command=lambda:show_customers(root, db))
        menu_bar.add_cascade(label="4. Customer", menu=customer_menu)

        # Product Dropdown
        #order_menu = tk.Menu(menu_bar, tearoff=0)
        #order_menu.add_command(label="5.1. Create Order", command=lambda: create_order(root))
        #order_menu.add_command(label="5.2. Modify Transaction",command=lambda:transaction_management(root, db))
        #order_menu.add_command(label="5.3. Modify Order",command=lambda: order_management(root, db))
        #menu_bar.add_cascade(label="5. Order", menu=order_menu)

    # 配置主窗口使用菜单栏
    root.config(menu=menu_bar)

# 创建主窗口
root = tk.Tk()
root.title("Comp 7640")
root.geometry("500x300")
login_status_bar = tk.Label(text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
login_status_bar.pack(side=tk.TOP, fill=tk.X)
# Initial UI setup
refresh_ui()
status_bar = tk.Label(text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)
# 运行主循环
root.mainloop()
