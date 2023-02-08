# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:47:17 2020

@author: Daniel
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# data visualization
import seaborn as sns

#This module will call the main method of data_analysis which will create the dataframe object. Using that object, we shall plot the data.
from data_analysis import main as data_analysis_main, country_in_list as data_analysis_country_in_list
pd.set_option("display.max_rows", None, "display.max_columns", None)

selected_countries = []

def main():
    print("""
          Selected 1 to display : The difference between the current death toll/1m population for today and 2 days ago
          Selected 2 to display : The trend line compares the number of total cases in the last 3 days for 5 countries
          Selected 3 to display : The total tests vs total recovered for today
          """)

    while(True):
        try:
            userInput = int(input('Enter selection: '))
            if(userInput == 1):
                plot_current_death_toll_per_1m()
                break
            elif userInput == 2:
                plot_trendline()
                break
            elif userInput == 3:
                plot_total_recovered_vs_total_tests()
                break
            print('Choose either 1, 2 or 3')
        except Exception:
            print('Choose either 1, 2 or 3')


  
#Creates a bar plot comparing the difference between the current death toll/1m population for today and 2 days ago. (5 countries)
def plot_current_death_toll_per_1m():
    #The user will repeatedly enter 5 countries if the countries have been selected before or aren't comparable
    while True:
        data_science = data_analysis_main()
        if areCountriesDeathTollPer1mComparable(data_science):
            if areCountriesNotAlreadySelected(data_science['country']):
                selected_countries.extend(data_science['country'].tolist())
                break
            print('1 or more countries were already selected. Select again')
            print()
            continue
        print('The countries are not comparable. Select again')    
        print()
            

    index = np.arange(5)
    bar_width = 0.35
    
    fig, ax = plt.subplots()
    
    ax.bar(index, data_science['deathsper1m_2_days_ago'], bar_width, label='2 Days Ago')
    
    ax.bar(index+bar_width, data_science['deathsper1m_today'],bar_width, label='Today')
    
    ax.set_xlabel('Country')
    ax.set_ylabel('Total Deaths')
    ax.set_title('Difference between the current death toll/1m population for today and 2 days ago')
    ax.set_xticks(index + bar_width / 2)
    
    ax.set_ylim(data_science['deathsper1m_today'].min() - 100,data_science['deathsper1m_today'].max() + 100)
    
    ax.set_xticklabels([selected_countries[0], selected_countries[1], selected_countries[2], selected_countries[3], selected_countries[4]])
    ax.legend()
    plt.show()
       
#Plots a trend line for 
def plot_trendline():
    #The user will repeatedly enter 5 countries if the countries have been selected before or aren't comparable
    while True:
        data_science = data_analysis_main()
        if areCountriesNotAlreadySelected(data_science['country']):
            selected_countries.extend(data_science['country'].tolist())
            break
        print('1 or more countries were already selected. Select again')
        print()
        
    days = [1, 2, 3]
    
    index = np.arange(4)
    
    fig, ax = plt.subplots()
    
    plt.style.use('seaborn-whitegrid')
    
    for i in range(0,5):
        data = [data_science['totalcases_2_days_ago'].tolist()[i], data_science['totalcases_yesterday'].tolist()[i], data_science['totalcases_today'].tolist()[i]]
        connectpoints(days, data, 0, 1)
        connectpoints(days, data, 1, 2)
    
    ax.set_title('Total Cases Trend Line Comparison')
    
    ax.set_xlabel('Days')
    ax.set_ylabel('Number of Cases')
    ax.set_xticks(index)
    ax.set_xticklabels([0, '2 Days Ago', 'Yesterday', 'Today'])
    
    ax.legend()
    plt.show()

#The bar plot for 5 other countries comparing the Total Recovered and Total tests for today.
def plot_total_recovered_vs_total_tests():
    #The user will repeatedly enter 5 countries if the countries have been selected before or aren't comparable
    while True:
        data_science = data_analysis_main()
        if totalRecoveredandTotalTestsCheck(data_science):
            if areCountriesNotAlreadySelected(data_science['country']):
                selected_countries.extend(data_science['country'].tolist())
                break
            print('1 or more countries were already selected. Select again')
            print()
            continue
        print('The countries are not comparable. Select again')  
        print()
        
    index = np.arange(5)
    
    fig, axes = plt.subplots(2)
    
    axes[0].bar(index, data_science['totaltests_today'], label='Total Tests', color=['red','red','red','red','red'])
    
    axes[1].bar(index, data_science['totalrecovered_today'], label='Total Recovered',color=['green','green','green','green','green'])
    
    axes[1].set_xlabel('Country')
    
    axes[0].set_ylabel('Total Tests')
    axes[1].set_ylabel('Total Recovered')
    
    axes[0].set_title('Total Tests vs Total Recovered')
    
    axes[0].set_xticks(index)
    axes[1].set_xticks(index)
    
    axes[0].set_ylim(data_science['totaltests_today'].min() - 1000000, data_science['totaltests_today'].max() + 1000000)
    axes[1].set_ylim(data_science['totalrecovered_today'].min() - 100000, data_science['totalrecovered_today'].max() + 100000)
    
    axes[0].set_xticklabels([None,None,None,None,None])
    axes[1].set_xticklabels([selected_countries[0], selected_countries[1], selected_countries[2], selected_countries[3], selected_countries[4]])
    plt.show()
    
    

#Checks if the new countries to be plotted have not been previously entered.
def areCountriesNotAlreadySelected(countries):
    for country in countries:
        if data_analysis_country_in_list(country,selected_countries):
            return False
    
    return True

#Checks if the countries are comparable for the Death toll / 1M plot
def areCountriesDeathTollPer1mComparable(data):
    countries = data['deathsper1m_today']
    
    #the countries death toll / 1m should not have differences greater than 300
    if countries.max() - countries.min() > 300:
        return False
       
    #return true if the death toll / 1m are comparable
    return True
        
#The bar plot for the total recovered and total tests must have comparable data       
def totalRecoveredandTotalTestsCheck(data):
    totalRecovered = data['totalrecovered_today']
    totalTests = data['totaltests_today']
    
    if totalRecovered.max() - totalRecovered.min() > 300000:
        return False
    
    if totalTests.max() - totalTests.min() > 9000000:
        return False
    
    #return true if the total recovered and total tests for all 5 countries are comparable
    return True



def connectpoints(x,y,p1,p2):
    x1, x2 = x[p1], x[p2]
    y1, y2 = y[p1], y[p2]
    plt.plot([x1,x2],[y1,y2],'k-')
    
    
    
if __name__ == "__main__":    
    main()