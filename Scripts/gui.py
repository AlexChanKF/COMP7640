import tkinter as tk
import os
from database import Database
from db_config import read_db_config
from tkinter import ttk
from tkinter import messagebox

db_config = read_db_config()
db = Database(**db_config)

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

#Vendor
def get_vendor_info(parent):

    popup = tk.Toplevel(parent)
    popup.title("Add Vendor")

    # 添加标签和输入框
    tk.Label(popup, text="Enter the business name of the vendor:").pack()
    business_entry = tk.Entry(popup)
    business_entry.pack()

    tk.Label(popup, text="Enter the customer feedback score of the vendor [0-100]:").pack()
    customer_score = tk.Entry(popup)
    customer_score.pack()

    tk.Label(popup, text="Enter the geographical presence of the vendor [HK,JP,TW]: ").pack()
    geographical_entry = tk.Entry(popup)
    geographical_entry.pack()

    # 提交按钮
    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_info())
    submit_button.pack()
    center_window(parent, popup)

    # 提交按钮的功能
    def submit_info():
        business_name = business_entry.get()
        customer_feedback_score = customer_score.get()
        geographical_presence = geographical_entry.get()
        db.insert_vendor(business_name, customer_feedback_score, geographical_presence)

        # 关闭弹窗
        popup.destroy()

def add_products(parent):
    popup = tk.Toplevel(parent)
    popup.title("Add Product")

    # 添加标签和输入框
    tk.Label(popup, text="Enter the VendorID of the product:").pack()
    vendor_entry = tk.Entry(popup)
    vendor_entry.pack()

    tk.Label(popup, text="Enter the name of the product:").pack()
    productname_entry = tk.Entry(popup)
    productname_entry.pack()

    tk.Label(popup, text="Enter the price of the product:").pack()
    price_entry = tk.Entry(popup)
    price_entry.pack()

    tk.Label(popup, text="Enter the Tag1:").pack()
    Tag1_entry= tk.Entry(popup)
    Tag1_entry.pack()

    tk.Label(popup, text="Enter the Tag2 ").pack()
    Tag2_entry = tk.Entry(popup)
    Tag2_entry.pack()

    tk.Label(popup, text="Enter the Tag3 ").pack()
    Tag3_entry = tk.Entry(popup)
    Tag3_entry.pack()

    # 提交按钮
    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_info())
    submit_button.pack()
    center_window(parent, popup)

    # 提交按钮的功能
    def submit_info():
        vendorID=vendor_entry.get()
        product_name = productname_entry.get()
        price = price_entry.get()
        Tag1 = Tag1_entry.get()
        Tag2 = Tag2_entry.get()
        Tag3 = Tag3_entry.get()
        db.insert_product(vendorID,product_name, price,Tag1, Tag2 ,Tag3)

        # 关闭弹窗
        popup.destroy()

def show_vendors(parent, database):
    # 创建弹窗
    db_window = tk.Toplevel(parent)
    db_window.title("Vendor Database")

    # 设置树形控件以显示表格数据
    columns = ("VendorID","BusinessName", "CutomerFeedbackScore", "GeographicalPresence")
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

#Customer
def get_customer_info(parent):
    popup = tk.Toplevel(parent)
    popup.title("输入信息")

    # 添加标签和输入框
    tk.Label(popup, text="Enter the phone number: ").pack()
    contact_number_entry = tk.Entry(popup)
    contact_number_entry.pack()

    tk.Label(popup, text="Enter the shipping details:").pack()
    shipping_details_entry = tk.Entry(popup)
    shipping_details_entry.pack()
    # 提交按钮
    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_info())
    submit_button.pack()
    center_window(parent, popup)

    # 提交按钮的功能
    def submit_info():
        contact_number=contact_number_entry.get()
        shipping_details=shipping_details_entry.get()
        db.insert_customer(contact_number, shipping_details)
     # 关闭弹窗
        popup.destroy()

def show_customers(parent, database):
    # 创建弹窗
    db_window = tk.Toplevel(parent)
    db_window.title("Customer Database")

    # 设置树形控件以显示表格数据
    columns = ("CutomerID","ContactNumber", "ShippingDetails")
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
        print (list)
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
    columns = ("ProductID","VendorID", "Name", "Price","Tag1","Tag2","Tag3")
    columnsa = ("ProductID","Quantity")
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
        cart.title("Creat Order")
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
        customer = tk.StringVar()
        order_pop = tk.Toplevel(parent)
        order_pop.title("Creat Order")
        transaction_list = []
        tk.Label(order_pop, text="Enter your customer ID:").pack()
        tk.Entry(order_pop,textvariable=customer).pack()
        submit_button = tk.Button(order_pop, text='Submit', command=lambda: submit_order())
        submit_button.pack(side=tk.LEFT, padx=8)
        center_window(parent, order_pop)
        def submit_order():
            for item in tree1.get_children():
                values = tree1.item(item)['values']
                if values:
                    transaction_list.append(values)
            print(transaction_list,customer.get())
            db.insert_order(customer.get(), transaction_list)
            order_pop.destroy()

    def delete():
        selection = tree1.selection()
        tree1.delete(selection)

    def print_products_table(parent):

        all_pro= tk.Toplevel(parent)
        all_pro.title("Creat Order")
        columns=('ProductID', 'VendorID','Name','Price', 'Tag1', 'Tag2','Tag3')

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

def order_modified(parent, datebase):

    all_order= tk.Toplevel()
    all_order.title("Modify Transaction")
    columns=('TransactionID', 'OrderID','CustomerID','ProductID', 'Quantity', 'Date')

    tree = ttk.Treeview(all_order, columns=columns, show='headings')
    tk.Button(all_order, text="Choose", command=lambda:modify_info(parent)).pack()
    tk.Button(all_order, text="Delete", command=lambda:delete_transaction(parent)).pack()

