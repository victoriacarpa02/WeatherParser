# Weather Scraper
This project is a web scraper that retrieves weather information from weather.com for a specified city using Selenium. It allows users to get the current weather, today's weather, UV index, sunrise and sunset times, and a 14-day weather forecast.

## Requirements
- Python 3
- Selenium
- Firefox WebDriver

## Installation
1. Install Selenium
```
pip install selenium
```
3. Download the Firefox WebDriver and add it to your system PATH.

## Usage
1. Clone this repository:
```
git clone https://github.com/victoriacarpa02/weather_parser.git
cd weather_parser
```
2. Create a Weather object and use its methods to get weather information:
```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re

# Your code goes here

with webdriver.Firefox() as browser:
    browser.get('https://weather.com')
    # time for page loading
    time.sleep(2)

    # creating an object with the weather of a specific city
    obj = Weather('Kyiv')

    # print weather now
    print(obj.weather_now('F'))

    # print weather for today
    print(obj.weather_today('C'))

    # check uv index
    print(obj.uv_check)

    # sunrise
    print(obj.sunrise)

    # sunset
    print(obj.sunset)

    # weather for 14 days
    obj.weather_for_14_days('C')
```

## Class and Methods
### Weather Class

**__init__(self, city)**
Initializes the Weather object with the specified city and performs a search.

**search_city(self)**
Searches for the specified city on weather.com.

**degrees(degree)**
Changes the temperature unit display to Celsius ('C') or Fahrenheit ('F').

**weather_now(self, degree)**
Returns the current temperature and weather condition.

**uv_check**
Returns the current UV index and a recommendation based on the UV level.

**weather_today(self, degree)**
Returns detailed weather information for today.

**sunrise**
Returns the sunrise time.

**sunset**
Returns the sunset time.

**weather_for_14_days(self, degree)**
Prints the weather forecast for the next 14 days.

## Notes
- Ensure you have a stable internet connection as the script interacts with live web pages.
- The script uses time.sleep() to wait for page elements to load. You may need to adjust the sleep durations based on your internet speed.
- The project can be further developed to include features such as language selection, hourly weather display, and more.
