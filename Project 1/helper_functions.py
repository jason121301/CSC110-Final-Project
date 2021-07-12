"""CSC110 Fall 2020 Project: Relationship between Climate Change, Pollution, and Productivity of a Nation

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 Jason Sastra

This python files contains all the helper functions that are used in this project.
Most of these helper functions are used to find averages, sums, and many other"""


from dataclasses import dataclass
import datetime
from typing import List, Optional, Tuple
import statistics
import operator


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


def list_of_countries(country_data: List[CountryTemperature], year: int) -> set:
    """Gives the list of countries that are available within the dataset of country datas that has temperature data for
    years above the given year"""
    return {row.country for row in country_data if int(row.date.strftime("%Y")) > year and row.temperature is not None}


def list_of_countries_in_all(co2_data: List[CO2Emission], country_data: List[CountryTemperature]) -> set:
    """Gives the list of countries that are available within the dataset of both co2_emission and country datas"""
    country1 = {row.country for row in country_data}
    country2 = {row.country for row in co2_data}
    countries_so_far = set()
    for row in country1:
        for co2 in country2:
            if row == co2:
                countries_so_far.add(row)
    return countries_so_far


def list_of_countries_co2(co2_data: List[CO2Emission]) -> set:
    """gives the list of countries that are available within the dataset of co2_data"""
    return {row.country for row in co2_data}


def create_global_yearly_data(global_data: List[GlobalTemperature],
                              start_year: int, end_year: int) -> Tuple[List[int], List[float]]:
    """Create a global temperature data based on yearly intervals in which the temperature
     is averaged over the year, above the years given in start_year and below the year in end_year
     Representative Invariants:
        - year <= end_year <= 2013
        - year >= 1900 >= end_year"""
    years = []
    temperature_so_far = []
    new_data = [row for row in global_data if end_year >= int(row.date.strftime("%Y")) >= start_year]
    for i in range(int(new_data[1].date.strftime("%Y")), int(new_data[-2].date.strftime("%Y"))):
        sum_temperature = []
        for row in new_data:
            if int(row.date.strftime("%Y")) < i:
                pass
            elif int(row.date.strftime("%Y")) == i:
                sum_temperature.append(row.temperature)
            elif int(row.date.strftime("%Y")) > i:
                years.append(i)
                temperature_so_far.append(statistics.mean(sum_temperature))
                break
    return (years, temperature_so_far)


def create_country_yearly_data(country_data: List[CountryTemperature],
                               nation: str, year: int, end_year: int) -> List[CountryTemperature]:
    """Create the yearly average temperature for the given country, for years above the year given
    Representative Invariants:
        - year <= end_year <= 2013
        - year >= 1900 >= end_year"""
    country_only_data = [row for row in country_data if row.country == nation]
    data_so_far = []
    for i in range(year, end_year):
        sum_temperature = []
        for row in country_only_data:
            if int(row.date.strftime("%Y")) < i:
                pass
            elif int(row.date.strftime("%Y")) == i:
                sum_temperature.append(row.temperature)
            elif int(row.date.strftime("%Y")) >= i:
                if isinstance(sum_temperature[0], float) is True:
                    data_so_far.append(CountryTemperature(datetime.date(i, 1, 1),
                                                          statistics.mean(sum_temperature), nation))
                break
    return data_so_far


def yearly_increase_temperature(country_data: List[CountryTemperature],
                                nation: str, start_year: int, end_year: int) -> List[float]:
    """Finds the yearly increase in temperature for the country given, between years start_year and end_year
    Representative Invariants:
        - nation in list_of_countries(country_data)
        - start_year >= 1750
        - end_year <= 2013"""
    new_data = create_country_yearly_data(country_data, nation, start_year, end_year)
    temperature_increase = []
    previous_year = None
    for row in new_data:
        if previous_year is None:
            previous_year = row.temperature
        if row.temperature is not None:
            new_increase = (row.temperature - previous_year)
            temperature_increase.append(new_increase)
            previous_year = row.temperature
    return temperature_increase


def average_yearly_increase_temperature(country_data: List[CountryTemperature],
                                        nation: str, year: int, end_year: int) -> float:
    """Returns the average yearly increase in temperature, for years above the year given and below the end_year
    Representative Invariants:
        - year <= end_year <= 2013
        - year >= 1900 >= end_year"""
    data = create_country_yearly_data(country_data, nation, year, end_year)
    new_data = [row for row in data if int(row.date.strftime("%Y")) >= year]
    sum_temperature = []
    previous_year = None
    for row in new_data:
        if previous_year is None:
            previous_year = row.temperature
        if row.temperature is not None:
            new_increase = (row.temperature - previous_year)
            sum_temperature.append(new_increase)
            previous_year = row.temperature
    if sum_temperature is not []:
        average = statistics.mean(sum_temperature)
        return average


def average_country_temperature(country_data: List[CountryTemperature], nation: str, year: int) -> float:
    """Returns the average temperature of the country, for years above year given"""
    data = [row for row in country_data if row.country in nation]
    new_data = [row for row in data if int(row.date.strftime("%Y")) >= year]
    sum_temperature = []
    for row in new_data:
        if row.temperature is not None:
            sum_temperature.append(row.temperature)
    if sum_temperature != []:
        average = statistics.mean(sum_temperature)
        return average