# 定义表头
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")


    # 将树形控件：放置在弹窗布局中
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(all_order, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    transitions = datebase.list_transition()
    list=[]
    for transition in transitions:
        list = (f"{transition['TransactionID']}", f"{transition['OrderID']}", f"{transition['CustomerID']}", f"{transition['ProductID']}",f"{transition['Quantity']}",f"{transition['Date']}")
        tree.insert("",tk.END,values=list)
    center_window(parent, all_order)

    def modify_info(parent):

        mod_order= tk.Toplevel(parent)
        tk.Label(mod_order, text="Enter the TrasactionID:").pack()
        TransactionID_entry=tk.Entry(mod_order)
        TransactionID_entry.pack()
        tk.Label(mod_order, text="Enter the OrderID:").pack()
        OrderID_entry=tk.Entry(mod_order)
        OrderID_entry.pack()
        tk.Label(mod_order, text="Enter the CustomerID:").pack()
        CustomerID_entry=tk.Entry(mod_order)
        CustomerID_entry.pack()
        tk.Label(mod_order, text="Enter the Quantity you want to Modified:").pack()
        Quantity_entry=tk.Entry(mod_order)
        Quantity_entry.pack()
        tk.Button(mod_order, text="Submit", command=lambda:modify_submit()).pack()
        center_window(parent, mod_order)

        def modify_submit():
            TransactionID = TransactionID_entry.get()
            CustomerID = CustomerID_entry.get()
            OrderID =OrderID_entry.get()
            Quantity = Quantity_entry.get()
            db.update_transaction(OrderID,CustomerID,TransactionID,Quantity)
            mod_order.destroy()

    def delete_transaction(parent):
        del_order= tk.Toplevel(parent)
        tk.Label(del_order, text="Enter the TrasactionID:").pack()
        TransactionID_entry=tk.Entry(del_order)
        TransactionID_entry.pack()
        tk.Label(del_order, text="Enter the OrderID:").pack()
        OrderID_entry=tk.Entry(del_order)
        OrderID_entry.pack()
        tk.Label(del_order, text="Enter the CustomerID:").pack()
        CustomerID_entry=tk.Entry(del_order)
        CustomerID_entry.pack()
        tk.Button(del_order, text="Submit", command=lambda:del_submit()).pack()
        center_window(parent, del_order)

        def del_submit():
            TransactionID = TransactionID_entry.get()
            CustomerID = CustomerID_entry.get()
            OrderID =OrderID_entry.get()
            db.delete_transaction(OrderID,CustomerID,TransactionID)
            del_order.destroy()

def order_delete(parent):
    all_order= tk.Toplevel(parent)
    all_order.title("Modify Order")
    columns=('OrderID','CustomerID','OrderDate', 'OrderStatus')

    tree = ttk.Treeview(all_order, columns=columns, show='headings')
    tk.Button(all_order, text="Search", command=lambda:search_order(parent)).pack()
    tk.Button(all_order, text="Delete", command=lambda:delete_order()).pack()

# 定义表头
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")


    # 将树形控件：放置在弹窗布局中
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(all_order, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    center_window(parent, all_order)

    def search_order(parent):
        src_order= tk.Toplevel(parent)
        src_order.title("Modify Transaction")
        tk.Label(src_order, text="Enter the CusID:").pack()
        CusID_entry=tk.Entry(src_order)
        CusID_entry.pack()
        tk.Button(src_order, text="Submit", command=lambda:modify_order()).pack()
        center_window(parent, src_order)
        def modify_order():
            orders=db.show_orders(CusID_entry.get())
            list=[]
            for order in orders:
                list = (f"{order['OrderID']}", f"{order['CustomerID']}", f"{order['OrderDate']}", f"{order['OrderStatus']}")
                tree.insert("",tk.END,values=list)
            src_order.destroy()


    def delete_order():
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            first_column_value = item["values"][0]
            db.cancel_order(first_column_value)
            tree.delete(*tree.selection())

# 创建主窗口
root = tk.Tk()
root.title("Comp 7640")
root.geometry("500x300")

# 创建菜单栏
menu_bar = tk.Menu(root)


# Vendor Dowpdown
vendor_menu = tk.Menu(menu_bar, tearoff=0)
vendor_menu.add_command(label="1. Add Vendor", command=lambda: get_vendor_info(root))
vendor_menu.add_command(label="2. Add Product", command=lambda: add_products(root))
vendor_menu.add_command(label="3. Show Vendors", command=lambda: show_vendors(root, db))
menu_bar.add_cascade(label="Vendor", menu=vendor_menu)


# Customer Dropdown
cus_menu = tk.Menu(menu_bar, tearoff=0)
cus_menu.add_command(label="1. Add Customer", command=lambda: get_customer_info(root))
cus_menu.add_command(label="2. Show Customers", command=lambda:show_customers(root, db))
menu_bar.add_cascade(label="Customer", menu=cus_menu)

# Product Dropdown
poc_menu = tk.Menu(menu_bar, tearoff=0)
poc_menu.add_command(label="1. Create Order", command=lambda: create_order(root))
poc_menu.add_command(label="2. Modify Order",command=lambda:order_modified(root, db))
poc_menu.add_command(label="3. Show Order",command=lambda: order_delete(root))
menu_bar.add_cascade(label="Order", menu=poc_menu)

# 配置主窗口使用菜单栏
root.config(menu=menu_bar)

# 运行主循环
root.mainloop()
