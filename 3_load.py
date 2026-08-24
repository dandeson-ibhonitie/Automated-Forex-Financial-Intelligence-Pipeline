import sqlite3
import pandas as pd

df_clean = pd.read_csv("Cleaned_rates.csv") #reading the csv file to memory



conn = sqlite3.connect("forex_warehouse.db") #Establishing a connection to sqlite3 database
cursor = conn.cursor()




cursor.execute("""
CREATE TABLE IF NOT EXISTS exchange_logs (
    Currency TEXT,
    Rate REAL,
    Risk_Status TEXT,
    Execution_Date TEXT,
    PRIMARY KEY (Currency, Execution_Date) -- This acts as our duplicate blocker!
);
""") 
conn.commit()



#  creating a new column and using try and except method to guaranttee data integrity

try:
    df_clean.to_sql("exchange_logs", con=conn, if_exists="append", index=False)
    conn.commit()
    print(" Success: Fresh financial metrics appended to warehouse tracks.")
    
except sqlite3.IntegrityError:
    print(" Status: Duplicate data detected for this date. Ingestion skipped to protect data integrity.")



#  Auditing querry validation with pandas

verification_df = pd.read_sql_query("SELECT * FROM exchange_logs;", conn)


print("\n .....VERIFICATION LOG......")
print(verification_df) #viewing the risk_status  

conn.close() #closing the connection 
print("DataBase connection safely closed")





                       

                         

