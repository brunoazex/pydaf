from ..app import App
import psycopg2
from psycopg2 import Error

class Postgres():   
    def query(sql):        
        """
        Fetches data from database with specified sql

        Parameters
        ----------
        sql : str
            SQL that will be executed

        Returns
        -------
        A Tuple filled with fields and rows from fetched data
        """
        if (sql is None):
            raise Exception("SQL not specified")        
        try:
            database = App.instance().environment.database
            connection = psycopg2.connect(host=database.host, dbname=database.database, 
                                            user=database.user, password=database.password)
            cursor = connection.cursor()
            cursor.execute(sql)
            fields = [ x[0] for x in cursor.description]
            return (fields, cursor.fetchall())
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error connecting to database", error)
        finally:
            if not connection is None:
                cursor.close()
                connection.close()
