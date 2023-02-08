# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:22:22 2020

@author: Alin Caia
"""
from bs4 import BeautifulSoup
import json
import requests
import os

#if you want to restart the data scraping procedure, 
#you need to have deleted the website_data.html file before running this module
def main():
    try:
        #if the html file exists in this project's directory structure, 
        #then it would be safer to scrape data directly from the html file instead of the website
        if(os.path.exists("website_data.html")):
            scrape_from_html_file()
        else:
            scrape_from_website()
            
    except Exception as error:
        print(error)
        print('Could not scrape data')
    
def scrape_from_website():
    try:
        #get the html info from the website
        url = "https://www.worldometers.info/coronavirus/"
        req = requests.get(url) #http request to the web site 
        soup = BeautifulSoup(req.text, "html.parser")
        
        #find all tables of data (from today, 1 day ago, and 2 days ago)
        table_today = soup.find(id="main_table_countries_today")
        table_yesterday = soup.find(id="main_table_countries_yesterday")
        table_yesterday2 = soup.find(id="main_table_countries_yesterday2")
        
        #store them in a specific html file (overwriting the old file if it exists)
        with open("website_data.html", "w") as write_file:
            write_file.write(str(table_today) + '\n' + str(table_yesterday) + '\n' + str(table_yesterday2))
        
        #now that you have the html file, scrape from there
        scrape_from_html_file()
        
    except Exception as error:
        print(error)
        print('Could not scrape data from website')
    
def scrape_from_html_file():
    try:
        #get the html data from the stored html file
        with open("website_data.html", "r") as read_file:
            soup = BeautifulSoup(read_file, "html.parser")
            
        #find all tables of data (from today, 1 day ago, and 2 days ago)
        table_today = soup.find(id="main_table_countries_today")
        table_yesterday = soup.find(id="main_table_countries_yesterday")
        table_yesterday2 = soup.find(id="main_table_countries_yesterday2")
            
        #find the headers from each table (the headers are the same for each table)
        table_headers = table_today.find_all('th')
        
        #find the rows of each table
        table_today_rows = table_today.find_all('tr')
        table_yesterday_rows = table_yesterday.find_all('tr')
        table_yesterday2_rows = table_yesterday2.find_all('tr')
        
        #put all of this info inside of one giant dict with multiple nested dicts
        #outer-most dict contains dicts representing the day
        today = {}
        yesterday = {}
        yesterday2 = {}
        json_file_dict = {
            'today' : today,
            'yesterday' : yesterday,
            'yesterday2' : yesterday2
        }
        
        #the day dict contains dicts representing the table columns
        for field in table_headers:
            json_file_dict['today'][field.text.strip()] = []
            json_file_dict['yesterday'][field.text.strip()] = []
            json_file_dict['yesterday2'][field.text.strip()] = []
        
        #the table columns lists contain the data associated with their particular column in the table
        #store the data recorded today
        first9Rows = 0
        for row in table_today_rows:
            #skip the header row and the rows where continents of 'world' are stored in the country column
            if(first9Rows >= 9 and first9Rows <= 226):
                #find the data inside of each row (excluding the headers)
                table_today_data = row.find_all('td')
                #put it in the appropriate location in the dictionary
                for table_column, data_cell in zip(table_headers, table_today_data):
                    json_file_dict['today'][table_column.text.strip()].append(data_cell.text.strip())
            first9Rows+=1
        
        #store the data recorded yesterday
        first9Rows = 0
        for row in table_yesterday_rows:
            #skip the header row and the rows where continents of 'world' are stored in the country column
            if(first9Rows >= 9 and first9Rows <= 226):
                #find the data inside of each row (excluding the headers)
                table_yesterday_data = row.find_all('td')
                #put it in the appropriate location in the dictionary
                for table_column, data_cell in zip(table_headers, table_yesterday_data):
                    json_file_dict['yesterday'][table_column.text.strip()].append(data_cell.text.strip())
            first9Rows+=1
        
        #store the data recorded 2 days ago
        first9Rows = 0
        for row in table_yesterday2_rows:
            #skip the header row and the rows where continents of 'world' are stored in the country column
            if(first9Rows >= 9 and first9Rows <= 226):
                #find the data inside of each row (excluding the headers)
                table_yesterday2_data = row.find_all('td')
                #put it in the appropriate location in the dictionary
                for table_column, data_cell in zip(table_headers, table_yesterday2_data):
                    json_file_dict['yesterday2'][table_column.text.strip()].append(data_cell.text.strip()) 
            first9Rows+=1
        
        #put this giant dictionary in a json file (overwriting file if exists)
        with open("country_neighbour_dist_file.json", "w", encoding='utf-8') as write_file:
            json.dump(json_file_dict, write_file, ensure_ascii=False)
    
    except FileNotFoundError as file_not_found_error:
        print(file_not_found_error)
        print('Could not find either html file or json file')
        
    except Exception as error:
        print(error)
        print('Could not scrape data from html file')
        
if __name__ == "__main__":    
    main()