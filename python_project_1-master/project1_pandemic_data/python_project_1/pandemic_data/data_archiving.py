# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 20:53:43 2020

1.1 Archive data in a database
The data written in the file country_neighbour_dist_file.json will be saved into a MySQL database

@author: Daniel
"""
import mysql.connector as mysql
import os
import json


#Initializing the Database connection with the proper credentials
db = mysql.connect(
    host="localhost",
    user="alincaia",
    password="dawson",
    database="test_project1",
    auth_plugin="mysql_native_password")

#Initializing the cursor for the database
cursor = db.cursor(buffered = True)

    
#verify that the country_neighbour_dist_file.json file exists, if not then display an error message
def main():
    if(os.path.exists("country_neighbour_dist_file.json")):
        with open("country_neighbour_dist_file.json", "r", encoding='utf-8') as read_file:
            print("The file exists")
            json_file_dict = json.load(read_file)
            createTables(json_file_dict)
        
    else:
        print("The file 'country_neighbour_dist_file.json' could not be found!")
        

#create the tables Day and Country
def createTables(json_file_dict):
    #The day table will have a 1-to-many relationship with the country table
    cursor.execute("CREATE TABLE DAY(DAYID INT AUTO_INCREMENT PRIMARY KEY, DAYNAME VARCHAR(50))")
    
    db.commit()

    #Creation of the country table. Every day will have 'X' amount of entries in this table
    cursor.execute("""
                   CREATE TABLE COUNTRY(
                       DAYID INT REFERENCES DAY(DAYID),
                       CountryNumber VARCHAR(3),
                       CountryOther VARCHAR(100),
                       TotalCases INT,
                       NewCases INT,
                       TotalDeaths INT,
                       NewDeaths INT,
                       TotalRecovered INT,
                       NewRecovered INT,
                       ActiveCases INT,
                       SeriousCritical INT,
                       CasesPer1M INT,
                       DeathsPer1M INT,
                       TotalTests INT,
                       TestsPer1M INT,
                       Population INT,
                       Continent VARCHAR(50),
                       1CaseEveryXppl INT,
                       1DeathEveryXppl INT,
                       1TestEveryXppl INT)                     
                   """)

    db.commit()

    #Pass the dictionary object so we can fill the tables with the data from the json file    
    fillTablesWithData(json_file_dict)

#Fill the created tables with the contents of the dictionary json_file_dict
def fillTablesWithData(json_file_dict):
    #fill the day table with all 3 days 
    for day in json_file_dict:
        insert_day_query = "INSERT INTO DAY(DAYNAME) VALUES (%s)"
        cursor.execute(insert_day_query,(day,))
    
        db.commit()

    
    #specificDay represents (today, yesterday, yesterday2)
    for specificDay in json_file_dict:
        
        #This variable will be used to reference a row in Day table from the Country table
        dayPrimaryKey = 0
        if specificDay == "today":
            dayPrimaryKey = 1
        elif specificDay == "yesterday":
            dayPrimaryKey = 2
        else:
            dayPrimaryKey = 3
            
        
      
        #The amount of rows in the table
        totalRows = len(json_file_dict[specificDay]['#'])
        
        #incrementing this allows us to move on to the next column for a specific country.
        columnPosition = 0
        
        #We want to repeat this process for every country for this day.
        for row in range(0,totalRows):
            
             #This list will be converted into a tuple for the sql insert. It represents all the data relating to one country.
             queryInsertValues = []
             queryInsertValues.append(dayPrimaryKey)
            
             #for every country, iterate through its columns
             for tableColumn in json_file_dict[specificDay]:
                #The table data in a specific column
                columnData = json_file_dict[specificDay][tableColumn][columnPosition]
                #cleaning up the data so numbers(int) will not have ',' and numbers with '+' will be plain ints.
                columnData = columnData.replace(',','').replace('+','')
                
                #empty data or 'N/A' is replaced with 0 for cleaner data in the database
                if(columnData == '' or columnData == 'N/A'):
                    columnData = 0
                elif(columnData.isnumeric()):
                    columnData = int(columnData)
                    

                #The data is to be added to the list relating to a single country insert
                queryInsertValues.append(columnData)
            
             #create an entry for this country in the database
             sql_country_insert = "INSERT INTO COUNTRY VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
             
             cursor.execute(sql_country_insert, tuple(queryInsertValues))
             
             db.commit()
             
             #increment since we are now looking at the next column for one specific country
             columnPosition = columnPosition + 1
    


#cursor.execute("DROP TABLE IF EXISTS DAY")  
#cursor.execute("DROP TABLE IF EXISTS COUNTRY")

main();

        