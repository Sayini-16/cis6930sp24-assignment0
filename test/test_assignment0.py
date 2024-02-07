import pytest
import os
import sqlite3
import sys
# Add the project directory to sys.path to ensure local modules can be imported
sys.path.append('C:/Users/aniru/Desktop/DE/project0')

import assignment0

# Pytest fixture to provide a sample PDF file path for tests
@pytest.fixture
def sample_incident_file():
    # Get the current working directory
    cwd = os.getcwd()
    # Return the absolute path of the sample.pdf file within the test directory
    return os.path.join(cwd, 'test', 'sample.pdf')

# Test the function responsible for fetching incident data from a PDF file
def test_fetchincidents(sample_incident_file):
    # Use assignment0's fetchincidents function to get data from the sample PDF file
    file_data = assignment0.fetchincidents('file:\\' + sample_incident_file)
    # Assert that the fetched data is in bytes format
    assert isinstance(file_data, bytes)

# Test the function that extracts incident records from raw PDF data
def test_extractincidents(sample_incident_file):
    # Open the sample PDF file in binary read mode and read its contents
    with open(sample_incident_file, 'rb') as sample_fp:
        data = assignment0.extractincidents(sample_fp.read())
        # Assert that the extracted data contains exactly 337 records
        assert len(data) == 336

# Test the database creation functionality
def test_createdb():
    # Specify the database name
    db_name="incident.db"
    # Call the createdb function from assignment0, creating or opening the database
    db_name = assignment0.createdb()
    # Construct the full path to the database file
    db_path = os.path.join(os.getcwd(), db_name)
    # Assert that the database file exists in the file system
    assert os.path.exists(db_path) is True
    # Connect to the database and assert no changes have been made yet
    connection = sqlite3.connect(db_name)
    assert connection.total_changes == 0

# Test the functionality to populate the database with incident records
def test_populatedb():
    # Name of the test database
    testdb = 'test_database2.db'
    # Sample incident records to insert into the database
    incidents = [
        ['1/4/2024 13:30', '2024-00000823','','','OK0140200'],
        ['1/4/2024 14:46', '2024-00000842','1189 BALD EAGLE DR', 'Traffic Stop', 'OK0140200'],
        ['1/4/2024 14:58', '2024-00000846', '290 34TH AVE SW','Traffic Stop','OK0140200']
    ]
    # Create or open the test database
    conn = assignment0.createdb()
    # Populate the database with the sample incidents and get the number of changes (inserted records)
    change_count = assignment0.populatedb(conn, incidents)
    # Assert that the number of records inserted matches the number of incidents provided
    assert change_count == len(incidents)

# Test the function that retrieves and formats the status of incidents in the database
def test_status():
    # Name of another test database
    testdb = 'test_database3.db'
    # Another set of sample incident records
    incidents = [
        ['1/4/2024 13:30', '2024-00000823','','','OK0140200'],
        ['1/4/2024 14:46', '2024-00000842','1189 BALD EAGLE DR', 'Traffic Stop', 'OK0140200'],
        ['1/4/2024 14:58', '2024-00000846', '290 34TH AVE SW','Traffic Stop','OK0140200']
    ]
    # Create or open the database and populate it with incidents
    conn = assignment0.createdb()
    assignment0.populatedb(conn, incidents)
    # Retrieve the status of incidents in the database
    actual = assignment0.status(conn)
    # Expected status format to find in the actual output
    expected = 'Traffic Stop|2'
    # Assert that the expected status is part of the actual status output
    assert expected in actual