def temperature_increase_ranking(country_data: List[CountryTemperature],
                                 nations: set, year: int, end_year: int) -> list:
    """Rank the average yearly increase in temperature for all the countries in nations, for the years
    above the year given
    Representative Invariants:
        - year <= end_year <= 2013
        - year >= 1900 >= end_year"""
    ranking = []
    for nation in nations:
        average_increase = average_yearly_increase_temperature(country_data, nation, year, end_year)
        nation_ranking = [average_increase, nation]
        ranking.append(nation_ranking)
    ranking.sort(reverse=True)
    for i in range(1, len(ranking) + 1):
        ranking[i - 1][0] = i

    return ranking


def yearly_increase_co2(co2_data: List[CO2Emission], nation: str, start_year: int, end_year: int) -> List[float]:
    """Returns a list of the yearly increase in CO2 for the given country from start_year to end_year
    Representative Invariants:
        - year <= end_year <= 2013
        - year >= 1900 >= end_year"""
    country_only_co2 = [row for row in co2_data if row.country == nation
                        and start_year <= int(row.date.strftime("%Y")) <= end_year]
    co2_change = []
    sorted_data = sorted(country_only_co2, key=operator.attrgetter('date'))
    previous_year = None
    for row in sorted_data:
        if previous_year is None:
            previous_year = row.emission
        else:
            new_increase = row.emission - previous_year
            co2_change.append(new_increase)
            previous_year = row.emission
    return co2_change


def average_yearly_increase_co2(co2_data: List[CO2Emission], nation: str, year: int) -> float:
    """Find the average yearly increase in co2 for the country given in years above the year given
    Representative Invariants:
        - nation in list_of_countries_co2(co2_data)"""
    new_data = [row for row in co2_data if row.country == nation]
    data = [row for row in new_data if int(row.date.strftime("%Y")) > year]
    sorted_data = sorted(data, key=operator.attrgetter('date'))
    sum_temperature = []
    previous_year = None
    for row in sorted_data:
        if previous_year is None:
            previous_year = row.emission
        else:
            new_increase = row.emission - previous_year
            sum_temperature.append(new_increase)
            previous_year = row.emission
    average = statistics.mean(sum_temperature)
    return average


def co2_increase_ranking(co2_data: List[CO2Emission], nations: set, year: int) -> list:
    """Ranks the average yearly increase in co2 for the countries given in years above the year given
    Representative Invariants:
        - all([nation in list_of_countries_co2(co2_data) for nation in nations])
        - 2017 >= year >= 1950"""
    ranking = []
    for nation in nations:
        average_increase = average_yearly_increase_co2(co2_data, nation, year)
        nation_ranking = [average_increase, nation]
        ranking.append(nation_ranking)
    ranking.sort(reverse=True)
    for i in range(1, len(ranking) + 1):
        ranking[i - 1][0] = i

    return ranking


def co2_ranking(co2_data: List[CO2Emission], nations: set, year: int) -> dict:
    """Returns a mapping of the total amount of CO2 emission produced above a certain year for the given countries
    Representative Invariants:
        - all([nation in list_of_countries_co2(co2_data) for nation in nations])
        - 2017 >= year >= 1950"""
    country_to_co2 = {}
    new_data = [row for row in co2_data if int(row.date.strftime("%Y")) >= year and row.country in nations]
    for row in new_data:
        if row.country not in country_to_co2:
            country_to_co2[row.country] = [row.emission]
        else:
            country_to_co2[row.country].append(row.emission)
    for country in country_to_co2:
        country_to_co2[country] = sum(country_to_co2[country])
    return country_to_co2


def simple_linear_regression(x: List[float or int], y: List[float or int]) -> Tuple[int, int]:
    """Perform a linear regression on the given datasets
    Representative Invariants:
        len(x) = len(y)
    """

    b = sum([(x[n] - statistics.mean(x)) * (y[n] - statistics.mean(y)) for n in range(0, len(x))]) / \
        sum([(n - statistics.mean(x)) ** 2 for n in x])
    a = statistics.mean(y) - b * statistics.mean(x)
    return (a, b)


def calculate_r_squared(x_list: list, y_list: list, a: float, b: float) -> float:
    """Return the R squared value when the given points are modelled as the line y = a + bx.
    """
    y_average = statistics.mean(y_list)
    sstot = sum([(y - y_average) ** 2 for y in y_list])
    ssres = sum([(y_list[n] - (a + b * x_list[n])) ** 2 for n in range(0, len(y_list))])
    r_squared = 1 - (ssres / sstot)
    return r_squared


def linear_regression_into_graph_points(x_data: List[float or int], y_data: List[float or int],
                                        x_start: int, x_end: int) -> List[list]:
    """Use the linear regression to create graph points for plotly"""
    equation = simple_linear_regression(x_data, y_data)
    y_so_far = []
    x_so_far = []
    for x in range(x_start, x_end):
        y = equation[0] + equation[1] * x
        y_so_far.append(y)
        x_so_far.append(x)
    return [x_so_far, y_so_far]


def ranked_by_gdp(gdp_data: List[GDP], countries: set) -> List[GDP]:
    """Ranks the GDP of the countries given in descending order, from highest GDP to lowest GDP,
    for its GDP in 2019"""
    new_data = [row for row in gdp_data if row.country in countries]
    return new_data
