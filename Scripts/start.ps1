# start.ps1

# !!! MODIFY YOUR PYTHON PATH !!!
$customPythonPath = "C:\Users\User\OneDrive\Software\Python\Python-3.11\python.exe"

# Function to find Python executable
function Find-Python {
    $pythonExe = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonExe -ne $null) {
        return $pythonExe.Source
    }
    $pythonExe = Get-Command python3.exe -ErrorAction SilentlyContinue
    if ($pythonExe -ne $null) {
        return $pythonExe.Source
    }
    return $null
}

# Attempt to find Python executable
$pythonPath = Find-Python

if ($pythonPath -ne $null) {
    # Run menu.py with the located Python executable
    & $pythonPath "menu.py"
} elseif ($customPythonPath -ne $null) {
    # Run menu.py with the located Python executable
	& $customPythonPath "menu.py"
} else {
    Write-Error "Python executable not found. Please install Python or add it to your PATH."
    # Optionally, open a browser to the Python download page
    Start-Process "https://www.python.org/downloads/"
}