import sensitiveData as SD
import mysql.connector


class MYSQL:
    def __init__(self):
        self.host = SD.databaseHost
        self.user = SD.databaseUser
        self.password = SD.databasePassword
        self.database = SD.database


    def createConnection(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)

        return connection
