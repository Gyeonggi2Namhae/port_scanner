import pymysql

from config import Config 

def connect_to_db():
    conn = pymysql.connect(
        host = Config.DB_CONFIG['host'], #RDS Endpoint
        user = Config.DB_CONFIG['user'], 
        password = Config.DB_CONFIG['password'],
        database = Config.DB_CONFIG['database'], #main DB
        port = Config.DB_CONFIG['port'],
        charset = Config.DB_CONFIG['charset'],
        cursorclass = pymysql.cursors.DictCursor
    )
    return conn

#테이블 "well_known_port_list" 조회
#port_number : 포트 번호
#service_name : 포트에서 작동하는 서비스명
#port_description : 서비스에 대한 설명
def get_all_list():
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT port_number, service_name, port_description FROM well_known_port_list"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        conn.close()
    return data

def get_custom_list():
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT port_num, service_name, port_desc FROM unknown_port"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        conn.close()
    return data
