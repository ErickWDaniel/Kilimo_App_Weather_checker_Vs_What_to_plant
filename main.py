import requests
import tkinter as tk
from tkinter import ttk, scrolledtext
from api_keys import OPENWEATHERMAP_API_KEY


def get_weather(city, country):
    api_key = OPENWEATHERMAP_API_KEY
    base_url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': f'{city},{country}',
        'appid': api_key,
        'units': 'metric',
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print('Error fetching weather data:', response.status_code)
        return None


def get_weather_forecast(city, country):
    api_key = OPENWEATHERMAP_API_KEY
    base_url = 'https://api.openweathermap.org/data/2.5/forecast'

    params = {
        'q': f'{city},{country}',
        'appid': api_key,
        'units': 'metric',
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print('Error fetching weather forecast data:', response.status_code)
        return None


def suggest_planting(weather_data, soil_type):
    if weather_data:
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']

        suggestions = []

        if temperature >= 25:
            suggestions.append("Consider planting heat-loving crops like tomatoes, peppers, or eggplants.")

        if 'rain' in description.lower():
            suggestions.append("It's a good time for crops that need plenty of water, like lettuce or cucumbers.")

        if 'clear' in description.lower():
            suggestions.append(
                "Clear skies may be suitable for crops that require full sunlight, such as corn or sunflowers.")

        if not suggestions:
            suggestions.append(
                "Weather conditions don't strongly favor specific crops. You can consider a variety of options.")

        # Now, suggest crops based on soil type
        soil_suggestions = []

        if soil_type.lower() == 'clay':
            soil_suggestions.append("Clay soil is suitable for crops like potatoes, beans, and peas.")

        if soil_type.lower() == 'sandy':
            soil_suggestions.append("Sandy soil is good for crops like carrots, radishes, and lettuce.")

        if soil_type.lower() == 'loam':
            soil_suggestions.append("Loam soil is versatile and suitable for a wide range of crops.")

        return suggestions, soil_suggestions
    else:
        return 'Weather data is not available.'


def get_weekly_forecast(forecast_data):
    if forecast_data:
        weekly_forecast = {}

        for item in forecast_data['list']:
            date_str = item['dt_txt'].split()[0]
            date = date_str
            day_of_week = date
            temperature = item['main']['temp']
            description = item['weather'][0]['description']

            if day_of_week not in weekly_forecast:
                weekly_forecast[day_of_week] = {
                    'temperature': [],
                    'description': set()
                }

            weekly_forecast[day_of_week]['temperature'].append(temperature)
            weekly_forecast[day_of_week]['description'].add(description)

        return weekly_forecast


def display_weekly_forecast(weekly_forecast):
    if weekly_forecast:
        forecast_label.config(text='Real Time 7-Day Weather Forecast:')
        forecast_data_label.delete(1.0, tk.END)  # Clear existing text
        forecast_text = ''

        for day, data in weekly_forecast.items():
            min_temp = min(data['temperature'])
            max_temp = max(data['temperature'])
            avg_temp = sum(data['temperature']) / len(data['temperature'])
            descriptions = ', '.join(data['description'])

            forecast_text += f'{day}:\n'
            forecast_text += f'   Min Temp: {min_temp}°C\n'
            forecast_text += f'   Max Temp: {max_temp}°C\n'
            forecast_text += f'   Avg Temp: {avg_temp:.1f}°C\n'
            forecast_text += f'   Description: {descriptions}\n\n'

        forecast_data_label.insert(tk.END, forecast_text)  # Insert new text
    else:
        forecast_label.config(text='Weather forecast data is not available.')


def check_weather_and_soil():
    city = city_entry.get()
    country = country_entry.get()
    soil_type = soil_entry.get()

    if not city or not country or not soil_type:
        result_label.config(text='Please enter both city, country, and soil type.')
        return

    weather_data = get_weather(city, country)
    forecast_data = get_weather_forecast(city, country)
    weekly_forecast = get_weekly_forecast(forecast_data)

    display_weekly_forecast(weekly_forecast)

    planting_suggestion, soil_suggestions = suggest_planting(weather_data, soil_type)

    result_text = '\n'.join(planting_suggestion + soil_suggestions)
    suggestion_label.config(text=result_text)


# Create the main application window
root = tk.Tk()
root.title('Weather/Crop Farmer Adviser By Erick Wilfred 2023')
root.geometry('800x600')  # Set a larger fixed window size

# Create and configure labels and entry fields for city, country, and soil type
city_label = tk.Label(root, text='Enter city:', font=('Helvetica', 14))
city_label.grid(row=0, column=0, padx=10, pady=5)

city_entry = tk.Entry(root, font=('Helvetica', 14))
city_entry.grid(row=0, column=1, padx=10, pady=5)

country_label = tk.Label(root, text='Enter country:', font=('Helvetica', 14))
country_label.grid(row=1, column=0, padx=10, pady=5)

country_entry = tk.Entry(root, font=('Helvetica', 14))
country_entry.grid(row=1, column=1, padx=10, pady=5)

soil_label = tk.Label(root, text='Enter soil type:', font=('Helvetica', 14))
soil_label.grid(row=2, column=0, padx=10, pady=5)

soil_entry = tk.Entry(root, font=('Helvetica', 14))
soil_entry.grid(row=2, column=1, padx=10, pady=5)

# Create the check weather button
check_button = tk.Button(root, text='Check Weather And Suggestion\nCrop For This Weather', command=check_weather_and_soil, font=('Helvetica', 14))
check_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create a label for the 7-day weather forecast
forecast_label = tk.Label(root, text='', font=('Helvetica', 16))
forecast_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Create a scrolled text widget for displaying the 7-day forecast data
forecast_data_label = scrolledtext.ScrolledText(root, font=('Helvetica', 12), wrap=tk.WORD, width=60, height=10)
forecast_data_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Create a label for planting and soil suggestions
suggestion_label = tk.Label(root, text='', font=('Helvetica', 14))
suggestion_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Create a label for displaying the result
result_label = tk.Label(root, text='', font=('Helvetica', 14), justify='left')
result_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Run the main event loop
root.mainloop()
