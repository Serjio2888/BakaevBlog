import pymysql

def get_c(login = "root", password = "serjio12", db_name = "bakaev_blog"):
    connection = pymysql.connect(host='localhost', user=login,
                                 password=password, db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
