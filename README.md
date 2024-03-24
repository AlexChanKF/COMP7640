# COMP7640 Group Assignment Project - Group 27

This application is a __command-line interface__ for a multi-vendor e-commerce platform, developed using __Python 3.5__ and __MySQL__. It is designed to provide a personalized user experience, allowing users to navigate through various vendor offerings, manage their shopping cart, and complete purchases. The focus is on simplicity and efficiency, enabling users to perform e-commerce operations via a text-based interface.

## Group Information

1. Group No.: 27
2. Group Members:

| Name          | Student ID | Email                         |
|---------------|------------|-------------------------------|
| FU Jiehao     | 23412852   | 23412852@life.hkbu.edu.hk     |
| LI Jingyi     | 23470372   | 23470372@life.hkbu.edu.hk     |
| TONG Ka Chun  | 23473355   | 23473355@life.hkbu.edu.hk     |
| CHAN Ka Fai   | 22450920   | 22450920@life.hkbu.edu.hk     |
| CHAU Ka Fai   | 23473347   | 23473347@life.hkbu.edu.hk     |

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed __Python 3.5__ on your computer.
- You have installed Python Library __PyMySQL__.
- You have installed __MySQL v8.0__.
- The default schema of __MySQL__ is __comp7640__.
- You have created tables and records according to `SQL\CreateTable.txt` and `SQL\InsertRecords.txt`. Please refer to the below topic `Creating Schema, Tables, Inserting Records`.
- You have modify the `config.ini` scripts by using your mysql account and password. Please refer to the below topic `Modifying the "config.ini" Script`.
- You have modify the `start.ps1` scripts by adding your python path. Please refer to the below topic `Modifying the "start.ps1" Script`.
- You have a Windows machine to run `.ps1` scripts (if you're using the PowerShell script option).

## Creating Schema, Tables, Inserting Records
Before running the application, you need to create schema, tables and insert records.
For more information, Please refer to `HowToInsertTablesAndRecords.mp4`.

## Modifying the `config.ini` Script
Before running the application, you need to modify the `config.ini` script to your MySQL account and password. Follow these steps to modify the script:

1. Locate the `config.ini` script script in the root directory of the project.
2. Right-click on the script and choose "Edit" to open it in a text editor.
3. Find the line that looks something like this:

   ```
   [mysql]
   host = localhost
   user = YourAccount
   password = YourPassword
   database = comp7640
   ```
   
4. Replace __user__ and __password__.
5. Save the changes and close the text editor.

## Modifying the `start.ps1` Script

Before running the application, you need to point the `start.ps1` script to your Python 3.5 installation. Follow these steps to modify the script:

1. Locate the `start.ps1` script in the root directory of the project.
2. Right-click on the script and choose "Edit" to open it in a text editor.
3. Find the line that looks something like this:

   ```powershell
   # !!! MODIFY YOUR PYTHON PATH !!!
   $customPythonPath = "C:\Users\User\OneDrive\Software\Python\Python-3.5\python.exe"
   ```
4. Replace C:\Users\User\OneDrive\Software\Python\Python-3.5\python.exe with the actual path to your Python 3.5 executable.
5. Save the changes and close the text editor.

## Running the Application

You can start the application using one of the following methods:

### Option 1: Using the PowerShell Script (Recommended)

1. Open PowerShell
2. Navigate to the directory where `start.ps1` is located.
3. Execute the script by running the following command:

   ```powershell
   .\start.ps1
   ```

### Option 2: Using the Command
1. Open a command prompt or terminal window.
2. Navigate to the directory where gui.py is located.
3. Run the application with the following command:

   ```bash
   python gui.py
   ```
   
   
## Functionalities are implemented

### Registration

- **Register as a Vendor**: Done (0. Registration Tab > 0.1. Register as a Vendor)

- **Register as a Customer**: Done (0. Registration Tab > 0.2. Register as a Customer)

### Login

- **Login as a Vendor**: Done (1. Login Tab > 0.1. Login as a Vendor)

- **Login as a Customer**: Done (1. Login Tab > 1.2. Login as a Customer)

### Vendor Administration

- **Display a List of All Vendors**: Done (2. Vendor Tab > 2.2. Show Vendors)

- **Onboard New Vendors**: Done (0. Registration Tab > 0.1. Register as a Vendor)

### Product Catalog Management

- **Browse Products by Vendor**: Done (3. Product Tab > 3.2. Show Products)

- **Introduce New Products**: Done (3. Product Tab > 3.1. Add Product)

### Product Discovery

- **Tag-Based Search Feature**: Done (3. Product Tab > 3.3. Search Product(s))

### Product Purchase (Customer Only)

- **Purchase Support**: Done (5. Order Tab > 5.1. Create Order > Search Products > Select Product > Click "Add In Cart" > Input "Quantity" and then "Add" > Order > Input CustID > Submit Order)

- **Transaction Recording**: Done (5.1 Order Tab > 5.2. Modify Transaction)

### Order Modification

- **Removing Specific Products**: Done (5.1 Order Tab > 5.3. Modify Order > Search > Delete)

- **Cancelling Entire Orders**: Done (5.1 Order Tab > 5.3. Modify Order > Search > Cancel)

