"""CSC110 Fall 2020 Project: Relationship between Climate Change, Pollution, and Productivity of a Nation

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of graders
grading this project and people who has permission from the creator to use. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Jason Sastra

This Python file is used whenever a graph wants to be charted in plotly. It is the collection of all
the functions used to generate plotly graphs"""

import datetime
from dataclasses import dataclass
from typing import Optional, List
import plotly.graph_objects as go
import statistics
import helper_functions
import plotly.express as px


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


def draw_ranking_comparison(country_data: List[CountryTemperature], co2_data: List[CO2Emission],
                            gdp_data: List[GDP], nations: set, year: int, end_year: int) -> None:
    """Draws a dot plot comparing the rankings of a countries gdp, average increase in CO2 emission
    and average increase in temperature"""
    temperature_ranking = helper_functions.temperature_increase_ranking(country_data, nations, year, end_year)
    co2_rank = helper_functions.co2_increase_ranking(co2_data, nations, year)
    gdp_ranking = [row for row in gdp_data if row.country in nations]
    for i in range(1, len(gdp_ranking) + 1):
        gdp_ranking[i - 1].ranking = i
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[temperature[0] for temperature in temperature_ranking],
        y=[temperature[1] for temperature in temperature_ranking],
        marker=dict(color="crimson", size=15),
        mode="markers",
        name="Ranking of the average increase in temperature",
    ))

    fig.add_trace(go.Scatter(x=[row.ranking for row in gdp_ranking],
                             y=[row.country for row in gdp_ranking],
                             marker=dict(color="gold", size=15),
                             mode="markers",
                             name="GDP ranking for the year of 2019"))

    fig.add_trace(go.Scatter(
        x=[co2[0] for co2 in co2_rank],
        y=[co2[1] for co2 in co2_rank],
        marker=dict(color="black", size=15),
        mode="markers",
        name="Ranking of the average increase in CO2 emission",
    ))

    fig.update_layout(title="Difference in Ranking for GDP, temperature, and CO2 emission from the year " + str(year),
                      xaxis_title="Ranking",
                      yaxis_title="Country")

    fig.show()


def co2_gdp_ranking(co2_data: List[CO2Emission], gdp_data: List[GDP], nations: set, start_year: int) -> None:
    """Draws a dot plot comparing the rankings of a countries gdp, average increase in CO2 emission
    and average increase in temperature"""
    co2_increase = helper_functions.co2_increase_ranking(co2_data, nations, start_year)
    gdp_ranking = [row for row in gdp_data if row.country in nations]
    co2_overall = helper_functions.co2_ranking(co2_data, nations, start_year)
    sorted_co2_overall = sorted(co2_overall.items(), key=lambda x: x[1], reverse=True)

    for i in range(1, len(gdp_ranking) + 1):
        gdp_ranking[i - 1].ranking = i
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=[row.ranking for row in gdp_ranking],
                             y=[row.country for row in gdp_ranking],
                             marker=dict(color="gold", size=17),
                             mode="markers",
                             name="GDP ranking for the year of 2019"))

    fig.add_trace(go.Scatter(
        x=[co2[0] for co2 in co2_increase],
        y=[co2[1] for co2 in co2_increase],
        marker=dict(color="black", size=15),
        mode="markers",
        name="Ranking of the average increase in CO2 emission",
    ))

    fig.add_trace(go.Scatter(x=range(1, len(sorted_co2_overall) - 1),
                             y=[row[0] for row in sorted_co2_overall],
                             marker=dict(color="red", size=13),
                             mode="markers",
                             name="Total co2 emission "))

    fig.update_layout(title="Difference in Ranking for GDP(2019), overall CO2 emission,"
                            " and average increase in CO2 emission from the year " + str(start_year),
                      xaxis_title="Ranking",
                      yaxis_title="Country")

    fig.show()


