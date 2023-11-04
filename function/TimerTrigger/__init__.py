import datetime
import logging
import requests
import csv
import pandas as pd
import azure.functions as func
import psycopg2
from azureproject.production import DATABASE_URI

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    url = 'https://data.sfgov.org/api/views/rqzj-sfat/rows.csv'
    response = requests.get(url)

    with open('Mobile_Food_Facility_Permit.csv', 'w', newline='') as csvfile:
        csvfile.write(response.text)
    
    logging.info('CSV file created succesfully.')

    df = pd.read_csv('Mobile_Food_Facility_Permit.csv')

    # Transform the data to match the FoodTruck class
    df = df.rename(columns={
        'Applicant': 'name',
        'Address': 'address',
        'ExpirationDate': 'expiration_date',
        'Latitude': 'latitude',
        'Longitude': 'longitude',
        'LocationDescription': 'location_description',
        'FoodItems': 'food_items',
        'FacilityType': 'facility_type',
        'Status': 'status',
        'dayshours': 'opening_hours',
        'Zip Codes': 'zip_codes'
        }
    )

    # Drop any columns that are not in the FoodTruck class
    df = df[['cnn', 'blocklot', 'permit', 'X', 'Y', 'Schedule', 'NOISent', 'Approved', 'Received', 'PriorPermit', 'Location', 'Fire Prevention Districts', 'Police Districts', 'Supervisor Districts', 'Neighborhoods (old)']]

    logging.info('Data transformed successfully.')

    # Connect to your Azure PostgreSQL instance
    conn = psycopg2.connect(DATABASE_URI)

    logging.info('Database connection established successfully.')

    # Create a cursor object
    cur = conn.cursor()
    
    # Check if each truck already exists in the database before inserting it into the table
    for index, row in df.iterrows():
        cur.execute(
            "SELECT id FROM truck WHERE name = %s AND address = %s AND latitude = %s AND longitude = %s",
            (row['name'], row['address'], row['latitude'], row['longitude'])
        )
        result = cur.fetchone()
        if result is None:
            cur.execute(
                "INSERT INTO truck (id, name, address, block, latitude, longitude, location_description, locationid, food_items, opening_hours, zip_codes, lot, facility_type, status, expiration_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (index, row['name'], row['address'], row['block'], row['latitude'], row['longitude'], row['location_description'], row['locationid'], row['food_items'], row['opening_hours'], row['zip_codes'], row['lot'], row['facility_type'], row['status'], row['expiration_date'])
            )
    
    logging.info('Data updated successfully.')

    # Commit the changes and close the connection
    conn.commit()

    logging.info('Data committed to database successfully.')

    cur.close()
    conn.close()

    logging.info('Database connection closed successfully.')
