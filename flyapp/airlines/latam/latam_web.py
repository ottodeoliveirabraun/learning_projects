import datetime
import time

from scraping_flights.utils.util_pandas import df_creator
from scraping_flights.utils.util_gsheet import write
from scraping_flights.utils.util_selenium import start_browser
from scraping_flights.utils.util_sqlite import insert_flight
from selenium.common.exceptions import NoSuchElementException
from scraping_flights.airlines.latam import latam_data
from selenium.webdriver.common.by import By


def build_link_for_latam(start_date, end_date, origin: str, destination: str) -> str:
    link = "https://www.latamairlines.com/de/de/flugangebote?origin=" + origin + "&inbound=" + str(end_date) + "T12%3A00%3A00.000Z&outbound=" + str(start_date) + "T12%3A00%3A00.000Z&destination=" + destination + "&adt=1&chd=0&inf=0&trip=RT&cabin=Economy&redemption=false&sort=RECOMMENDED"
    #print(link)
    return link


def pull_list_of_flights(driver, START_DATE):
    flight_found = True
    flight_id = 0
    flight_list = []
    while flight_found is True:
        wrapper_text = 'WrapperCardFlight' + str(flight_id)
        # print(wrapper_text)
        try:
            flight_element = driver.find_element(By.ID, wrapper_text)
            get_data = latam_data.loop_throught(flight_element.text.splitlines())
            save_data = latam_data.fill_flight_object_for_latam(get_data, START_DATE)
            flight_list.append(save_data)
            flight_id = flight_id + 1
        except NoSuchElementException:
            flight_found = False

    return flight_list




def navigate_latam(START_DATE: datetime.date, TRIP_DURATION_DAYS: int, ORIGIN: str, DESTINATION: str):

    LATAM_PAGE = build_link_for_latam(START_DATE, START_DATE + datetime.timedelta(days=TRIP_DURATION_DAYS), ORIGIN,DESTINATION)

    #Start selenium without opening the browser
    driver = start_browser(LATAM_PAGE,  headless=True)

    #print(driver.title)
    #wait to load page
    driver.implicitly_wait(10)

    #deal with cookies
    button = driver.find_element(By.ID, 'cookies-politics-button')
    button.click()

    #pull first way flights
    list_of_flights = pull_list_of_flights(driver, START_DATE)

    print(list_of_flights)

    for flight_wow in list_of_flights:
        print(flight_wow)
        print(flight_wow.price)

    #debugging command
    #driver.save_screenshot('screenie.png')

    #select first flight
    #button = driver.find_element(By.CSS_SELECTOR, '[data-testid="card-expander-0"]')
    button = driver.find_element(By.XPATH, '//div[@data-testid="card-expander-0"]')
    button.click()

    time.sleep(5)

    #confirm first flight
    button = driver.find_element(By.CSS_SELECTOR, '[data-testid="bundle-detail-0-flight-select"]')
    button.click()

    time.sleep(5)

    list_of_flights = pull_list_of_flights(driver, START_DATE + datetime.timedelta(days=TRIP_DURATION_DAYS))

    # creates df for flights to send data to gsheet
    #df = df_creator(list_of_flights)

    # Write results to Gsheet
    #write(df.values.tolist(), "wow!A1")

    print(list_of_flights)

    for each_flight in list_of_flights:
        print(each_flight)
        insert_flight(each_flight)


    print("!!!!!!!!!!!!!!!!QUITING DRIVER!!!!!!!!!!!!!!!!!!!")
    driver.quit()