#2.03 Drifter Blue's Weather Measurements Website
# Flask Setup
import os
import numpy as np
import pandas as pd 
from pandas import DataFrame
from flask import Flask, request, abort, render_template
app = Flask(__name__)

# Google Sheets API Setup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                              ["https://spreadsheets.google.com/feeds",                                                               
                                                              "https://www.googleapis.com/auth/spreadsheets",                                                        
                                                              "https://www.googleapis.com/auth/drive.file",                                                        
                                                              "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
gsheet = client.open("drifterBlueData.CSV").sheet1

# GET Route to get all Data
@app.route('/', methods = ['GET'])
def chart():
    #GET all data and convert into DataFrame
    records = gsheet.get_all_records()
    df = pd.DataFrame.from_dict(records, orient='columns')
    #Split Date column into multiple columns for simplified sorting
    df[["Month", "Day", "Year"]] = df["Date"].str.split(pat="/", expand=True)
    df["Day"] = pd.to_numeric(df["Day"])
    df["Month"] = pd.to_numeric(df["Month"])
    df["Year"] = pd.to_numeric(df["Year"])
    #Split Time column into multiple columns for simplified sorting
    df[["Hour", "Minute"]] = df["Time"].str.split(pat=":", expand=True)
    df["Hour"] = pd.to_numeric(df["Hour"])
    df["Minute"] = pd.to_numeric(df["Minute"])
    #Sort data in ascending order beginning from year all the way to minutes
    df = df.sort_values(['Year', 'Month', 'Day', 'Hour', 'Minute'], ascending = [True, True, True, True, True])
    print(df)
    #Create a list of only the unique days in a month without duplicates (1-31)
    days = df['Day'].unique() 
    print(dates)

    allRecords = {}
    for Day in days:
        df_ = df.query('Day==' + str(Day))
        labels = df_['Hour'] 
        
        extTemp = df_['Ext-Temp']
        tds = df_['TDS']
        salt = df_['Salinity']
        con = df_['Concentration']
        battery = df_['Battery']

        recordSet = [extTemp, tds, salt, con, battery, labels]
        allRecords[Day] = recordSet

    return render_template('charts.html', days = days, values = allRecords)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 80))