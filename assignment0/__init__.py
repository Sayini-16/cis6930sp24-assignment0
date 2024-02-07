import urllib.request
import tempfile
import PyPDF2
import re
import os
import sqlite3

def fetchincidents(url):
    # Custom headers to mimic a web browser request.
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    # Perform the web request with the specified headers.
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    return data

def extractincidents(pdf_data):
    # Initialize a temporary file to sto    re PDF data.
    with tempfile.TemporaryFile() as tmp_file:
        tmp_file.write(pdf_data)
        tmp_file.seek(0)
        
        # Open the temporary PDF file and prepare to read it.
        pdf = PyPDF2.PdfFileReader(tmp_file)
        incidents = []
        
        # Iterate through each page of the PDF.
        for num in range(len(pdf.pages)):
            text = pdf.getPage(num).extractText()
            text = text.replace("Date / Time Incident Number Location Nature Incident ORI", "").replace("Daily Incident Summary (Public)", "").replace("NORMAN POLICE DEPARTMENT", "\n").replace(" \n", " ")
            # Use regular expression to better separate each incident entry.
            text = re.sub('\n(\\d?\\d/\\d?\\d/\\d{4} )', r'\n||\1', text)
            entries = [entry.split('\n') for entry in text.strip().split('\n||')]
            incidents.extend(entries)

    # Adjust data entries to match database schema requirements.
    formatted_data = [entry for entry in incidents if len(entry) == 5]
    formatted_data += [[entry[0], entry[1], '', '', entry[2]] for entry in incidents if len(entry) == 3]
    formatted_data += [[entry[0], entry[1], entry[2], '', entry[3]] for entry in incidents if len(entry) == 4]
    formatted_data.pop(0)
    
    return formatted_data

def createdb():
    database_name = os.path.join("resources","normanpd.db")
    # Establish a new database connection.
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS incident')
        cursor.execute('CREATE TABLE incident (Time TEXT, incident_Number TEXT, location TEXT, nature TEXT, incident_ORI TEXT);')
    return database_name

def populatedb(database_name, incident_records):
    # Connect to the specified SQLite database.
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO incident VALUES (?,?,?,?,?)", incident_records)
    return len(incident_records)

def status(database_name):
    # Connect to database and calculate incident statistics.
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        query_result = cursor.execute("SELECT nature, COUNT(*) as count FROM incident GROUP BY nature ORDER BY count DESC, nature").fetchall()
    
    summary = ""
    total_incidents = sum([row[1] for row in query_result])
    for nature, count in query_result:
        if nature != None :
            summary += f"{nature}|{count}\n"
    #print(total_incidents)
        
    conn.close()

    return summary

