import requests
from tkinter import *
from tkinter import messagebox
import geocoder

# API configuration
API_KEY = 'bfdafbd759962ccd10f50c0a2b1e8a75'  # Replace with your OpenWeatherMap API key
BASE_URL_CURRENT = 'https://api.openweathermap.org/data/2.5/weather'
BASE_URL_FORECAST = 'https://api.openweathermap.org/data/2.5/forecast'

# Function to fetch weather data
def get_weather(city, unit):
    try:
        params = {'q': city, 'appid': API_KEY, 'units': unit}
        response = requests.get(BASE_URL_CURRENT, params=params)
        response.raise_for_status()
        data = response.json()

        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        weather = data['weather'][0]['description'].capitalize()
        wind_speed = data['wind']['speed']

        forecast = get_forecast(city, unit)

        result = f"City: {city_name}, {country}\nTemperature: {temp}° {'C' if unit == 'metric' else 'F'}\nHumidity: {humidity}%\nWeather: {weather}\nWind Speed: {wind_speed} m/s\n\nForecast (Next 3 Days):\n{forecast}"

        weather_label.config(text=result)

    except requests.exceptions.HTTPError:
        messagebox.showerror('Error', 'Invalid city name or server issue. Please try again.')
    except requests.exceptions.RequestException:
        messagebox.showerror('Error', 'Network error. Check your connection.')


# Function to fetch 3-day forecast
def get_forecast(city, unit):
    try:
        params = {'q': city, 'appid': API_KEY, 'units': unit}
        response = requests.get(BASE_URL_FORECAST, params=params)
        response.raise_for_status()
        data = response.json()

        forecast_text = ''
        dates_checked = set()

        for entry in data['list']:
            date = entry['dt_txt'].split(' ')[0]

            if date not in dates_checked and len(dates_checked) < 3:  # Only 3 unique days
                dates_checked.add(date)
                temp = entry['main']['temp']
                condition = entry['weather'][0]['description'].capitalize()
                forecast_text += f"{date}: {temp}° {'C' if unit == 'metric' else 'F'}, {condition}\n"

        return forecast_text
    except:
        return 'Unable to fetch forecast.'


# Function to get location using GPS (via IP-based geolocation)
def get_location():
    try:
        location = geocoder.ip('me')
        return location.city
    except:
        return ''


# Tkinter setup
app = Tk()
app.title('Advanced Weather App')
app.geometry('500x500')
app.configure(bg='#e0f7fa')  # Light blue background

header = Label(app, text='🌤️ Weather Forecast 🌦️', font=('Helvetica', 20, 'bold'), bg='#e0f7fa', fg='#01579b')
header.pack(pady=10)

frame = Frame(app, bg='#b2ebf2', padx=10, pady=10, relief=RIDGE, bd=2)
frame.pack(pady=10)

city_label = Label(frame, text='Enter City Name or Use GPS:', font=('Arial', 14), bg='#b2ebf2')
city_label.grid(row=0, column=0, columnspan=2, pady=5)

city_entry = Entry(frame, font=('Arial', 14), width=25)
city_entry.grid(row=1, column=0, columnspan=2, pady=5)

unit_var = StringVar(value='metric')
Radiobutton(frame, text='Celsius', variable=unit_var, value='metric', bg='#b2ebf2').grid(row=2, column=0, sticky=W)
Radiobutton(frame, text='Fahrenheit', variable=unit_var, value='imperial', bg='#b2ebf2').grid(row=2, column=1, sticky=W)

get_button = Button(app, text='Get Weather 🌦️', font=('Arial', 14), bg='#0288d1', fg='white', command=lambda: get_weather(city_entry.get() or get_location(), unit_var.get()))
get_button.pack(pady=10)

weather_label = Label(app, text='', font=('Arial', 12), justify=LEFT, bg='#e0f7fa', fg='#004d40')
weather_label.pack(pady=20, padx=10, anchor=W)

app.mainloop()
