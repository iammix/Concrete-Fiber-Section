import sqlite3
import pandas as pd


class Store:
    def __init__(self, dbname):
        self.dbname = dbname

    def make_table(self, input_file, tablename):
        df = pd.read_csv(input_file)
        conn = sqlite3.connect(self.dbname)
        df.to_sql(tablename, conn, if_exists="replace", index=None)
        conn.close()

    def conv_pd_data(self, df, tablename):
        conn = sqlite3.connect(self.dbname)
        df.to_sql(tablename, conn, if_exists='replace', index=None)
        conn.close()

    def conv_csv(self, tablename, out_file):
        conn = sqlite3.connect(self.dbname)
        df = pd.read_sql_query(f"SELECT * FROM {tablename}", conn)
        df.to_csv(out_file, header=True, index=None)
        conn.close()
