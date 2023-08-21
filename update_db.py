import pandas as pd
import schedule

from api import db
from models import FoodTruck

def update_database():
    # Read CSV file
    df = pd.read_csv('Mobile_Food_Facility_Permit.csv')

    # Iterate over each row and update the database
    for index, row in df.iterrows():
        truck = FoodTruck.query.filter_by(name=row['name']).first()
        if truck:
            truck.name = row['Applicant']
            truck.address = row['address']
            truck.latitude = row['Latitude']
            truck.longitude = row['Longitude']
        else:
            truck = FoodTruck(id=index, name=row['Applicant'], address=row['Address'], block=row['block'], lot=row['lot'], status=row['Status'], food_items=row['FoodItems'], facility_type=row['FacilityType'], location_description=row['LocationDescription'], locationid=row['locationid'], opening_hours=row['dayshours'], zip_codes=row['Zip Codes'], expiration_date=row['ExpirationDate'], latitude=row['Latitude'], longitude=row['Longitude'])
            db.session.add(truck)
            print(truck)
    db.session.commit()

# Schedule the task to run every day at midnight
# schedule.every().day.at('00:00').do(update_database)

# Run the task once
update_database()