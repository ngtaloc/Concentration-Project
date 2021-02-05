import pyodbc

class DBConnet():

    @staticmethod
    def getConnet():
        try:
            conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                  #Loc
                                  #'Server=DESKTOP-4UPPHLQ\SQLEXPRESS;' 'Database=db_DACN;'
                                  #'Server=(LocalDB)\MSSQLLocalDB;' 'Database=dbDACN;'
                                  
                                  # Hau
                                  #'Server=DESKTOP-LM0C49R\SQLEXPRESS;' 'Database=DOAN_CHUYENNGANH;'
                                  
                                  # QUOC
                                  'Server=DESKTOP-TD9R29S;' 'Database=chuyen_nganh;'
                                  'Trusted_Connection=Yes'
                                  )
            return conn
        except Exception as e:
            print(e)
