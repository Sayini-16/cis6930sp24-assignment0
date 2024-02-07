## Crime Incidents Reporter

## Author: Anirudh Sayini

## Description of the project:

The Norman, Oklahoma police department regularly reports incidents, arrests, and other activities. This data is distributed to the public in the form of PDF files. (https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports)
The website contains three types of summaries arrests, incidents, and case summaries. In this project a function is built that collects only the incidents. And Following operations are done

- To download the data given one incident pdf
- To Extract the below fields:
  - Date / Time
  - Incident Number
  - Location
  - Nature
  - Incident ORI
- To create a SQLite database to store the data;
- To Insert the data into the database;
- To Print each nature and the number of times it appears

## Setting up the Initial installations 
We run the following installations in the project's virtual environment. Even if the installations are done in the Python environment, in the project's virtual environment, there might be an error popping up "no module named nltk"
~~~
pipenv install pyPDF2
~~~
The other packages are built-in modules, so they don't need to be installed separately rather they just have to be imported into the code.


## Packages Required for Project:

- urllib.request
- tempfile
- PyPDF2
- re
- sqlite3
\
## The Projects have below files: 
# 1. main.py 
 
assignment0.py is imported into this file and below mentioned functions will be executed by function calling. The URL will be accepted as an input argument.
\
- Data downloaded function 
  - incident_data = assignment0.fetchincidents(url)

- Data Extract function
  - incidents = assignment0.extractincidents(incident_data)

- New database creation function
  - db = assignment0.createdb()

- Insert data function
  - assignment0.populatedb(db, incidents)

- Print incident counts function
  - print(assignment0.status(db))

## 2. assignment0.py


