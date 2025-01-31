from scraping_flights.flight import flight
import datetime


def fill_flight_object_for_latam(
    flight_data: dict,
    departure_date,
) -> flight.Flight:
    return flight.Flight(
        airline="Latam",
        airport_from=flight_data["airport_from"],
        airport_to=flight_data["airport_to"],
        price=flight_data["price"],
        date_departure=str(departure_date),
        time_departure=flight_data["departure_time"],
        date_arrival=str(departure_date + datetime.timedelta(days=int(flight_data["next_day_arrival"].replace("+","")))),
        time_arrival=flight_data["arrival_time"],
        stopover=flight_data["stopovers"],
        duration=flight_data["duration"],
        scraped_timestamp=str(datetime.datetime.now())
    )

def loop_throught (scraped_list):
    flight_data = {}
    for e in scraped_list:
        flight_data.update(find_departure_and_arrival(e,flight_data)) if find_departure_and_arrival(e,flight_data) is not None else None
        flight_data.update(find_airport_code(e, flight_data)) if find_airport_code(e, flight_data) is not None else None
        flight_data.update(find_duration(e)) if find_duration(e) is not None else None
        flight_data.update(is_next_day_arrival(e)) if is_next_day_arrival(e) is not None else None
        flight_data.update(find_price(e)) if find_price(e) is not None else None
        flight_data.update(find_stopeovers(e)) if find_stopeovers(e) is not None else None
    if 'next_day_arrival' not in flight_data.keys():
        flight_data.update({'next_day_arrival':'+0'})
    return flight_data

def find_departure_and_arrival (list_element, flight_dictionary):
    if list_element.find(':',1,3) != -1:
        if 'departure_time' in flight_dictionary:
            return {'arrival_time': list_element}
        else:
            return {'departure_time':list_element}

def find_airport_code (list_element, flight_dictionary):
    if len(list_element) == 3:
        if 'airport_from' in flight_dictionary:
            return {'airport_to': list_element}
        else:
            return {'airport_from':list_element}

def find_duration (list_element):
    if list_element.find('Std.') != -1:
        return {'duration':list_element}

def find_price (list_element):
    if list_element.find('EUR') != -1:
        return {'price':list_element}

def is_next_day_arrival (list_element):
    if '+' in list_element and '|' not in list_element:
        return {'next_day_arrival':list_element}

def find_stopeovers (list_element):
    if 'Zwischenlandung' in list_element:
        return {'stopovers':list_element.split(' ')[0]}


