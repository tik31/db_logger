import json
import sqlite3
import datetime
import os

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
            self.sqlite_connection = sqlite3.connect(db_path, check_same_thread = False)
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

    def create_database(self, db_path):

        # Чтение SQL-скрипта для инициализации БД
        try:
            sql_path = os.path.dirname(os.path.abspath(__file__))
            with open(sql_path + '/sql/create_db.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            self.cursor.executescript(sql_script)
        except IOError as error:
            print("Cann't open file")
        except sqlite3.Error:
            print("Error during creating DB")
        self.sqlite_connection.commit()


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

        self.sqlite_connection.commit()

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

        if isinstance(events, list):
            for event in events:
                self.log(event["Parameter"], event["Level"], event["Source"], event["Time"], event["Value"])
        else:
            self.log(events["Parameter"], events["Level"], events["Source"], events["Time"], events["Value"])
