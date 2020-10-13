import pyodbc
import sys
from pathlib import Path

# import preferences


server = r'edwpub.s.uw.edu'
database = r'UWSDBDataStore'

## Users must add a file a the same level as this module. Name the file 'preferences.py' and add:
## USERNAME = 'NETID\<your username>'
## PWD = '<your password>'
# username = preferences.USERNAME
# password = preferences.PWD



def get_cursor():

    try:
        # print('Looking for usable DSN')
        conn = pyodbc.connect('DSN=EDW')
    except pyodbc.OperationalError:
        try:
            print('DSN unavailable. Trying to use mssql driver.')
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=edwpub.s.uw.edu;DATABASE=UWSDBDataStore;UID='+username+';PWD='+password+';')
        except pyodbc.InterfaceError:
            try:
                # print('No usable mssql driver. Attempting to connect via FreeTDS')
                # db = input('Enter database name: ')
                conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=edwpub.s.uw.edu; PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password+';')
            except pyodbc.OperationalError:
                print("Not able to connect with provided methods")
                sys.exit()
        except pyodbc.OperationalError:
            try:
                # print('No usable mssql driver. Attempting to connect via FreeTDS')
                # db = input('Enter database name: ')
                conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=edwpub.s.uw.edu; PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password+';')
            except pyodbc.OperationalError:
                print("Not able to connect with provided methods")
                sys.exit()
        finally:
            conn.close()
            
                

    
  

    # print('Connection to database successful')
    return conn.cursor()


if __name__ == '__main__':
    cur = get_cursor('UWSDBDataStore')
    cur.execute("SELECT 'YES'")