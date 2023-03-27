# Local Zone Project

This project was created to test the latency difference between regular availability zone and Helsinki local zone in Stockholm region of AWS.


### Description

This project is a flask app that pings two different instances of your choosing and creates SQLite database, where it saves the responses and calclulates the average.
Each time you press the ping button, the app will ping two different instances four times and return the average latency.
The average at the top is calclulated from all the four ping averages that SQLite database has stored at the time.

### Dependencies / Requirements

Flask, SQLite, and pythonping are required to use this app. You can use **pip install -r requirements.txt** in app directory.

### Installing and using the app

To use this app you simply need to start two EC2 instances in different availability zones and add their public IP addresses to app.py file, after the @app.route('/') (line 70 onwards, higlighted by comments).
The names of the availability zones should also be changed to represent the availability zones that are being tested.
After these changes you can run app.py from the app folder and open the localhost:5000 to use the app UI.
If you decide to swap the instances / names of the availability zones, you should always clear the SQLite database by clicking "Clear Responses" button in the browser UI.

