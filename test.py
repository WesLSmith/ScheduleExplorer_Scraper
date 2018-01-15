import sys
sys.path.append(r"C:\Users\Wesley Smith\Desktop\gm_Scraper")
from gm_scraper import web_address_builder, get_schedule_explorer_data
import datetime
import pandas as pd
import time

## Testing some sample coordinates

##Input coords can be any sort of Iterable
origins = ["42.3563946,-71.0624242", "41.8138752,-71.4245513", "40.6906544,-73.9428026", "40.7216974,-74.0053699", "37.852803,-122.270062"]
dests = ["42.3422297,-71.0900691", "42.3563946,-71.0624242", "40.6010438,-73.973015", "40.791641,-73.964699", "37.7381014,-122.4689529"]
u_time = datetime.datetime(2018, 1, 20 , 16, 10,0)
webdriver_path = r"C:\Users\Wesley Smith\Desktop\gm_Scraper\chromedriver.exe"

##Iterate
df = pd.DataFrame()
urls = []
for i, j in zip(origins, dests):
    url = (web_address_builder(i,j, u_time))
    df_test = get_schedule_explorer_data(url, webdriver_path)
    df = pd.concat([df,df_test])
    urls.append(url)
print(df)
print(urls)
