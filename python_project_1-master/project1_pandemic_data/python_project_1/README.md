# Python_Project_1

This project involves web scraping, database management, and data analysis. This project 
consists of obtaining Covid-19 data from the web, storing it in a database, analyzing/comparing 
the data, and creating charts about the data (plotting it). A couple of modules are used to 
handle this project.

web_data_scraping.py: This module is used to scrape data from a website 
(https://www.worldometers.info/coronavirus/) and storing the data in a json 
file called country_neighbour_dist_file.json. This module will scrape data from the a website, 
then store the html contents of what was scraped in an html file called website_data.html. The html file's 
purpose is to avoid being prevented from scraping data from the website after many attempts. This means 
the module will scrape data directly from the html file if it exists, which is why you must delete it if you 
wish to scrape new data from the website. Once the data is scraped, this module stores the data in a json file 
using one big structured dictionary.

data_archiving.py:

data_analysis.py: This module is used to analyze data for 5 countries. The user will need to input 5 countries. 
This module will use pandas to create DataFrame objects that will hold data from the database. This module then 
analyzes 5 data that we considered important (Total Cases, Total Deaths, Total Recovered, Deaths/1M Pop, Total Tests) 
by finding the difference between the data of today and the data of 2 days ago. With this, we can determine whether 
the country has had an increase, a decrease, or nothing for this data in question. Apart from these 5 data, a DataFrame 
will hold the country name, the population (useful for part 1.4 of this project) the values (original data, difference, 
and increase/decrease/nothing) of the 5 important data. An analysis will be performed on all 5 of the selected countries 
and all these 5 DataFrame objects will be combined together and stored in a global variable for part 1.4 to access.