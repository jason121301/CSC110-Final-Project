"""CSC110 Fall 2020 Project: Relationship between Climate Change, Pollution, and Productivity of a Nation

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of graders
grading this project and people who has permission from the creator to use. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Jason Sastra

This file contains the main page to run the functions in"""


import datetime
from dataclasses import dataclass
from typing import Optional
import converting_data
import helper_functions
import draw_graph
import global_map


@dataclass
class GlobalTemperature:
    """The dataset from GlobalTemperatures.csv, formatted to show three variables, date in datetime.date,
    average temperature, uncertainty in average temperature
    Attributes
        - date: the datetime in datetime.date format, with year-month-day
        - temperature: average temperature of the world in floats
    """
    date: datetime.date
    temperature: Optional[float]


@dataclass
class CountryTemperature:
    """The dataset from GlobalLandTemperaturesByCountry.csv, formatted  to show three variables, date in datetime.date
    average temperature, and the country itself
    Attributes
        - date: the datetime in datetime.date format, with year-month-day
        - temperature: average temperature of the country in floats
        - country: the name of the country in strings
    """
    date: datetime.date
    temperature: Optional[float]
    country: str


@dataclass
class CO2Emission:
    """The dataset from UNdata_Export_20201102_015629836,
    Carbon dioxide (CO2) Emissions without Land Use,
    Land-Use Change and Forestry (LULUCF), in kilotonne CO2 equi.csv, formatted to show three variables,
    country or area, year, emission
    Attributes
        - date: the datetime in datetime.date format, with every month and date being January 1st
        - emission: The emission as a float in killotone CO2
        - country: the name of the country in strings
    """
    date: datetime.date
    emission: float
    country: str


@dataclass
class GDP:
    """The dataset from GDP.csv, formetted to show three variables, ranking, country, and GDP. This dataset
    shows the ranking of all country's GDP in 2019
    Attributes
        - ranking: the rank the country's GDP, from highest to lowest
        - country: the name of the country in strings
        - gdp: the GDP calculated in millions of USD in strings"""
    ranking: int
    gdp: str
    country: str


@dataclass
class GlobalCO2:
    """The dataset from climate_change.csv, formatted to show two variables, datetime and CO2 emission.
    This dataset shows the global CO2 in parts per million by volume
    Attributes
        - date: the datetime in datetime.date format
        - emission: the parts"""
    date: datetime.date
    emission: float


# First Step
# This part mutates the data sets into list of dataclasses to work with

country_data = converting_data.convert_country_temperatures()
global_data = converting_data.convert_global_temperatures()
co2_data = converting_data.co2_emission_convert()
gdp_data = converting_data.gdp_convert()
global_co2 = converting_data.global_co2_convert()
co2_data = converting_data.mutate_united_states(co2_data)


# The Given functions below are the ones used in the computational plan, comment it out in order to produce
# what was produced in my computational step.

##########################################################################
# Second Step

# global_map.draw_changing_co2_graph(1990, 2017)
"""This function is to observe the changes in CO2 emission from the starting year given, the to ending year given
This functions serves as a way to see the changes in CO2 emission. The trends observed here will further be analyzed
later"""

# global_map.draw_changing_global_graph_temperature('1990-01-01', '2013-01-01')
"""This function is used to observe the changes in average temperature throughout the years in the range of the
start_date and end_date given above. The trends observed here will further be analyzed later"""

# draw_graph.draw_ranking_comparison(country_data, co2_data, gdp_data, helper_functions.list_of_countries_in_all(co2_data, country_data), 1990, 2017)
"""This graph ranks all the country's respective values and see how they match up to each other. The
trends observed here will further be analyzed later"""
#########################################################
# Third Step

# draw_graph.draw_global_graph_year(global_data)
"""This function analyzes the global change in temperature in relation to date"""

# draw_graph.draw_global_co2_year(global_co2)
"""This function analyzes the global change in CO2 emission in relation to date"""

# draw_graph.draw_global_co2_vs_temperature(global_data, global_co2)
"""This function analyzes the global change in temperature in relation to CO2 emission.
It is connected through date."""

##########################################################
# Fourth Step

# draw_graph.co2_gdp_ranking(co2_data, gdp_data, helper_functions.list_of_countries_co2(), 1983)
"""To modify this function, you can change the list of countries that want to be seen
by changing the third value and the year it starts in by changing the fourth value"""
###########################################################
# Fifth Step

# draw_graph.draw_percentage_of_pollution(gdp_data, co2_data, helper_functions.list_of_countries_co2(co2_data), 1990, 2017, 10)
"""This graph can be modified. 
draw_percentage_of_pollution(gdp_data: list[GDP], co2_data: list[CO2_Emission], 
countries: set, start_year: int, end_year: int, amount_of_countries: int)
It is possible to change the countries in the set, the start year, the end year, and most crucially,
the amount of countries that will be calculated as a top nth country in terms of its GDP."""

###########################################################
# Sixth Step

# draw_graph.draw_country_increase_vs_average(country_data, helper_functions.list_of_countries(country_data, 1990), 1990, 2013)
"""start_year and end_year along with the countries can be modified for this function. Note that the countries
must have data above the start_year therefore when calling list_of_countries(year: int), the year inside
list_of_countries need to be above start_year"""

###########################################################
# Seventh Step

# draw_graph.draw_increase_co2_increase_temperature_country(country_data, co2_data, 'United States', 1990, 2013)
"""draw_increase_co2_increase_temperature_country(country_data: List[CountryTemperature], co2_data: List[CO2Emission],
nation: str, start_year: int, end_year: int), in this case, the options that can be modified is the start_year,
end_year, and the nation. This step specifically focuses on a specific country to analyze."""

###########################################################
# Eighth Step

# draw_graph.draw_increase_co2_increase_temperature(country_data, co2_data, helper_functions.list_of_countries_in_all(co2_data, country_data), 1990, 2013)
"""In this case, the two things that could be modified is the set of countries and the dates."""

###########################################################
# Additional graphs to be played around with for your curiosity

# draw_graph.draw_country_vs_global(global_data, country_data, 'Australia')
"""Insert your desired country into this function to show how global warming is affecting it compared to
global warming in a global scale"""

# draw_graph.draw_country_vs_global_year(global_data, country_data, 'Australia', 1950, 2013)
"""Similar as above but this graph is more streamlined as the temperature is averaged throughout the year,
so it does not fluctuate wildly for summer and winter"""


print('Hello and welcome to this project, in this main.py file there are some functions that can be uncommented'
      'in order to make various graphs, uncomment it in order to produce the graph you want.')
