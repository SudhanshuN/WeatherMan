## WeatherMan.py
## @author SudhanshuAN
##
## Program description:
##          The progarm takes in a file listing names of cities in each new line and outputs
##          the average temperature and humidity over past specified number of days (on Shell)
##          Also variations temperature and humidity is plotted (each city in new window)
##          Maximize the Plot window for clear viewing
##
## Customisables:
##          back_days= number of days to go back = total days - 1 (default: 6)
##          d        = last day of observation (default: yesterday)
##          file_name= name of input file (must be in same folder as the code)
##
##
##
## Some places don't give results
## Doesn't work for about an hour after midnight if d is set to today
## Doesn't work if the city is forward and date hasn't changed there yet
##          For example, for a city in Aus it is yesterday's date at 1am IST
##
## After taking all this into account, I decided to take average till the day before



import requests                                     ##For download of page
from bs4 import BeautifulSoup as BS                 ##Scraping through the page
from datetime import date, timedelta                ##managing time and date also knowing today's date
import numpy as np                                  ##Data import and maths
import matplotlib.pyplot as plt                     ##Plotting
import matplotlib.dates as dt                       ##Plotting

##Number of days to take data for -1
back_days=6

##end date              May be taken as anything in Python date format
d = date.today() - timedelta(days=1)

##file in which the places are given
## !!!Not all places are supported!!! :(
## Will recieve a AttributeError: NoneType    or error from plot library if no data is available
file_name = "input.txt"


file = open(file_name,'r')                          ##open given file in read mode
places = file.readlines()                           ##read lines from the file
places = [x.strip() for x in places]                ##cleanup of '\n',etc

dates = [d-timedelta(days=back_days-r) for r in range(back_days+1)]         ##compile list of dates
datenums = dt.date2num(dates)                                               ##convert to number of days since 01-01-0001 to use in plotting

##Head line for table in Shell
op = "{pla:15s}{temp:>15s}{hum:>15s}".format(pla="City",temp="Temperature",hum="Humidity")
print (op)

for place in places:                                    ##iterate through places
    ##print (place)     ##debug
    ## Compose URL request
    url = "https://www.wunderground.com/history/place/"+place+"/"+str(dates[0].year)+"/"+str(dates[0].month)+"/"+str(dates[0].day)+"/CustomHistory.html?dayend="+str(dates[back_days].day)+"&monthend="+str(dates[back_days].month)+"&yearend="+str(dates[back_days].year)
    page = requests.get(url)                            ##download the page
    ##print(url)        ##debug
    soup = BS(page.content, 'html.parser')              ##Convert to BeautifulSoup
    days = soup.find(id="obsTable").find_all("tbody")   ##Find table with id="obsTable" and Find all "tbody" tags
    ##Retruve each row
    dayObs = [ BS(str(days[t]),'html.parser').find_all(class_="wx-value") for t in range(len(days))]

    temps=[]                                            ##Stores temperatues
    hums=[]                                             ##Stores humidity
    for t in range(len(days)):                          ##iterate through days
        if(len(dayObs[t])>0):                           ##Select only the rows containing weather data
            temps.append(int(dayObs[t][1].get_text()))  ##Retrive temperature
            hums.append(int(dayObs[t][7].get_text()))   ##Retrive humidity

    ##print(temps)      ##debug
    ##print(hums)       ##debug

    ##Format the string and print it
    op = "{pla:15s}{temp:15.3f}{hum:15.3f}".format(pla=place.capitalize(),temp=np.mean(temps),hum=np.mean(hums))
    print (op)
    
    plt.figure(place.capitalize())                                                      ##Set window name
    plt.subplot(211)                                                                    ##Upper plot
    plt.plot_date(datenums,temps,'go-', linewidth=2, markersize=7)                      ##Plot it
    plt.title("Temperature(\u2103)  Average = " + str(np.mean(temps)) + "\u2103")       ##Title ("\u2103" is unicode for degree celcius symbol)
    plt.subplot(212)                                                                    ##Second plot
    plt.plot_date(datenums,hums,'bo-', linewidth=2, markersize=7)                       ##Plot it
    plt.title("Humidity(%)   Average = " + str(np.mean(hums)) + "%")                    ##Title

plt.show()      ##Show all the plots
