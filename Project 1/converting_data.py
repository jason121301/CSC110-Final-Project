"""CSC110 Fall 2020 Project: Relationship between Climate Change, Pollution, and Productivity of a Nation

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of graders
grading this project and people who has permission from the creator to use. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Jason Sastra

This group of code will convert all the csv filed into dataclasses that are
easier to process. It also mutates some values in the data sets such that it is more convenient to work with"""

import csv
import datetime
from dataclasses import dataclass
from typing import List, Optional

# This part contains all the Dataclasses


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

# This part converts the csv filed into its respective dataclass


def convert_global_temperatures() -> List[GlobalTemperature]:
    """Open the GlobalTemperatures.csv document and arrange it into the dataclass
    Global Temperature which contains dates and temperatures above the year 1900."""
    data_so_far = []
    with open('GlobalTemperature.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            dates = str.split(row[0], '-')
            if int(dates[0]) >= 1900:
                date = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
                if row[1] == '':
                    temperature = GlobalTemperature(date, None)
                else:
                    temperature = GlobalTemperature(date, float(row[1]))
                data_so_far.append(temperature)
    return data_so_far


def convert_country_temperatures() -> List[CountryTemperature]:
    """
    Open the GlobalLandTemperaturesByCountry file and arrange it into the dataclass CountryTemperature
    """
    data_so_far = []
    with open('GlobalLandTemperaturesByCountry.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            dates = str.split(row[0], '-')
            if int(dates[0]) >= 1900:
                date = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
                if row[1] != '':
                    new_data = CountryTemperature(date, float(row[1]), row[3])
                    data_so_far.append(new_data)
                else:
                    new_data = CountryTemperature(date, None, row[3])
                    data_so_far.append(new_data)
    return data_so_far


def co2_emission_convert() -> List[CO2Emission]:
    """Convert the data from UNdata_Export into the dataclass format of CO2Emission"""
    data_so_far = []
    with open('UNdata_Export_20201102_015629836, '
              'Carbon dioxide (CO2) Emissions without Land Use, Land-Use Change and Forestry (LULUCF), '
              'in kilotonne CO2 equi.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data = CO2Emission(datetime.date(int(row[1]), 1, 1),
                               float(row[2]), row[0])
            data_so_far.append(data)
    return data_so_far


def gdp_convert() -> List[GDP]:
    """Convert the data from GDP.csv into the dataclass format of GDP"""
    data_so_far = []
    with open('GDP.csv') as file:
        reader = csv.reader(file)
        next(reader)
        next(reader)
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            if row[1] != '':
                data = GDP(int(row[1]), row[4], row[3])
                data_so_far.append(data)
            else:
                return data_so_far


def global_co2_convert() -> List[GlobalCO2]:
    """Convert the data from climate_change.csv"""
    data_so_far = []
    with open('climate_change.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data = GlobalCO2(datetime.date(int(row[0]), int(row[1]), 1), float(row[3]))
            data_so_far.append(data)
    return data_so_far


def mutate_united_states(co2: List[CO2Emission]) -> List[CO2Emission]:
    """Mutate the dataset within co2_data so that the country written there for specifically
    United States matches with the one in country_data and gdp,
    which is written as United States"""

    for row in co2:
        if row.country == 'United States of America':
            row.country = 'United States'
    return co2
