import pandas as pd
import json



#Loading the raw text snapshot back into memory

with open("raw_rates.json", "r") as file:
    raw_json = json.load(file)

rates_dict = raw_json["rates"]


#Extract and create the initial DataFrame
df = pd.DataFrame(list(rates_dict.items()), columns=["Currency", "Rate"])


#Filter to target currencies

target_currencies = ['NGN','KES','GBP','EUR']
df_filtered = df[df["Currency"].isin(target_currencies)].copy()



#Defining and apply Volatility Risk function

def check_volatility(row):
    Currency = row["Currency"]
    Rate = row["Rate"]
    if Currency == "NGN" and Rate >= 1500.0:
        return "High Risk"
    if Currency =="GBP" and Rate >= 0.80:
        return "High Risk"
    if Currency == "KES" and Rate >= 130.0:
        return  "High Risk" 
    if Currency == "Eur" and Rate >=0.95:
        return "High Risk"
    else:
        return "Stable"


#Creating a new column

df_filtered["Risk_Status"] = df_filtered.apply(check_volatility, axis = 1)


#Clean missing/dead rates

df_filtered = df_filtered.dropna(subset = ["Rate"])
df_filtered = df_filtered[df_filtered["Rate"] > 0]


#creating a timestamp to make sure only data at a given day is collected

df_filtered["Execution_Date"] = raw_json.get(
    "time_last_update_utc", "Unknown"
)
        

#Saving the final results to a CSV file

df_filtered.to_csv("Cleaned_rates.csv", index=False)

print("Cleaned_rates.csv created")
                  

    
    

    