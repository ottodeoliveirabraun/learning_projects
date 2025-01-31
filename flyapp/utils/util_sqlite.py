import sqlite3

def insert_flight(flight):
    # Connect to the SQLite database
    conn = sqlite3.connect('flights.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Insert flight data into the flights table
    cursor.execute('''
        INSERT INTO raw_crawler (
            airline, 
            airport_from, 
            airport_to, 
            price, 
            date_departure, 
            time_departure, 
            date_arrival, 
            time_arrival, 
            stopover, 
            duration, 
            scraped_timestamp
        ) 
        VALUES (
            flight.airline, 
            flight.airport_from, 
            flight.airport_to, 
            flight.price, 
            flight.date_departure, 
            flight.time_departure, 
            flight.date_arrival, 
            flight.time_arrival, 
            flight.stopover, 
            flight.duration, 
            flight.scraped_timestamp
        )
    ''', flight)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

