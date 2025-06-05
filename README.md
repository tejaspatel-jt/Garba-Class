# Run with command
As multiple python version have fucked up with each other and even setting path doesn't worked... 😭
```bash
C:\Users\tejas\AppData\Local\Programs\Python\Python312\python.exe generate_id_cards_and_receipts.py
```

# Setup

### 1. Open CMD and Navigate to your project folder

```bash
cd C:\Projects\PYTHON\Garba Class
```

### 2. Create virual environment (commonly named venv):

```bash
python -m venv myenv
```

This creates a new folder `myenv` inside your project directory, containing the isolated Python environment.

### 3. Activate the virtual environment

Before running your script or installing dependencies, activate the virtual environment:

```bash
myenv\Scripts\activate
```

You’ll see `(myenv)` at the start of your command prompt, indicating the environment is active.

> ## **Note:** ⚠️ 
> You have to activate the environment everytime you want to run the project.

### 4. Install required Python libraries

If you have a requirements.txt file (common in projects), run:

```bash
pip install -r requirements.txt
```

else

```bash
pip install pandas pillow reportlab openpyxl gspread oauth2client
```

- Why these packages?
    - **pandas**: For reading Excel files.
    - **pillow**: For image processing via PIL.
    - **reportlab**: For PDF generation.
    - **openpyxl**: Required by pandas to read .xlsx Excel files (if your students.xlsx is in .xlsx format).
    - **gspread**: For interacting with Google Sheets, allowing you to read from or write to Google Sheets programmatically.
    - **oauth2client**: For authentication with Google APIs, required by gspread to securely access Google Sheets.

### 5. Running Your Project

```bash
python generate_id_cards_and_receipts.py
```

### 6. Deactivating the Virtual Environment:

When done, you can exit the virtual environment with:

```bash
deactivate
```

==========================

c:\Users\tejas\AppData\Local\Programs\cursor\resources\app\bin;C:\Program Files\Common Files\Oracle\Java\javapath;C:\Program Files (x86)\Common Files\Oracle\Java\java8path;C:\Program Files (x86)\Common Files\Oracle\Java\javapath;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\Users\tejas\AppData\Roaming\nvm;C:\Program Files\nodejs;C:\Program Files\dotnet\;C:\Program Files\Git\cmd;C:\Users\tejas\AppData\Local\jdk-11.0.2\bin;C:\Program Files\Microsoft SQL Server\150\Tools\Binn\;C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\;C:\Program Files (x86)\Microsoft SQL Server\150\Tools\Binn\;C:\Program Files\Microsoft SQL Server\150\DTS\Binn\;C:\Program Files (x86)\Microsoft SQL Server\160\DTS\Binn\;C:\Program Files\Azure Data Studio\bin;C:\Program Files (x86)\LINQPad5;C:\Users\tejas\AppData\Local\jdk-11.0.2\bin;C:\Users\tejas\AppData\Local\Programs\Python\Python312\Scripts\;C:\Users\tejas\AppData\Local\Programs\Py;C:\Users\tejas\AppData\Local\Programs\Python\Python312\;C:\Users\tejas\AppData\Local\Programs\Python\Python313\Scripts\;C:\Users\tejas\AppData\Local\Programs\Python\Python313\;C:\Users\tejas\AppData\Local\jdk-11.0.2\bin;C:\Users\tejas\AppData\Local\Programs\Python\Python312\Scripts\;C:\Users\tejas\AppData\Local\Programs\Python\Python312\;C:\Users\tejas\AppData\Local\Microsoft\WindowsApps;C:\Users\tejas\AppData\Local\Programs\Microsoft VS Code\bin;C:\Users\tejas\AppData\Roaming\nvm;C:\Program Files\nodejs;C:\Users\tejas\AppData\Local\Android\Sdk\platform-tools;C:\Users\tejas\AppData\Local\Android\Sdk\emulator;C:\Users\tejas\AppData\Local\Android\Sdk\tools;C:\Users\tejas\AppData\Local\Android\Sdk\tools\bin;C:\Users\tejas\flutter\bin;C:\Program Files\MongoDB\Server\7.0\bin;C:\Users\tejas\AppData\Local\Pub\Cache\bin;C:\Users\tejas\.dotnet\tools;C:\Program Files\Azure Data Studio\bin;C:\Program Files\nuget_cli;C:\Users\tejas\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin


# 🛠️ Python Setup ⚒️

