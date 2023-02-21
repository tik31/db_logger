import json
import sqlite3
import datetime

class db_logger:

    def __init__(self):
        return

    def __del__(self):
        """
        При удалении объекта соединение с БД должно быть закрыто
        """

        self.close_database()


    def open_database(self, db_path):
        try:
            self.sqlite_connection = sqlite3.connect(db_path)
            self.cursor = self.sqlite_connection.cursor()
        except sqlite3.Error as error:
            print("Error during connection to database!", error)

    def close_database(self):
        if (hasattr(self, "sqlite_connection")):
            try:
                self.sqlite_connection.commit()
                self.sqlite_connection.close()
            except sqlite3.Error as error:
                print("Error during closing database!", error)
            finally:
                del(self.sqlite_connection)
                if (hasattr(self, "cursor")):
                    del(self.cursor)


    def log(self, Parameter, Level, Source, Time, Value):
        '''
        Функция для выполнения сохранения параметра в базу данных
        Parameter - строка с именем сохраняемого параметра
        Level - строка с именем уровня сообзения
        Source - строка с именем источника сообщения
        Time - Время сообщения
        Value - Значение параметра
        '''

        # TODO: Добавить проверку входных параметров

        # Сохрание информации о сообщении
        try:
            self.cursor.execute(
                    """
                    INSERT INTO events (event_time, id_parameter, id_level, id_producer) VALUES (?,
                        (SELECT id FROM parameters WHERE name = ?),
                        (SELECT id FROM levels WHERE name = ?),
                        (SELECT id FROM producers WHERE name = ?)
                    )
                    """,
                    (Time, Parameter, Level, Source)
            )
        except sqlite3.Error as error:
            print("Error during inserting event!\n", error)

    
        id_event = self.cursor.lastrowid

        # Получение имени таблицы для сохрания данных
        try:
            self.cursor.execute(
                    """
                    SELECT table_name FROM units WHERE id = (SELECT id_unit FROM parameters WHERE name = ?) 
                    """,
                    (Parameter, )
	      )
        except sqlite3.Error as error:
            print("Error finding table name!\n", error)
	
        table_name = self.cursor.fetchall()[0][0]
    
        # Сохранение данных
        try:
            self.cursor.execute(
                    "INSERT INTO " + table_name + " (id, value) VALUES (?, ?)",
                    (id_event, Value)
            )
        except sqlite3.Error as error:
            print("Error during inserting value!\n", error)

    def log_json(self, s):
        """
        Функция для выполнения сохранения параметра, принятого в
        формате JSON.
        """

        try:
            events = json.loads(s)
        except json.decoder.JSONDecodeError as error:
            print("Error in JSON line!", error)
            return

        for event in events["Events"]:
            self.log(event["Parameter"], event["Level"], event["Source"], event["Time"], event["Value"])

#logger = db_logger()
#logger.open_database("../db/test.db")

#with open('../db/test.json') as f:
#    s = f.read()
#logger.log_json(s)


#logger.close_database()
#del(logger)


"""
try:
    sqlite_connection = sqlite3.connect("../db/test.db")
    cursor = sqlite_connection.cursor()
except sqlite3.Error as error:
    print("Error during connection to database!", error)

current_time = datetime.datetime.now()
time_stamp1 = current_time.timestamp()

current_time = datetime.datetime.now()
time_stamp = current_time.timestamp()
date_time = datetime.datetime.fromtimestamp(time_stamp)

# for i in range(0,1):
#     Log(cursor, 'MB1', "INFO", "GENERATOR", date_time, 1.23)

with open('../db/test.json') as f:
    s = f.read()
Log_json(cursor, s)


current_time = datetime.datetime.now()
time_stamp2 = current_time.timestamp()
print(time_stamp2 - time_stamp1)
"""
#sqlite_connection.commit()  
#sqlite_connection.close()
