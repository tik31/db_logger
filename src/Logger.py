import sqlite3
import datetime

def Log(cursor, Parameter, Level, Source, Time, Value):
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
        cursor.execute(
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

    
    id_event = cursor.lastrowid

    # Получение имени таблицы для сохрания данных
    try:
        cursor.execute(
                """
                SELECT table_name FROM units WHERE id = (SELECT id_unit FROM parameters WHERE name = ?) 
                """,
                (Parameter, )
	   )
    except sqlite3.Error as error:
        print("Error finding table name!\n", error)
	
    table_name = cursor.fetchall()[0][0]
    
    # Сохранение данных
    try:
        cursor.execute(
                "INSERT INTO " + table_name + " (id, value) VALUES (?, ?)",
                (id_event, Value)
        )
    except sqlite3.Error as error:
        print("Error during inserting value!\n", error)


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

for i in range(0,1):
    Log(cursor, 'MB1', "INFO", "GENERATOR", date_time, 1.23)

current_time = datetime.datetime.now()
time_stamp2 = current_time.timestamp()
print(time_stamp2 - time_stamp1)

sqlite_connection.commit()  
sqlite_connection.close()
