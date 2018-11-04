import mysql.connector as mariadb
import config

mariadb_connection = mariadb.connect(user = config.username, password = config.password, database = config.database_name)
cursor = mariadb_connection.cursor()