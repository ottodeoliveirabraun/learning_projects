import datetime
from scraping_flights.airlines.latam.latam_web import navigate_latam
from scraping_flights.config import START_DATE, END_DATE, ORIGIN, DESTINATION, TRIP_DURATION_DAYS



#this will be the main looping function
def iterating_over_days(start_date, end_date, duration, origin, destination ):
    scrape_date = start_date
    while scrape_date <= end_date:

        navigate_latam(scrape_date, duration, origin, destination)
        scrape_date = scrape_date + datetime.timedelta(days=1)


iterating_over_days(START_DATE, END_DATE, TRIP_DURATION_DAYS, ORIGIN, DESTINATION,)



#creates df for flights
#df = df_creator(list_of_flights)

#print(df)

#Print results do Gsheet
#write(df.values.tolist())

# print('flight ', flight_element)
# print(flight_element.text)
# print(flight_element.text.splitlines())
# latam.loop_throught(flight.text.splitlines())

