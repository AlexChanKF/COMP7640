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
- You have installed __MySQL__ and set up the necessary databases and tables.
- You have installed Python Library __PyMySQL__
- You have modify the `start.ps1` scripts by adding your python path
- You have a Windows machine to run `.ps1` scripts (if you're using the PowerShell script option).

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
2. Navigate to the directory where menu.py is located.
3. Run the application with the following command:

   ```bash
   python menu.py
   ```