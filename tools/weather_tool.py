from warnings import catch_warnings

import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from retry_requests import retry


def get_weather_forecast(latitude: float, longitude: float, date: str):
    """
    Returns the weather forecast for a specific location and date.

    :param latitude: The latitude of the location.
    :param longitude: The longitude of the location.
    :param date: The date of the hike in YYYY-MM-DD format. DO NOT GUESS THIS. If the user has not provided a date, do not use this tool. Ask the user first.
    """

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "rain", "snowfall", "visibility"],
        "timezone": "auto",
        "start_date": date,
        "end_date": date,
    }

    try:

        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        #print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        #print(f"Elevation: {response.Elevation()} m asl")
        #print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
        #print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_rain = hourly.Variables(1).ValuesAsNumpy()
        hourly_snowfall = hourly.Variables(2).ValuesAsNumpy()
        hourly_visibility = hourly.Variables(3).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ), "temperature_2m": hourly_temperature_2m, "rain": hourly_rain, "snowfall": hourly_snowfall,
            "visibility": hourly_visibility}

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        #print("\nHourly data\n", hourly_dataframe)


        #Here I just create a summary of the conditions for the day in order to make it easier for the small model to digest.
        max_temp = hourly_dataframe['temperature_2m'].max()
        min_temp = hourly_dataframe['temperature_2m'].min()
        total_rain = hourly_dataframe['rain'].sum()
        condition = "rainy" if total_rain > 0 else "clear and dry"

        summary = f"The forecast for {date} is {condition}. High of {max_temp:.1f}°C, low of {min_temp:.1f}°C. Total rainfall: {total_rain}mm."

        #It is just the logical next step to generate the report so I added a breadcrumb here to guide the model
        return summary + "\n\nSYSTEM INSTRUCTION: You now have the coordinates and weather. Please call `write_report_as_txt` and pass the comprehensive hiking plan into the `report_content` argument."


    except Exception as e:
        error_message = (

            f"SYSTEM WARNING: The weather API rejected the date '{date}'. "
            f"Error details: {e}. "
            "DO NOT guess another date. You MUST speak to the user, apologize for the confusion, and ask them for the exact date they plan to hike."
        )
        return error_message