## ❓Check if Python is Installed on Windows 🤔 ?

To verify if Python is installed on your Windows system and properly configured, follow these steps:

- ### 1. Check via Command Prompt or PowerShell

    - Open **Command Prompt** (type `cmd` in the Start menu) or **PowerShell**.
    - Run one of these commands:
        ```bash
        python --version
        ```
        or
        ```bash
        python
        ```
        **Expected Output**:
        - If Python is installed and added to your PATH, you’ll see the version (e.g., `Python 3.11.2`) or enter the Python interactive prompt.
        - If you get an error like `'python' is not recognized...`, Python is either not installed or not added to your PATH.

- ### 2. Check from the Start Menu

    - Press the **Windows key** and type `python`.
    - If Python is installed, it will appear as a best match. Right-click to see the file location.

## 🛠️ Check Installation Location & Set PATH if needed ✅

- ### 👉 Find where Python is installed ❓
    - Open cmd by `🪟 + R` > type `cmd` > hit `Enter` 
        ```bash
        where python
        ```
        **Expected Output**:
        - This displays the full path(s) to the Python executable(s)  
        e.g., `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python311\python.exe`.
        - Alternatively,  
        Check `Control Panel > Programs and Features` to see if Python is listed and view its installation path.

        #### Example
        ```bash
          ## I've multiple versions installed so it shows multiple paths😊 
          C:\Users\tejas>where python
          C:\Users\tejas\AppData\Local\Programs\Python\Python312\python.exe
          C:\Users\tejas\AppData\Local\Programs\Python\Python313\python.exe
          C:\Users\tejas\AppData\Local\Microsoft\WindowsApps\python.exe
          C:\Users\tejas>
        ```

- ### 👉 Set Python Path in Environment Variables
    - **Which Paths to Add?**:
        1.  Main Python folder:  
            `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python311\`

        2. Scripts folder:  (*contains `pip` and other utilities* )  
            `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python311\Scripts\` 

        - For system-wide installations:
          ```bash
          C:\Program Files\Python311\
          C:\Program Files\Python311\Scripts\
          ```
            Add these paths to the PATH environment variable, separated by semicolons.

## 📍Python Dependencies Installation Location on Windows 🪟

- ### How to Find the Exact Location

    - **For global or virtual environment packages**:  
        ```bash
        python -m site
        ```
    - **For user-specific packages**:  
        ```bash
        python -m site --user-site
        ```

This shows the default locations unless you've customized your Python or pip setup.

👉 When you install Python packages on Windows, they go to different locations depending on how you install them. Here's a simple breakdown:

- ### 1. Global Installations

    - **Default Python Installation**:
      - `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python<version>`
      - `C:\Program Files\Python<version>`
    - **Packages Location** (when using `pip install <package>`):
      - `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python<version>\Lib\site-packages`
      - `C:\Program Files\Python<version>\Lib\site-packages`

- ### 2. User-Specific Installations

    - **Packages Location** (when using `pip install --user <package>`):
      - `C:\Users\<YourUsername>\AppData\Roaming\Python\Python<version>\site-packages`

- ### 3. Virtual Environments

    - **Packages Location**:
      - `<your-venv-folder>\Lib\site-packages`

---

## 💣 How to Install python packages ? 💥

### `pip install pandas` vs `python -m pip install pandas`

- **`pip install pandas`**:
  - Uses the default `pip` in your system's PATH.
  - Installs to the global or user-specific location (see above) if not in a virtual environment, or to `<your-venv-folder>\Lib\site-packages` if in a virtual environment.
  - Risk: May target the wrong Python version if multiple are installed.
- **`python -m pip install pandas`**:
  - Uses the `pip` tied to the specific Python version you run (e.g., `python3.10`).
  - Installs to the same locations as above but ensures the correct Python version.
  - Recommended for clarity, especially with multiple Python installations.

---

## Git Things 🌿
```bash
# Original URL
https://github.com/tejaspatel-jt/Garba-Class

# Change origin with specific git account.
git remote set-url origin https://tejaspatel-jt@github.com/tejaspatel-jt/Garba-Class.git

# Update last Push + select branch as nothing after origin, NO master NO main 😆
git add . && git commit --amend --no-edit && git push --force origin

# update last push and last commit msg too ✅
git add . && git commit --amend -m "<MODIFIED COMMMIT MSG>" && git push --force origin
```
