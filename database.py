import sqlite3


class Database:
    def __init__(self, db_path):
        self.__connection = sqlite3.connect(db_path)
        self.__cursor = self.__connection.cursor()
        self.__driver_id = {44: 1, 63: 2, 1: 3, 11: 4, 16: 5, 55: 6, 4: 7, 3: 8, 31: 9, 14: 10,
                            10: 11, 22: 12, 18: 13, 5: 14, 23: 15, 6: 16, 77: 17, 24: 18, 20: 19, 47: 20,
                            27: 21}
        self.__team_id = {"Mercedes": 1, "Red Bull": 2, "Ferrari": 3, "McLaren": 4, "Alpine": 5,
                          "AlphaTauri": 6, "Aston Martin": 7, "Williams": 8, "Alfa Romeo": 9, "Haas": 10}
        self.gp_id = {1124: 1, 1125: 2, 1108: 3, 1109: 4}

    def insert_race(self, data, gp_id):
        query = "INSERT INTO race (grand_prix_id,driver_id,team_id,position,laps,time,points) VALUES (?,?,?,?,?,?,?)"
        for d in data:
            driver_id = self.__driver_id[int(d["No"])]
            team_id = self.__team_id[d["Team"]]
            self.__cursor.execute(query, (gp_id, driver_id, team_id, d["Pos"], d["Laps"], d["Time"], d["Pts"]))
        self.__connection.commit()

    def insert_qualifying(self, data, gp_id):
        query = "INSERT INTO qualifying (grand_prix_id,driver_id,team_id,position,q1,q2,q3) VALUES (?,?,?,?,?,?,?)"
        for d in data:
            driver_id = self.__driver_id[int(d["No"])]
            team_id = self.__team_id[d["Team"]]
            d["Q2"] = None if d["Q2"] == '' else d["Q2"]
            d["Q3"] = None if d["Q3"] == '' else d["Q3"]
            self.__cursor.execute(query, (gp_id, driver_id, team_id, d["Pos"], d["Q1"], d["Q2"], d["Q3"]))
        self.__connection.commit()

    def insert_practice(self, data, gp_id, session_no):
        query = "INSERT INTO practice " \
                "(grand_prix_id,session_no,driver_id,team_id,position,time,laps) VALUES (?, ?,?,?,?,?,?)"
        for d in data:
            driver_id = self.__driver_id[int(d["No"])]
            team_id = self.__team_id[d["Team"]]
            d["Time"] = None if d["Time"] == '' else d["Time"]
            self.__cursor.execute(query, (gp_id, session_no, driver_id, team_id, d["Pos"], d["Time"], d["Laps"]))
        self.__connection.commit()

    def insert_sprint(self, data, gp_id):
        query = "INSERT INTO sprint (grand_prix_id,driver_id,team_id,position,laps,time,points) VALUES (?,?,?,?,?,?,?)"
        for d in data:
            driver_id = self.__driver_id[int(d["No"])]
            team_id = self.__team_id[d["Team"]]
            self.__cursor.execute(query, (gp_id, driver_id, team_id, d["Pos"], d["Laps"], d["Time"], d["Pts"]))
        self.__connection.commit()


if __name__ == '__main__':
    db = Database("db/f2.db")