# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 22:00:44 2020

@author: Alin Caia
"""
import mysql.connector as mysql
import pandas as pd

#Initializing the Database connection with the proper credentials
db = mysql.connect(
    host="localhost",
    user="alincaia",
    password="dawson",
    database="test_project1",
    auth_plugin="mysql_native_password")

#Initializing the DataFrame object that will contain all the necessary data from the database
pandemic_data = pd.read_sql("SELECT d.dayname, c.countryother as 'country', c.totalcases, c.totaldeaths, c.totalrecovered, c.deathsper1m, c.totaltests, c.population FROM country c JOIN day d USING (dayid)", db)
#Initializing the list that will hold all the countries selected
countries_list = []
#data_science must be global
data_science = pd.DataFrame()


def main():
    #ask user to input 5 countries
    for x in range(0,5):
        countries_list.append(input_user_country())
    #analyse the data of these countries
    data_science = analyze_country_data(countries_list)
    #The data_science object is going to be returned to the 1.4 module when we need to show the plots
    return data_science

def analyze_country_data(chosen_countries_list):
    #hold the data frame of each country
    data_frames_list = []
    #iterate through the list of chosen countries
    for country in chosen_countries_list:
        #set up the columns and data needed
        #calculate the difference of the data of today and 2 days ago
        country_data_analysis = pd.read_sql("SELECT present.countryother as 'country', present.population as 'population', present.totalcases as 'totalcases_today', past.totalcases as 'totalcases_yesterday', past2.totalcases as 'totalcases_2_days_ago', (present.totalcases - past2.totalcases) as 'totalcasesDiff', present.totaldeaths as 'totaldeaths_today', past.totaldeaths as 'totaldeaths_yesterday', past2.totaldeaths as 'totaldeaths_2_days_ago', (present.totaldeaths - past2.totaldeaths) as 'totaldeathsDiff', present.totalrecovered as 'totalrecovered_today', past.totalrecovered as 'totalrecovered_yesterday', past2.totalrecovered as 'totalrecovered_2_days_ago', (present.totalrecovered - past2.totalrecovered) as 'totalrecoveredDiff', present.deathsper1m as 'deathsper1m_today', past.deathsper1m as 'deathsper1m_yesterday', past2.deathsper1m as 'deathsper1m_2_days_ago', (present.deathsper1m - past2.deathsper1m) as 'deathsper1mDiff', present.totaltests as 'totaltests_today', past.totaltests as 'totaltests_yesterday', past2.totaltests as 'totaltests_2_days_ago', (present.totaltests - past2.totaltests) as 'totaltestsDiff' FROM country present JOIN country past USING (countryother) JOIN country past2 USING (countryother) WHERE present.dayid = 1 AND past.dayid = 2 AND past2.dayid = 3 AND present.countryother = '%s'" % country, db)
        j = 0
        for diff, i in zip(country_data_analysis.columns, range(1, len(country_data_analysis.columns)+1)):
            #find all columns that hold the difference
            if(diff[-4:] == 'Diff'):
                #find out whether the numbers have increased, decreased, or not changed since 2 days ago
                if(country_data_analysis[diff].values[0] > 0):
                    country_data_analysis.insert(i+j, str(diff + 'Change'), 'increase')
                elif(country_data_analysis[diff].values[0] < 0):
                    country_data_analysis.insert(i+j, str(diff + 'Change'), 'decrease')
                else:
                    country_data_analysis.insert(i+j, str(diff + 'Change'), 'no change')
                j+=1
        #put the found data in the DataFrame list
        data_frames_list.append(country_data_analysis)
    #return the DataFrames of all selected countries combined into one DataFrame
    return pd.concat(data_frames_list)

def input_user_country():
    #ask user to input a VALID country to analyze
    #keep asking user to input a country until they select a valid one
    while(True):
        country = str(input("Enter a country to analyze: "))
        #verify that user hasn't already selected this country by checking the global list of countries selected
        if(country_in_list(country, countries_list)):
            print("You've already selected this country")
            continue
        #verify that the country exists in the database
        elif(not(country_in_list(country, pandemic_data["country"]))):
            print("The country you've selected does not exist in the database")
            continue
        else:
            return country

def country_in_list(country_chosen, countries):
    for country in countries:
        if(country == country_chosen):
            return True
    return False