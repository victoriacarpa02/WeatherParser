from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re


class Weather:
    def __init__(self, city):
        try:
            self.city = city
            self.search_city()
        except Exception:
            print(f'Exception was raised during the search. Please, enter the name of the city correctly!')

    def search_city(self):
        field = browser.find_element(By.ID, 'LocationSearch_input')
        field.send_keys(self.city)

        # wait for the city options to come up and choose the first one
        option = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'LocationSearch_listbox')))
        option.find_element(By.TAG_NAME, 'button').click()

    @staticmethod
    def degrees(degree):
        # changing the display of degrees (Celsius or Fahrenheit)
        browser.find_element(By.CLASS_NAME, 'LanguageSelector--menuButtonInner--3z59Z').click()
        if degree == 'C':
            browser.find_element(By.ID, 'UnitSelectorTabs-tab_1').click()
        elif degree == 'F':
            browser.find_element(By.ID, 'UnitSelectorTabs-tab_0').click()
        else:
            raise Exception('Incorrect input')

    def weather_now(self, degree):
        # wait for page loading
        time.sleep(3)

        # changing the display of degrees (Celsius or Fahrenheit)
        self.degrees(degree)

        # result output (temperature and current condition)
        temperature = browser.find_element(By.CLASS_NAME, 'CurrentConditions--tempValue--MHmYY')
        condition = browser.find_element(By.CLASS_NAME, 'CurrentConditions--phraseValue--mZC_p')

        # pulling up the timestamp
        regular_exp = r'\d+:\d+\s[ap]m'
        timestamp = re.findall(regular_exp, browser.find_element(By.CLASS_NAME, 'CurrentConditions--timestamp--1ybTk').text)[0]

        return 'Weather for now: \n' + f'Temperature at {timestamp} in {self.city}: {temperature.text}\nCurrent ' \
                                   f'condition: {condition.text}\n'

    @property
    def uv_check(self):
        uv_index = browser.find_element(By.XPATH, '//div[@class="WeatherDetailsListItem--wxData--kK35q"]/span['
                                                  '@data-testid="UVIndexValue"]').text
        # uv_index recommendations
        recommended = ''
        if int(uv_index[0]) in range(0, 3):
            recommended = 'You can safely enjoy being outside!'
        if int(uv_index[0]) in range(3, 8):
            recommended = 'Seek shade during midday hours! Slip on a shirt, slop on sunscreen and slap on hat!'
        if int(uv_index[0]) > 7:
            recommended = 'Avoid being outside during midday hours! Make sure you seek shade! Shirt, sunscreen and ' \
                          'hat are a must!'
        return f'UV index is {uv_index}. Here is your recommendation for today: \n{recommended}\n'

    def weather_today(self, degree):
        # wait for page loading
        time.sleep(3)

        # changing the display of degrees (Celsius or Fahrenheit)
        self.degrees(degree)

        # gather info
        elements_titles = browser.find_elements(By.CLASS_NAME, 'WeatherDetailsListItem--label--2ZacS')
        elements_info = browser.find_elements(By.CLASS_NAME, 'WeatherDetailsListItem--wxData--kK35q')
        result = [f'Feels like: {browser.find_element(By.CLASS_NAME, "TodayDetailsCard--feelsLikeTempValue--2icPt").text}']
        for i in range(len(elements_titles)):
            result.append(f'{elements_titles[i].text}: {elements_info[i].text}')

        # result output
        return 'Weather for today: \n' + f'\n'.join(inf for inf in result) + '\n'

    @property
    def sunrise(self):
        return 'Sunrise at ' + browser.find_element(By.XPATH, '//div[@data-testid="SunriseValue"]/p').text

    @property
    def sunset(self):
        return 'Sunset at ' + browser.find_element(By.XPATH, '//div[@data-testid="SunsetValue"]/p').text

    def weather_for_14_days(self, degree):
        # wait for page loading
        time.sleep(3)

        # go to another page with hourly weather display
        browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[3]/div/nav/div/div[1]/a[3]').click()

        # wait for page loading
        time.sleep(3)

        # changing the display of degrees (Celsius or Fahrenheit)
        self.degrees(degree)

        box = browser.find_elements(By.XPATH, '//div[@class="DailyForecast--DisclosureList--nosQS"]/details')
        for d in box:
            if d.get_attribute('id') == 'detailIndex0':
                continue
            print(f'Date: {d.find_element(By.CLASS_NAME, "DetailsSummary--daypartName--kbngc").text}')
            print(f'Max temperature: {d.find_element(By.CLASS_NAME, "DetailsSummary--highTempValue--3PjlX").text}')
            print(f'Min temperature: {d.find_element(By.CLASS_NAME, "DetailsSummary--lowTempValue--2tesQ").text}')
            print(f'Condition: {d.find_element(By.CLASS_NAME, "DetailsSummary--extendedData--307Ax").text}')
            rain = d.find_element(By.CLASS_NAME, 'DetailsSummary--precip--1a98O').find_element(By.TAG_NAME, 'span').text
            print(f'Rain: {rain}')
            print('-' * 5)


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
