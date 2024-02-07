# -*- coding: utf-8 -*-
# Example main.py
import argparse

import assignment0

def main(url):
    # Download data
    incident_data = assignment0.fetchincidents(url)

    # Extract data
    incidents = assignment0.extractincidents(incident_data)
	
    # Create new database
    db = assignment0.createdb()
	
    # Insert data
    assignment0.populatedb(db, incidents)
	
    # Print incident counts
    print(assignment0.status(db),end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
