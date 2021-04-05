#2.03 Drifter Blue's Weather Measurements Website
# Flask Setup
import os
import pandas as pd 
from pandas import DataFrame
from flask import Flask, make_response, request, abort, render_template
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

def Average(lst):
    average = sum(lst) / len(lst)
    average = round(average, 2)
    return average

# GET Route to get all Data
@app.route('/', methods = ['GET', 'POST'])
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

    if request.method == 'POST':
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

    # Create dictionary of list values to organize unique month/days
    dates = {} 
    for i in df.Month:
        dates[i] = []
        for j in df.Month[df.Month == i].index:
            if df.Day[j] not in dates[i]:
                dates[i].append(df.Day[j])
    print(dates)

    allDailyRecords = {}
    allMonthlyRecords = {}
    for Month in dates.keys():    
        allMonthlyRecords[Month] = {}
        for Day in dates[Month]:
            df_ = df[(df.Month == Month) & (df.Day == Day)] 
            print(Month, Day)
            labels = df_['Hour'] 
            labelsM = df_['Minute']
            time = zip(labels, labelsM)
            timeList = list(time)

            intTemp = df_['Int-Temp']
            extTemp = df_['Ext-Temp']
            tds = df_['TDS']
            salt = df_['Salinity']
            con = df_['Concentration']
            battery = df_['Battery']
        
            recordDailySet = [intTemp, extTemp, tds, salt, con, battery, timeList]
            allDailyRecords[(Month, Day)] = recordDailySet

            recordAvgSet = [Average(intTemp), Average(extTemp), Average(tds), Average(salt), Average(con), Average(battery)]
            allMonthlyRecords[Month][Day] = recordAvgSet
        

    print(allMonthlyRecords[3])

    return render_template('charts.html', dailyValues = allDailyRecords, monthlyValues = allMonthlyRecords)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 80))