def draw_global_graph(global_data: List[GlobalTemperature]) -> None:
    """Draw the global graph as a scatter plot with plotly and produce a linear regression of it"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[data.date for data in global_data],
                             y=[data.temperature for data in global_data], mode='lines+markers'))
    fig.update_xaxes(title_text="Date (M-D-Y)")
    fig.update_yaxes(title_text="Temperature (C)")
    fig.show()


def draw_global_graph_year(global_data: List[GlobalTemperature]) -> None:
    """Draw the global graph as a scatter plot but its y value would be averaged over the years, and the x value
    would be based on yearly intervals"""
    years = []
    temperature_so_far = []
    for i in range(int(global_data[1].date.strftime("%Y")), int(global_data[-1].date.strftime("%Y"))):
        sum_temperature = []
        for row in global_data:
            if int(row.date.strftime("%Y")) < i:
                pass
            elif int(row.date.strftime("%Y")) == i:
                sum_temperature.append(row.temperature)
            elif int(row.date.strftime("%Y")) > i:
                years.append(i)
                temperature_so_far.append(statistics.mean(sum_temperature))
                break
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[datetime.date(year, 1, 1) for year in years],
                             y=temperature_so_far, mode='lines+markers'))
    fig.update_xaxes(title_text="Date (Y)")
    fig.update_yaxes(title_text="Temperature (C)")
    fig.show()


def draw_global_co2_year(global_co2: List[GlobalCO2]) -> None:
    """Draw the global graph as a function of the increase in co2"""
    emission_so_far = []
    years = []
    for i in range(int(global_co2[1].date.strftime("%Y")), int(global_co2[-1].date.strftime("%Y"))):
        sum_emission = []
        for row in global_co2:
            if int(row.date.strftime("%Y")) < i:
                pass
            elif int(row.date.strftime("%Y")) == i:
                sum_emission.append(row.emission)
            elif int(row.date.strftime("%Y")) > i:
                years.append(i)
                emission_so_far.append(statistics.mean(sum_emission))
                break
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=emission_so_far,
                             y=[datetime.date(year, 1, 1) for year in years],
                             mode='lines+markers'))
    fig.update_xaxes(title_text="Date (Y)")
    fig.update_yaxes(title_text="CO2 in the atmosphere (ppmv)")
    fig.show()


def draw_global_co2_vs_temperature(global_data: List[GlobalTemperature], global_co2: List[GlobalCO2]) -> None:
    """Draw the global graph as a temperature versus global CO2 emission"""
    temperature = helper_functions.create_global_yearly_data(global_data, int(global_co2[0].date.strftime('%Y')),
                                                             int(global_co2[-1].date.strftime('%Y')))
    emission_so_far = []
    years = []
    for i in range(int(global_co2[1].date.strftime("%Y")), int(global_co2[-1].date.strftime("%Y"))):
        sum_emission = []
        for row in global_co2:
            if int(row.date.strftime("%Y")) < i:
                pass
            elif int(row.date.strftime("%Y")) == i:
                sum_emission.append(row.emission)
            elif int(row.date.strftime("%Y")) > i:
                years.append(i)
                emission_so_far.append(statistics.mean(sum_emission))
                break
    equation = helper_functions.simple_linear_regression(emission_so_far, temperature[1])
    linear_regression = helper_functions.\
        linear_regression_into_graph_points(emission_so_far, temperature[1],
                                            round(emission_so_far[0]), round(emission_so_far[-1]))
    r_squared = helper_functions.calculate_r_squared(emission_so_far,
                                                     temperature[1], equation[0], equation[1])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=emission_so_far,
                             y=temperature[1],
                             mode='lines+markers',
                             name='Raw Values'))
    fig.add_trace(go.Scatter(x=linear_regression[0],
                             y=linear_regression[1],
                             mode='lines+markers',
                             name='Linear Regression')
                  )
    fig.update_xaxes(title_text="CO2 in the atmosphere (ppmv)")
    fig.update_yaxes(title_text="Temperature (C)")
    fig.update_layout(title={'text': 'The linear regression is '
                                     + 'y = ' + str(equation[0]) + ' + x' + str(equation[1])
                                     + 'It also has an r^2 = ' + str(r_squared)})
    fig.show()


def draw_country_graph(country_data: list, nation: str) -> None:
    """Draw the graph of the country's temperature as a scatter plot with plotly
    and produce a linear regression of it"""
    country_only_data = [row for row in country_data if row.country == nation]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[row.date for row in country_only_data],
                             y=[row.temperature for row in country_only_data],
                             mode='lines+markers'))
    fig.update_xaxes(title_text="Date (Y)")
    fig.update_yaxes(title_text="Temperature (C)")
    fig.show()


def draw_country_graph_year(country_data: list, nation: str) -> None:
    """Draw the global graph as a scatter plot but its y value would be averaged over the years, and the x value
    would be based on yearly intervals"""
    country_only_data = [row for row in country_data if row.country == nation]
    years = []
    temperature_so_far = []
    for i in range(int(country_only_data[1].date.strftime("%Y")), int(country_only_data[-1].date.strftime("%Y"))):
        sum_temperature = []
        for row in country_only_data:
            if int(row.date.strftime("%Y")) < i:
                pass
            elif int(row.date.strftime("%Y")) == i:
                sum_temperature.append(row.temperature)
            elif int(row.date.strftime("%Y")) > i:
                years.append(i)
                temperature_so_far.append(statistics.mean(sum_temperature))
                break
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[datetime.date(year, 1, 1) for year in years],
                             y=temperature_so_far, mode='lines+markers'))
    fig.update_layout(title={'text': nation})
    fig.update_xaxes(title_text="Date (Y)")
    fig.update_yaxes(title_text="Temperature (C)")
    fig.show()


def draw_co2_emission(co2_data: List[CO2Emission], nation: str) -> None:
    """Draw the graph for CO2 emission in each country based on the year and produce a linear regression of it"""
    country_only_data = [row for row in co2_data if row.country == nation]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[row.date for row in country_only_data],
                             y=[row.emission for row in country_only_data],
                             mode='lines+markers', name='nation'))
    fig.update_layout(title={'text': nation})
    fig.update_xaxes(title_text="Date (Y)")
    fig.update_yaxes(title_text="Emission")
    fig.show()


def draw_country_vs_global(global_data: list, country_data: list, nation: str) -> None:
    """Draw the graph of the country versus the global change in temperature"""
    fig = go.Figure()
    country_only_data = [row for row in country_data if row.country == nation]
    fig.add_trace(go.Scatter(x=[data.date for data in global_data],
                             y=[data.temperature for data in global_data], mode='lines+markers', name='Global'))
    fig.add_trace(go.Scatter(x=[row.date for row in country_only_data],
                             y=[row.temperature for row in country_only_data],
                             mode='lines+markers', name=nation))
    fig.update_xaxes(title_text="Date (Y)")
    fig.update_yaxes(title_text="Temperature (C)")
    fig.show()


def draw_country_vs_global_year(global_data: List[GlobalTemperature],
                                country_data: list, nation: str, start_year: int, end_year: int) -> None:
    """Draw the graph of the country versus the global change in temperature within the time range
    of start_year and end_year"""
    country_only_data = [row for row in country_data if row.country == nation]
    years = []
    temperature_so_far = []
    for i in range(start_year, end_year):
        sum_temperature = []
        for row in country_only_data:
            if int(row.date.strftime("%Y")) < i:
                pass
            elif int(row.date.strftime("%Y")) == i:
                sum_temperature.append(row.temperature)
            elif int(row.date.strftime("%Y")) > i:
                years.append(i)
                temperature_so_far.append(statistics.mean(sum_temperature))
                break
    (global_years, global_temp) = helper_functions.create_global_yearly_data(global_data, start_year, end_year)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[datetime.date(year, 1, 1) for year in global_years],
                             y=global_temp, mode='lines+markers', name='Global'))
    fig.add_trace(go.Scatter(x=[datetime.date(year, 1, 1) for year in years],
                             y=temperature_so_far, mode='lines+markers', name=nation))
    fig.update_layout(title={'text': nation})
    fig.update_xaxes(title_text="Date (Y)")
    fig.update_yaxes(title_text="Temperature (C)")
    fig.show()


def draw_country_increase_vs_average(country_data: List[CountryTemperature], nations: set, year: int, end_year: int):
    """Draw the graph for the average yearly increase in temperature in comparison with the average
    temperature of the country.
    Representative Invariants
        - year <= end_year <= 2013
        - year >= 1900 >= end_year"""
    average_so_far = []
    increase_so_far = []
    for nation in nations:
        average = helper_functions.average_country_temperature(country_data, nation, year)
        increase = helper_functions.average_yearly_increase_temperature(country_data, nation, year, end_year)
        average_so_far.append(average)
        increase_so_far.append(increase)
    equation = helper_functions.simple_linear_regression(average_so_far, increase_so_far)
    r_squared = helper_functions.calculate_r_squared(average_so_far, increase_so_far, equation[0], equation[1])
    linear_regression = helper_functions.linear_regression_into_graph_points(average_so_far, increase_so_far, -20, 31)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=average_so_far,
                             y=increase_so_far, mode='markers', marker=dict(color="blue", size=13)))
    fig.add_trace(go.Scatter(x=linear_regression[0],
                             y=linear_regression[1], mode='lines+markers', name='linear regression'))
    fig.update_layout(title={'text': 'Average increase in temperature as a function of average temperature. <br>' +
                                     'The linear regression has an equation y = ' + str(equation[0]) + ' + x'
                                     + str(equation[1]) + '. It also has an r^2 = ' + str(r_squared)})
    fig.update_xaxes(title_text="Average Temperature from the year " + str(year) + ' to the year '
                                                                                 + str(end_year) + " (C)")
    fig.update_yaxes(title_text="Average Increase in Temperature from the year " + str(year) + ' to the year '
                                + str(end_year) + " (C)")
    fig.show()


def draw_percentage_of_pollution(gdp_data: List[GDP], co2_data: List[CO2Emission],
                                 countries: set, start_year: int, end_year: int, amount_of_country: int):
    """Percentage of pollution caused by the top 10 countries in countries compared to the rest of it"""
    new_data = helper_functions.ranked_by_gdp(gdp_data, countries)
    top_country = set()
    other_country = set()
    for i in range(0, amount_of_country):
        top_country.add(new_data[i].country)
    for i in range(amount_of_country, len(new_data)):
        other_country.add(new_data[i].country)
    top_10_co2 = sum([row.emission for row in co2_data if row.country in top_country
                      and end_year >= int(row.date.strftime("%Y")) >= start_year])
    other_country = sum([row.emission for row in co2_data if row.country in other_country
                         and end_year >= int(row.date.strftime("%Y")) >= start_year])
    labels = ['Top ' + str(amount_of_country) +
              ' Countries in GDP ranking from the set of countries', 'Other Countries']
    values = [top_10_co2, other_country]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                                 title='Percentage of total CO2 emission from year ' + str(start_year) + ' to '
                                       + str(end_year) + ' from a total of ' + str(len(countries)) + ' countries')])
    fig.update_layout(font=dict(size=18))
    fig.show()


def draw_increase_co2_increase_temperature_country(country_data: List[CountryTemperature], co2_data: List[CO2Emission],
                                                   nation: str, start_year: int, end_year: int) -> None:
    """Draw the a graph the compares the change in temperature versus the change in CO2 emission.
    Representative Invariants:
        - country in helper_functions.list_of_countries_co2(co2_data, country_data)
        - start_year <= end_year <= 2013
        - start_year >= 1990"""
    country_only_data = helper_functions.yearly_increase_temperature(country_data, nation, start_year, end_year)
    co2_country = helper_functions.yearly_increase_co2(co2_data, nation, start_year, end_year)
    equation = helper_functions.simple_linear_regression(co2_country, country_only_data)
    r_squared = helper_functions.calculate_r_squared(co2_country, country_only_data, equation[0], equation[1])
    linear_regression = \
        helper_functions.linear_regression_into_graph_points(co2_country, country_only_data,
                                                             round(min(co2_country)), round(max(co2_country)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=co2_country, y=country_only_data, mode='markers',
                             name='Temperature Increase vs CO2 Increase'))
    fig.add_trace(go.Scatter(x=linear_regression[0], y=linear_regression[1], mode='lines', name='Linear Regression'))
    fig.update_layout(title={'text': 'Increase in temperature as a function of increase in CO2 for the country '
                             + nation + ' in the years ' + str(start_year) + ' to ' + str(end_year)
                             + '<br> The linear regression has an equation y = ' + str(equation[0]) + ' + x'
                                     + str(equation[1]) + '. It also has an r^2 = ' + str(r_squared)})
    fig.show()


def draw_increase_co2_increase_temperature(country_data: List[CountryTemperature], co2_data: List[CO2Emission],
                                           countries: set, start_year: int, end_year: int) -> None:
    """Draw the a graph the compares the change in temperature versus the change in CO2 emission.
    Representative Invariants:
        - country in helper_functions.list_of_countries_co2(co2_data, country_data)
        - start_year <= end_year <= 2013
        - start_year >= 1990"""
    all_country = []
    all_co2 = []
    x_data = []
    y_data = []
    for country in countries:
        country_only_data = helper_functions.yearly_increase_temperature(country_data, country, start_year, end_year)
        co2_country = helper_functions.yearly_increase_co2(co2_data, country, start_year, end_year)
        all_country.append(country_only_data)
        all_co2.append(co2_country)
    for i in range(0, len(all_country[0])):
        country_mean = sum([row[i] for row in all_country])
        co2_mean = sum([row[i] for row in all_co2])
        x_data.append(co2_mean)
        y_data.append(country_mean)

    equation = helper_functions.simple_linear_regression(x_data, y_data)
    r_squared = helper_functions.calculate_r_squared(x_data, y_data, equation[0], equation[1])
    linear_regression = \
        helper_functions.linear_regression_into_graph_points(x_data, y_data,
                                                             round(min(x_data)), round(max(x_data)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers',
                             name='Temperature Increase vs CO2 Increase'))
    fig.add_trace(go.Scatter(x=linear_regression[0], y=linear_regression[1], mode='lines', name='Linear Regression'))
    fig.update_layout(title={'text': 'Increase in temperature as a function of increase in CO2' +
                                     ' in the years ' + str(start_year) + ' to ' + str(end_year)
                                     + '<br> The linear regression has an equation y = ' + str(equation[0]) + ' + x'
                                     + str(equation[1]) + '. It also has an r^2 = ' + str(r_squared)})
    fig.show()
