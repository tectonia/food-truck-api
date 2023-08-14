import os

from flask import Flask, json, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import pandas as pd
import math

api = Flask(__name__)
csrf = CSRFProtect(api)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    api.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    api.config.from_object('azureproject.production')

api.config.update(
    SQLALCHEMY_DATABASE_URI=api.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(api)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(api, db)

@api.route('/', methods = ['GET'])
def home():
    data = "hello world"
    return jsonify({'data': data})

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c * 1000

    return distance

@api.route('/trucks', methods=['GET'])
def get_trucks():
    # Get longitude and latitude from query string
    lon = request.args.get('lon', type=float)
    lat = request.args.get('lat', type=float)
    number = request.args.get('number', type=int, default=5)

    # Read csv file
    df = pd.read_csv(r'Mobile_Food_Facility_Permit.csv')

    # Drop rows where longitude or latitude is 0 and where status is not approved
    df = df[(df.Longitude != 0) & (df.Latitude != 0) & (df.Status == 'APPROVED')]

    # Drop rows where expiration date is before today
    df['ExpirationDate_fmt'] = df.apply(lambda row: pd.to_datetime(row['ExpirationDate'], format='%m/%d/%Y %I:%M:%S %p', errors='ignore'), axis=1)
    df = df[df['ExpirationDate_fmt'] > pd.Timestamp('today').normalize()]

    # Calculate distance between each truck and the given longitude and latitude
    df['Distance (meters)'] = df.apply(lambda row: haversine_distance(row['Latitude'], row['Longitude'], lat, lon), axis=1)
    
    # Sort by distance and return top n trucks
    df = df.sort_values(by=['Distance (meters)']).head(number)

    # Drop unnecessary columns and rename columns
    df = df.drop(columns=['Approved', 'ExpirationDate', 'ExpirationDate_fmt', 
                          'Fire Prevention Districts', 'Schedule', 'blocklot', 
                          'NOISent', 'Neighborhoods (old)', 'cnn', 'X', 'Y', 
                          'Police Districts', 'Received', 'permit', 'Status', 
                          'PriorPermit', 'Supervisor Districts'])
    df = df.rename(columns={'Applicant': 'Name', 'FacilityType': 'Facility Type', 
                            'LocationDescription': 'Location Description', 
                            'dayshours': 'Opening Hours', 'block': 'Block', 
                            'lot': 'Lot', 'FoodItems': 'Food Items', 
                            'locationid': 'Location ID'})

    # Convert to json
    df = df.to_json(orient='records')
    trucks = json.loads(df)

    return trucks

@api.route('/trucks/<int:locationid>', methods=['GET'])
def get_truck(locationid):
    # Read csv file
    df = pd.read_csv(r'Mobile_Food_Facility_Permit.csv')

    # Find truck with given locationid
    df = df[df['locationid'] == locationid]

    # Drop unnecessary columns and rename columns
    df = df.drop(columns=['Approved', 'ExpirationDate', 'Fire Prevention Districts', 
                          'Schedule', 'blocklot', 'NOISent', 'Neighborhoods (old)', 
                          'cnn', 'X', 'Y', 'Police Districts', 'Received', 
                          'permit', 'Status', 'PriorPermit', 'Supervisor Districts'])
    df = df.rename(columns={'Applicant': 'Name', 'FacilityType': 'Facility Type', 
                            'LocationDescription': 'Location Description', 
                            'dayshours': 'Opening Hours', 'block': 'Block', 
                            'lot': 'Lot', 'FoodItems': 'Food Items', 
                            'locationid': 'Location ID'})

    # Convert to json
    df = df.to_json(orient='records')
    truck = json.loads(df)

    return truck

if __name__ == '__main__':
    api.run()
