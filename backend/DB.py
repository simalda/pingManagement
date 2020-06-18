import mysql.connector


class SQL(object):
    def __init__(self):
         self.mydb = mysql.connector.connect(
            host="localhost",
            user="roma",
            password="Aa123456",
            database="ping_management"
          )

    def getPings(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM pings")
        myresult = mycursor.fetchall()
        print(type(myresult))
        for x in myresult:
          print(x)
        return myresult
 
 



 