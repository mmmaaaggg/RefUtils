from mysql.connector import (connection)

# Connect with the MySQL Server
cnx = connection.MySQLConnection(user='root',
                                 password='Pa5Svv()rd',
                                 host='127.0.0.1',
                                 database='sm_db')
cnx.close()
