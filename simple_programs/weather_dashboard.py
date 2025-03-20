# 1. Import necessary libraries (requests, json, datetime)
import sys
import requests
import json
from datetime import datetime


# 2. Define function to get weather data from API
#    - Take city name as input
#    - Construct API request URL with city and API key
#    - Send GET request to API
#    - Parse JSON response
#    - Return weather data


def get_weather(city, api_key):
    try:
        print(f"We are now getting data for {city}")
        lat_lon_url = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
        )
        lat_lon = lat_lon_url.json()

        if not lat_lon:
            sys.exit(
                f"City '{city}' not found. Please check spelling or try another city."
            )

        city = lat_lon[0]
        lat = city["lat"]
        lon = city["lon"]

        weather_url = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        weather_data = weather_url.json()

    except Exception as e:
        print(e)
        sys.exit("An exception has occured.")
    else:
        return weather_data


# 3. Define function to display weather information nicely
#    - Take weather data as input
#    - Format and print current conditions, temperature, etc.


def format(weather_data):

    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    description = weather_data["weather"][0]["description"].capitalize()

    return f"{description}, the temperature is {temperature:.2f}°C and feels like {feels_like:.2f}°C.\nThe humidity is {humidity}%\nThe wind speed is {wind_speed} m/s."


# 4. Main program:
#    - Ask user for city name
#    - Get weather data by calling the get_weather_data function
#    - Display data by calling display_weather function
#    - Ask if user wants to check another city


def main():
    city = input("Input a city: ")
    api_key = input("Input your api key: ")
    print(format(get_weather(city, api_key)))


if __name__ == "__main__":
    main()

#    Libraries:

# requests: For making HTTP requests to the weather API
# json: For parsing API responses
# datetime: For formatting date/time information

# Implementation Notes:

# You'll need to sign up for a free API key from a weather service like OpenWeatherMap
# Focus on error handling (e.g., invalid city names, API failures)
