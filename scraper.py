import requests
from bs4 import BeautifulSoup

import re
from collections import defaultdict

from database import Database


class Scraper:
    def __init__(self, url: str):
        self.url = url
        self.data = []
        self.gp_id = int(url.split('/')[-3]) - 1105
        self.__get_data()

    def __get_data(self):
        response = requests.get(url=self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1')
        print(title.text.strip())

        table = soup.find(lambda tag: tag.name == 'table')
        rows = table.findAll(lambda tag: tag.name == 'tr')

        if "race-result" in self.url:
            self.get_race_results(rows)
        elif "qualifying" in self.url:
            self.get_qualifying_results(rows)

    def get_race_results(self, rows):
        for row in rows[1:]:
            raw_data = (list(row))
            driver = defaultdict(None)
            for i, line in enumerate(raw_data):
                if i == 3:
                    driver["Pos"] = self.__extract(line)
                elif i == 5:
                    driver["No"] = self.__extract(line)
                elif i == 7:
                    driver["Driver"] = self.__extract_driver(line)
                elif i == 9:
                    driver["Team"] = self.__extract_team(line)
                elif i == 11:
                    driver["Laps"] = self.__extract(line)
                elif i == 13:
                    driver["Time"] = self.__extract_time(line)
                elif i == 15:
                    driver["Pts"] = self.__extract(line)
            print(driver)
            self.data.append(driver)

    def get_qualifying_results(self, rows):
        for row in rows[1:]:
            raw_data = (list(row))
            driver = defaultdict(None)
            for i, line in enumerate(raw_data):
                if i == 3:
                    driver["Pos"] = self.__extract(line)
                elif i == 5:
                    driver["No"] = self.__extract(line)
                elif i == 7:
                    driver["Driver"] = self.__extract_driver(line)
                elif i == 9:
                    driver["Team"] = self.__extract_team(line)
                elif i == 11:
                    driver["Q1"] = self.__extract_time(line)
                elif i == 13:
                    driver["Q2"] = self.__extract_time(line)
                elif i == 15:
                    driver["Q3"] = self.__extract_time(line)
            print(driver)
            self.data.append(driver)

    @staticmethod
    def __extract(line):
        return re.findall('>.*<', str(line))[0][1:-1]

    @staticmethod
    def __extract_driver(line):
        return re.findall('mobile">.*<', str(line))[0][8:-1]

    def __extract_team(self, line):
        full_name = self.__extract(line).split(' ')
        if len(full_name) > 1:
            if full_name[0] == 'Alfa' or full_name[0] == 'Aston' or full_name[0] == 'Red':
                return full_name[0] + ' ' + full_name[1]
        return full_name[0]

    @staticmethod
    def __extract_time(line):
        if "seconds" in str(line):
            return re.findall('>.*<s', str(line))[0][1:-2]
        elif " lap" in str(line):
            laps = re.findall('>.*<s', str(line))[0][1:-2]
            suffix = " lap" if laps == '+1' else " laps"
            return laps + suffix
        else:
            return re.findall('>.*<', str(line))[0][1:-1]

    def update_database(self, path):
        user_input = input(f"Do you want to update database({path}) [Yes/No]: ")
        if user_input == "Yes":
            db = Database(path)
            if "race-result" in self.url:
                db.insert_race_results(self.data, self.gp_id)
            elif "qualifying" in self.url:
                db.insert_qualifying(self.data, self.gp_id)
            print("Database updated!")


if __name__ == '__main__':
    # scr = Scrapper("https://www.formula1.com/en/results.html/2022/races/1108/australia/qualifying.html")
    scr = Scraper("https://www.formula1.com/en/results.html/2022/races/1108/australia/race-result.html")
    scr.update_database("db/f1.db")
