"""CSC110 Fall 2020 Project: Relationship between Climate Change, Pollution, and Productivity of a Nation

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of graders
grading this project and people who has permission from the creator to use. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Jason Sastra
This python file is used to draw the global maps"""


import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def draw_global_graph_temperature(start_date: str, end_date: str) -> None:
    """draw global graph of the effects of global warming
    start and end date must be in the format YYYY-MM-DD
    Representative Invariant:
        - start_date >= '1750-01-01'
        - end_date <= '2013-01-01'
        - start_date > end_date"""
    data = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
    data = data.drop("AverageTemperatureUncertainty", axis=1)
    clean_data = data.dropna()
    sorted_data = clean_data.groupby(['Country', 'dt']).sum().reset_index().sort_values('dt', ascending=False)
    range_of_date = (sorted_data['dt'] > start_date) & (sorted_data['dt'] <= end_date)
    graphed_data = sorted_data.loc[range_of_date]

    fig = go.Figure(data=go.Choropleth(locations=graphed_data['Country'], locationmode='country names',
                                       z=graphed_data['AverageTemperature'], colorscale='icefire'))
    fig.update_layout(title_text='Global Warming', geo=dict(showcoastlines=False, projection_type='equirectangular'))
    fig.show()


def draw_global_graph_co2(start_year: int, end_year: int) -> None:
    """Draw global graph of the amount of CO2 emission. Start and end date must be only year
    Representative Invariants:
        - start_year >= 1990
        - end_year <= 2017
        - start_date > end_date"""
    data = pd.read_csv("UNdata_Export_20201102_015629836, Carbon dioxide (CO2) Emissions without Land Use, Land-Use Change and Forestry (LULUCF), in kilotonne CO2 equi.csv")
    clean_data = data.dropna()
    sorted_data = clean_data.groupby(['Country or Area', 'Year']).sum().reset_index().sort_values('Year', ascending=False)
    range_of_date = (sorted_data['Year'] > start_year) & (sorted_data['Year'] <= end_year)
    graphed_data = sorted_data.loc[range_of_date]

    fig = go.Figure(data=go.Choropleth(locations=graphed_data['Country or Area'], locationmode='country names',
                    z=graphed_data['Value'], colorscale=['grey', 'black']))
    fig.update_layout(title_text='CO2 Emission', geo=dict(showcoastlines=False, projection_type='equirectangular'))
    fig.show()


def draw_changing_global_graph_temperature(start_date: str, end_date: str) -> None:
    """Draw global graph of the effects of global warming. Including the change throughout the years.
    start and end date must be in the format YYYY-MM-DD
    Representative Invariant:
        - start_date >= '1750-01-01'
        - end_date <= '2013-01-01'
        - start_date > end_date"""
    data = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
    data = data.drop("AverageTemperatureUncertainty", axis=1)
    clean_data = data.dropna()
    sorted_data = clean_data.groupby(['Country', 'dt']).sum().reset_index()
    range_of_date = (sorted_data['dt'] > start_date) & (sorted_data['dt'] <= end_date)
    graphed_data = sorted_data.loc[range_of_date]

    fig = px.choropleth(graphed_data, locations='Country', locationmode='country names',
                        color='AverageTemperature', animation_frame='dt', color_continuous_scale='reds')
    fig.update_layout(title_text='Global Warming: Change in Temperature Throughout the Years',
                      geo=dict(showcoastlines=False))
    fig.show()


def draw_changing_co2_graph(start_year: int, end_year: int) -> None:
    """The the change in temperature for the 43 countries within UNdata through the years given in start_year and
    end_year
    Representative Invariants:
        - start_year >= 1990
        - end_year <= 2017
        - start_date > end_date"""
    data = pd.read_csv("UNdata_Export_20201102_015629836, Carbon dioxide (CO2) Emissions without Land Use, Land-Use Change and Forestry (LULUCF), in kilotonne CO2 equi.csv")
    clean_data = data.dropna()
    sorted_data = clean_data.groupby(['Country or Area', 'Year']).sum().reset_index()
    range_of_date = (sorted_data['Year'] > start_year) & (sorted_data['Year'] <= end_year)
    graphed_data = sorted_data.loc[range_of_date]
    fig = px.choropleth(graphed_data, locations='Country or Area', locationmode='country names',
                        color='Value', animation_frame='Year', color_continuous_scale=['grey', 'black'])
    fig.update_layout(title_text='CO2 Emission: Change in Emission Throughout the Years',
                      geo=dict(showcoastlines=False))
    fig.show()
