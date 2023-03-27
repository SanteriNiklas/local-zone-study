import flask
from pythonping import ping
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["DATABASE"] = "ping_data.db"


# Initialize the database with a table to store the response times
def init_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS ping_response_times
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  region TEXT,
                  response_time FLOAT)""")
    conn.commit()
    conn.close()


init_db()


# Insert a new response time into the database
def insert_response_time(region, response_time):
    conn = sqlite3.connect(app.config["DATABASE"])
    c = conn.cursor()
    c.execute("INSERT INTO ping_response_times (region, response_time) VALUES (?, ?)", (region, response_time))
    conn.commit()
    conn.close()


# Retrieve the previous response times from the database
def get_response_times():
    conn = sqlite3.connect(app.config["DATABASE"])
    c = conn.cursor()
    c.execute("SELECT region, response_time, timestamp FROM ping_response_times ORDER BY timestamp DESC")
    rows = c.fetchall()
    response_times = []
    for row in rows:
        response_times.append({'region': row[0], 'response_time': row[1], 'timestamp': row[2]})
    conn.close()
    return response_times


#Average response time
def get_avg_response_times():
    conn = sqlite3.connect(app.config["DATABASE"])
    c = conn.cursor()
    c.execute("SELECT region, AVG(response_time) FROM ping_response_times GROUP BY region")
    rows = c.fetchall()
    response_times = []
    for row in rows:
        response_times.append({'region': row[0], 'avg_response_time': row[1]})
    conn.close()
    return response_times


# Clear the ping_response_times table
def clear_response_times():
    conn = sqlite3.connect(app.config["DATABASE"])
    c = conn.cursor()
    c.execute("DELETE FROM ping_response_times")
    conn.commit()
    conn.close()


@app.route('/', methods=['GET'])
def home():

    #########################################################################################################################################
    # IP addresses are from the instances that are being tested, change these to public IP addresses of the instances that you want to test #
    #########################################################################################################################################
    responseAZ1 = ping('13.49.76.8', verbose=True)
    responseAZ2 = ping('15.220.169.134', verbose=True)

    ################################################################
    # Change these names to the availability zones you are testing #
    ################################################################
    AZ1Name = "Availability Zone 1a"
    AZ2Name = "Helsinki Local Zone"
    
    # Save the response times in the database                                               
    insert_response_time(f"{AZ1Name}", responseAZ1.rtt_avg_ms)
    insert_response_time(f"{AZ2Name}", responseAZ2.rtt_avg_ms)
    
    # Get the previous response times from the database
    response_times = get_response_times()
    avg_response_times = get_avg_response_times()
    for item in avg_response_times:
        item["avg_response_time"] = round(item["avg_response_time"], 3)
    return flask.render_template("index.html", response_times=response_times, avg_response_times=avg_response_times, AZ1Name=AZ1Name, AZ2Name=AZ2Name)


@app.route('/delete', methods=['GET'])
def delete():
    clear_response_times()
    return flask.render_template("index.html", response_times=[])


if __name__ == "__main__":
    init_db()
    app.run()
