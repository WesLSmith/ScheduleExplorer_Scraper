##       By: Wesley Smith        ##
## Repo at:                       $$

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import pandas as pd
import time
import datetime





#datetime.datetime(year, monthy, day, hour, minute)

def web_address_builder(origin_coords, dest_coords, departure_time, unix = False):
    """Creates a web address based on input arguements
    Coordinates should be comma seperated string: e.g. "42.363021,-71.05829"
    Depature time must be a datetime() tuple"""

    start = "https://www.google.com/maps/dir"
    view_coords = "42.339673,-71.052303,14z"
    utime = time.mktime(departure_time.timetuple())
    utime = str(utime)[:10]
    data_path = "data=!4m5!4m4!2m2!7e2!8j{}!3e3".format(utime)

    return "{}/{}/{}/@{}/{}".format(start, origin_coords, dest_coords, view_coords, data_path)



def get_schedule_explorer_data(url, webdriver_path,lat_long = True):
    """Load a google maps directions TRANSIT page, extract schedule explorer  data"""

    wd_path = webdriver_path
    browser= webdriver.Chrome(executable_path = wd_path)
    browser.get(url)
    browser.implicitly_wait(3)
    ##Click on the schedule explorer button
    browser.find_element_by_xpath('//*[@id="pane"]/div/div[2]/div/div/div[6]').click()
    ##Wait for page to load
    time.sleep(10)
    ##Regex for times
    html_source = browser.page_source
    times = re.findall("""class="transit-time" jsan="7.transit-time">(.*?)</span>""", html_source)
    ##Each time-pair gets pulled twice for some reason, get every 4th for arrival and departure
    depart_times = times[::4]
    arrival_times = times[1::4]
    ##Regex for travel time
    travel_times = re.findall('class="duration" jsan="7.duration">(.*?)</span>', html_source)
    travel_times = travel_times[::2]
    ##Pandas Export
    depart_times = pd.Series(depart_times)
    arrival_times = pd.Series(arrival_times)
    travel_times = pd.Series(travel_times)
    temp_df = pd.DataFrame()
    temp_df["depart_time"] = depart_times
    temp_df["arrival_time"] = arrival_times
    temp_df["travel_time"] = travel_times
    ##Optionally return coordinates from weh address
    if lat_long == True:
        temp_df["orgin_coords"] = url.split('/')[5]
        temp_df["dest_coords"] = url.split('/')[6]
    ##retrun a pandas dataframe
    browser.close()
    return temp_df
