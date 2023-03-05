This project contains a Django application for managing ads. The application uses Invoke Tasks to run the necessery python scripts as tasks, and includes the following tasks: 

import, insert, pause_ad, unpause_ad, and update_ad. These tasks can be triggered by calling the tasks using invoke command line tool. 


Installation
Clone the repository:

git clone https://github.com/your-username/adtask.git

Install the dependencies:

cd adtask
pip install -r files/setup/requirements.txt

Migrate the database:

python manage.py migrate

Create a superuser:

python manage.py createsuperuser

Run the server:

python manage.py runserver

Export the Google Big Query Credentials:

export GOOGLE_APPLICATION_CREDENTIALS="files/setup/wildnet-379515-14a67b02623c.json"

Run the tasks:

Import the TableA Data to the Database:

invoke property.import --filename=files/csv_data/TableA.csv

Inert GoogleAds data to bigquery:

invoke ad.insert

Calculate the ad matrix:

invoke ad.calculate

Pause the ads:

invoke ad.pause

Unpause the ads:

invoke ad.unpause

Update the ads:

invoke ad.update

Run the tests:

python manage.py test



