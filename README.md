# Introducing Amazon Price Tracker
**Amazon Price Tracker** is a simple Python application that tracks the price of your specified products on Amazon once a day and notifies you via email in case the price is below the threshold set by you.

# Features
The products to track and their price limits are specified by you in the 'products_to_track.csv' file, which expect a simple content:
    
<img src="Screenshots/products_to_track.png" alt="Products to Track" width="350"><br>

If the price of the product is below the limit you set in the CSV file, the recipients get an email notification:

<img src="Screenshots/notification_email.png" alt="Products to Track" width="550"><br>

The application also writes the prices into the 'tracker.log' file where you can see the daily price developments:

<img src="Screenshots/tracker_log.png" alt="Products to Track" width="350"><br>


# Installation and Setup
- Download the entire project code to your computer and unzip files locally.
- Install the following packages that are not part of the standard Python installation if you don't have them yet:
    - pip install beautifulsoup4
    - pip install lxml
    - pip install requests
    - pip install python-dotenv
    - pip install pandas
- This project uses Gmail account for sending the email notification. You need to get the gmail <a href="https://myaccount.google.com/apppasswords" target="_blank">App Password</a> for your Google Account.
- open the .env file and populate the first three entries (email_address, email_password and recipients)
- Fill in 'products_to_track.csv' with your price_limit, friendly name and URL
- Schedule the 'price_tracker.py' to run on daily basis (e.g. using Windows Task Scheduler on your server or in the cloud using, e.g.  <a href="https://www.pythonanywhere.com/" target="_blank">PythonAnywhere</a>)