### **fetchincidents(url)**
![image](https://github.com/Sayini-16/coursera-test/assets/81869410/557ae404-1747-407d-b455-ccb04d79338a)

`fetchincidents` takes a single parameter, `url`, which is expected to be a string representing the URL from which to fetch data. Here's a step-by-step explanation of what the function does:

1. **Custom Headers**: A dictionary named `headers` is created with a single key-value pair. The key is `'User-Agent'`, and the value is a string that mimics the user agent of a web browser. This is often done to make the request appear as if it's coming from a web browser, which can be necessary because some websites might restrict access to non-browser user agents for various reasons, such as preventing scraping.

2. **Web Request**: The `urllib.request.Request` method is used to prepare a web request. This method takes two arguments: the URL to fetch and the custom headers dictionary. The result is stored in a variable named `request`. This step doesn't actually perform the network operation; it just configures what the request will look like.

3. **Open URL**: The `urllib.request.urlopen` function is then called with the previously prepared `request` object. This function sends the request to the specified URL and returns a response object. This step is where the network operation occurs, and the function will wait (block) until the response is received or an error occurs.

4. **Read Data**: The `read` method is called on the response object returned by `urlopen`. This method reads the entire response body (the data returned by the server) and returns it as a bytes object. This is typically the HTML of a webpage, JSON, XML, or any other kind of data served by the URL.

5. **Return Data**: Finally, the data read from the response is returned to the caller of the `fetchincidents` function.

### **extractincidents(incident_data)**

![SS1](https://github.com/Sayini-16/coursera-test/assets/81869410/0e8dbe5a-7243-47c3-8d1a-97825ed7b707)
The provided code defines a function `extractincidents` designed to process PDF data, extracting incident reports and formatting them for database insertion. This explanation breaks down the code into its key operations:

1. **Temporary File Creation**: The function starts by creating a temporary file using the `tempfile.TemporaryFile()` method. This is a context manager that automatically handles the creation and deletion of the temporary file. The PDF data passed to the function (`pdf_data`) is written to this temporary file, which is then rewinded to the beginning with `tmp_file.seek(0)` for reading.

2. **PDF Reading**: It uses the `PyPDF2.PdfFileReader` class to open the temporary PDF file. `PyPDF2` is a popular Python library for working with PDF files, allowing for the extraction of text among other operations.

3. **Text Extraction and Cleaning**: The function iterates over each page of the PDF. For each page, it extracts the text using `pdf.getPage(num).extractText()` and performs several cleaning operations to remove headers and footers, and normalize the spacing. This includes removing specific header texts and replacing certain patterns with newlines or spaces to make the incident entries more distinguishable. Regular expressions (`re.sub`) are used to insert markers (`||`) before dates, facilitating the separation of individual incident reports.

4. **Parsing Incident Entries**: After cleaning the text, it splits the content into individual incident entries based on the inserted markers and newline characters. Each entry is then split again by newline characters to separate the fields of the incidents. These operations result in a list of lists, where each sub-list represents an incident report.

5. **Data Formatting**: The final part of the function formats each incident entry according to specific criteria, ensuring the data structure matches expected database schema requirements. It organizes the data based on the number of fields in each entry:
    - Entries with five fields are assumed to be complete and are added directly to the `formatted_data` list.
    - Entries with three or four fields are adjusted by adding empty strings (`''`) as placeholders where information is missing. This step ensures that each entry has a uniform structure, likely corresponding to predefined database columns such as date/time, incident number, location, nature of the incident, and the originating agency's identifier (ORI).

6. **Return Formatted Data**: Finally, the function returns `formatted_data`, a list of incident entries that are now properly formatted for database insertion. This list contains sub-lists, each representing an individual incident with its fields ready to be inserted into a database.


### **createdb()**

![SS4](https://github.com/Sayini-16/coursera-test/assets/81869410/eccff4a3-f490-4eb7-815a-24a959880926)
<br>
This code snippet is a continuation of Python code that interacts with a SQLite database named `"incident_summary.db"`. It demonstrates how to connect to a SQLite database, execute SQL commands to drop an existing table if it exists, and then create a new table. Here's a breakdown of what each part of the code does:

1. **Database Name**: The variable `database_name` is assigned a string that specifies the name of the SQLite database file. In this case, the database file is called `"incident_summary.db"`.

2. **Database Connection**:
   - `with sqlite3.connect(database_name) as conn:`: This line uses the `sqlite3.connect()` function to establish a connection to the SQLite database specified by `database_name`. The `with` statement ensures that the connection is automatically closed when the block of code inside it completes, which is a good practice to manage resources efficiently. The `conn` variable represents the database connection.
   
3. **Cursor Creation**:
   - `cursor = conn.cursor()`: A cursor object is created using the `cursor()` method of the connection object. The cursor is used to execute SQL commands.

4. **Drop Table If Exists**:
   - `cursor.execute('DROP TABLE IF EXISTS incident')`: This SQL command checks if a table named `incident` already exists in the database. If it does, the table is dropped (deleted). This is often done to start fresh with a new table structure or to clear old data.

5. **Create Table**:
   - `cursor.execute('CREATE TABLE incident (Time TEXT, incident_Number TEXT, location TEXT, nature TEXT, incident_ORI TEXT);')`: This SQL command creates a new table named `incident` with five columns: `Time`, `incident_Number`, `location`, `nature`, and `incident_ORI`. Each column is defined to store text (`TEXT`), which can hold any character data.

6. **Return Statement**:
   - `return database_name`: After executing the SQL commands to drop the existing table (if any) and create a new one, the function (from which this snippet seems to be a part) returns the name of the database. This might be used to confirm the operation's success or for subsequent operations that require the database name.

### **populatedb(db_name, incidents)**

The list from extractincidents() and  db name from createdb() is passed as input parameters to **populatedb()**,

![SS5](https://github.com/Sayini-16/coursera-test/assets/81869410/ecc01acd-3f72-4fe2-97a3-1b63039fd26a)
<br>
This code defines a Python function named `populatedb` that takes two parameters: `database_name`, a string representing the name of a SQLite database file, and `incident_records`, a list of tuples where each tuple represents a record to be inserted into the `incident` table in the database. Here's a detailed explanation of what the function does:

1. **Connect to SQLite Database**: 
   - `with sqlite3.connect(database_name) as conn:`: This line establishes a connection to the SQLite database specified by `database_name`. The `with` statement ensures that the connection is properly closed after the operations are completed, even if an error occurs. This is a context manager that handles the opening and closing of the database connection.

2. **Create a Cursor Object**: 
   - `cursor = conn.cursor()`: A cursor object is created from the connection. This cursor is used to execute SQL commands.

3. **Insert Records into the Database**: 
   - `cursor.executemany("INSERT INTO incident VALUES (?,?,?,?,?)", incident_records)`: This command uses the `executemany` method of the cursor object, which is designed to execute an SQL command against all parameters that are provided in `incident_records`. The `INSERT INTO` SQL command adds new rows to the `incident` table. The `VALUES (?,?,?,?,?)` part of the command is a placeholder for the values to be inserted into each column of the table for each record. The `incident_records` parameter should be a list of tuples, where each tuple contains five elements corresponding to the five columns in the `incident` table (`Time`, `incident_Number`, `location`, `nature`, `incident_ORI`).

4. **Return the Number of Records Inserted**: 
   - `return len(incident_records)`: After all records have been inserted into the database, the function returns the number of records inserted. This is simply the length of the `incident_records` list, which represents the number of tuples (records) provided to the function for insertion.

This function does not explicitly handle errors, such as what might occur if the database connection fails, if the `incident` table does not exist, or if there are any issues with the data in `incident_records`. Depending on the application, you might need to add error handling to manage such cases.

### **status(db)**

![SS6](https://github.com/Sayini-16/coursera-test/assets/81869410/c9dfa2e2-d4d8-4496-8ed1-1652fba96039)
<br>
The `status` function connects to a SQLite database specified by the `database_name` parameter, queries the `incident` table to calculate statistics on incidents grouped by their nature, and then generates a summary of these statistics. Here's a detailed breakdown of the function's operations:

1. **Database Connection**: 
   - The function starts by establishing a connection to the SQLite database using `sqlite3.connect(database_name)`. This connection is managed using a `with` statement, ensuring that the connection is properly closed after the operations within the block are completed. However, the explicit call to `conn.close()` at the end of the function is redundant because the `with` statement automatically takes care of closing the connection.

2. **Execute Query**:
   - A cursor object is created from the connection to execute SQL commands.
   - The function executes an SQL query using `cursor.execute()`. This query selects the nature of incidents and counts how many incidents there are of each nature by using `COUNT(*)`. It groups the results by the nature of the incidents (`GROUP BY nature`) and orders the results first by the count in descending order (`ORDER BY count DESC`) and then by the nature alphabetically. This ensures that the most frequent incident types are listed first, and within each frequency, types are listed alphabetically.

3. **Fetching Query Results**:
   - The `fetchall()` method is used to retrieve all rows of the query result. Each row in the result set contains the nature of the incident and the count of incidents of that nature.

4. **Summarize Results**:
   - The function initializes a summary string with headers "Nature|Count\n" for readability.
   - It calculates the total number of incidents by summing the second element (`count`) of each row in the query result.
   - Then, it iterates over each row in the query result, appending the nature and count of each incident type to the summary string in the format "nature|count\n".

5. **Return Summary**:
   - The function returns the summary string, which contains a formatted list of incident types and their counts, sorted by frequency and nature.

Note:
- The explicit `conn.close()` is not necessary due to the use of the `with` statement, as mentioned.
- The commented-out `print(total_incidents)` line suggests there was or could be an intention to debug or display the total number of incidents directly, but it's currently inactive due to being commented out.
- The function effectively provides a summary of incidents grouped by their nature, which could be useful for reporting or analyzing the types of incidents that occur most frequently.

## Pytest framework for the project :
I used the Pytest framework in Python to check for the individual test cases. To run the pytest framework, we need to first ensure if we have the pytest installed in our current project directory. I used the following command to install the pytest in my project's execution virtual environment.
~~~
pipenv install pytest
~~~

## 3.test_project0.py

The test_project0.py file contains the unit testcases to test each method of project0.py if it is working are not, in this file we written the below 5 testcases to test each method.
Below are imported for this file
- pytest
- NoneType from types
- os
- io
- sqlite3
- project0
<br>
In tests folder I attached a pdf file called sample.pdf to test my functions.

![SS7](https://user-images.githubusercontent.com/96924488/157276897-8e529aa1-cbc9-4147-b1de-97d02a14ff88.png)

<br>
os. getcwd() returns the absolute path of the working directory where Python is currently running as a string str.
So from the command

<br>

return os.path.join(cwd, 'tests', 'sample.pdf')
<br>
it returns the path to sample.pdf file from tests directory in the current directory

### **test_fetchincidents():**
<br>

![SS8](https://github.com/Sayini-16/coursera-test/assets/81869410/06a38162-56cb-4aba-84ee-623e1ab28622)
The `test_fetchincidents` function appears to be a test function, likely designed to test the functionality of a `fetchincidents` function from a module or assignment labeled `assignment0`. The test specifically checks that the `fetchincidents` function can fetch data from a file and that the data fetched is in bytes format. Here's a breakdown of the function and what each part does:

1. **Function Description**: The purpose of the `test_fetchincidents` function is to test the `fetchincidents` function from `assignment0`. It ensures that `fetchincidents` can correctly fetch data from a specified file and that the fetched data is of the correct type (`bytes`).

2. **Fetching Data**:
   - The function takes a single parameter, `sample_incident_file`, which is expected to be the path to a sample PDF file used for testing.
   - It then constructs a file URI by concatenating `'file:\\'` with the `sample_incident_file` path. This URI is passed to `assignment0.fetchincidents`, which is called to fetch the data from the file.

3. **Assertion**:
   - After fetching the data, the function checks that the returned data is in bytes format. This is done using the `assert` statement with the condition `isinstance(file_data, bytes)`, which verifies that `file_data` is an instance of the `bytes` class.

### **test_extractincidents():**

![SS9](https://github.com/Sayini-16/coursera-test/assets/81869410/c85c364c-0986-4b58-82b7-83c876347bad)
<br>
The `test_extractincidents` function is designed to test the `extractincidents` function from a module or assignment labeled `assignment0`. It verifies that the `extractincidents` function correctly processes a sample PDF file and extracts a specific number of records, in this case, 337 records. Here's a detailed explanation of the function and its components:

1. **Opening the Sample PDF File**:
   - The function takes a single parameter, `sample_incident_file`, which is expected to be the path to a sample PDF file used for testing.
   - It opens this file in binary read mode (`'rb'`). Opening a file in binary mode is necessary for PDF files since they contain binary data, not just plain text.
   - The `with` statement is used to ensure that the file is properly closed after its contents have been read, even if an error occurs during the file operations.

2. **Reading and Extracting Data**:
   - `sample_fp.read()` reads the entire content of the file into memory as a bytes object.
   - This data is then passed to `assignment0.extractincidents`, which is expected to process the PDF content and extract incident records from it. The specifics of how `extractincidents` works are not detailed here, but it presumably analyzes the structure and content of the PDF to identify and extract data related to incidents.

3. **Assertion**:
   - After extracting the data, the function asserts that the number of records extracted is exactly 337 with `assert len(data) == 337`. This assertion checks the length of the returned data structure (presumably a list or similar iterable) against the expected number of records. If the number of records does not match the expected count, the assertion will fail, indicating a potential issue with the `extractincidents` function's ability to accurately process the file and extract the correct number of records.

### **test_createdb():**

![SS10](https://github.com/Sayini-16/coursera-test/assets/81869410/19a00f81-1bbd-442b-8e17-8567da5bf38b)
<br>
The `test_createdb` function is designed to test the database creation functionality, presumably of a `createdb` function from a module or assignment labeled `assignment0`. This test checks whether a database file is successfully created or opened and verifies that no changes have been made to the database upon creation. Here's a step-by-step explanation of how the function works:

1. **Specify Database Name**:
   - The variable `db_name` is assigned the name of the database file to be created or opened, in this case, `"incident.db"`.

2. **Call the `createdb` Function**:
   - The `createdb` function from `assignment0` is called with `db_name` as its argument. This function is expected to either create a new SQLite database file with the specified name if it doesn't already exist or open it if it does. The function then returns the name of the database, which is reassigned to `db_name` to ensure any modifications made by `createdb` are captured.

3. **Construct Full Path to Database File**:
   - The `os.path.join(os.getcwd(), db_name)` statement constructs the full path to the database file by joining the current working directory (`os.getcwd()`) with the database name. This step is crucial for verifying the existence of the file in the file system, as the assertion that follows uses the full path.

4. **Assert Database File Exists**:
   - The `assert os.path.exists(db_path) is True` statement checks that the database file exists at the path specified by `db_path`. If the file does not exist, the assertion will fail, indicating that the `createdb` function did not successfully create the database file.

5. **Connect to the Database**:
   - The code then connects to the newly created or opened database using `sqlite3.connect(db_name)`. This connection is stored in the variable `connection`.

6. **Assert No Changes Made**:
   - Finally, the function asserts that no changes have been made to the database upon creation by checking `connection.total_changes == 0`. The `total_changes` attribute of the SQLite connection object returns the number of database rows that have been modified, inserted, or deleted since the database connection was opened. If this value is not 0, it would indicate that some operations have unexpectedly altered the database.

### **test_populatedb( ):**

![SS11](https://user-images.githubusercontent.com/96924488/157277066-8a4f6117-6794-474d-b636-d9aa26a3ef1e.png)
<br>
In this method we test the **populated()** method, few incidents will be pushed into the database. populate_db method will return the count of total changes, so this count will be taken after inserting the data and this is compared with length of the incidents that I pushed into the table, if both are same then the test case is passed. Finally the path to the database will be removed.

## **test_status( ):**

In this method we test the **status()** method.
<br>
 ![SS12](https://user-images.githubusercontent.com/96924488/157277117-c3821d7e-5670-491d-8e92-c2cb24d61d62.png)
<br>
Like previous function, incidents data will be pushed into the database. Then populatedb method will be executed on it, it will give a result and that result is compared with result that we already expect, and if they both are same test case will be passed.

## To run the Pytest : 
I used the following command to run my python tests for the given function.
~~~
 pipenv run python -m pytest
~~~

## 4.Assumptions/Bugs:

- In this project we assumed that only location and nature columns have missing values in the pdf document and we handled only the missing values in those columns, if any other column has the missing values in the pdf the code will fail. 
- After splitting the data by date the maximum length of the list we observed is 7, if the length of list is > 7 then the code may fail in this case.
- I assumed that among location and nature, if my data gives only list of length 4 then nature column is missing, this assumption is made after looking into the files, but if location is missed instead of nature then this code will fail.


## Steps to Run project0

- **Step1** \
clone the project directory using below command 
> git clone  https://github.com/VarshithaCVasireddy/Crime_Incidents_Reporter

- **Step2** \
Navigate to directory that we cloned from git and run the below command to install dependencies

> pipenv install

- **Step3** \
Then run the below command by providing URL

> pipenv run python project0/main.py --incidents **URL**

- **Step4** 

Then run the below command to test the testcases. 

> pipenv run python -m pytest -v

