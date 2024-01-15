import re
import winsound
import argparse
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

CFX_LV = r'https://servers.redm.gg/servers/detail/qybeq6'


class CheckPlayerAvailable:

    def __init__(self, player_name, timeout, period):
        self.player_name = player_name
        self.timeout = timeout
        self.period = period
        self.run()

    def run(self):
        start = time.time()
        while True:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

            wait = WebDriverWait(driver, 10)

            driver.get(CFX_LV)
            get_url = driver.current_url
            wait.until(EC.url_to_be(CFX_LV))

            if get_url == CFX_LV:
                page_source = driver.page_source
            else:
                raise RuntimeError
            driver.close()

            soup = BeautifulSoup(page_source, features='html.parser')

            matches = soup.body.find_all(string=re.compile(self.player_name))

            if len(matches) > 0:
                frequency = 2000
                duration = 300
                winsound.Beep(frequency, duration)
                break

            current = time.time()
            if current - start > self.period:
                print('Player did not show up for {} minutes'.format(self.period/60))
                break

            time.sleep(self.timeout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('player_name', type=str)
    parser.add_argument('-t', '--timeout', type=int, default=300)
    parser.add_argument('-p', '--period', type=int, default=600)

    args = parser.parse_args()
    name, delay, run_time = args.player_name, args.timeout, args.period
    check_player = CheckPlayerAvailable(name, delay, run_time)
