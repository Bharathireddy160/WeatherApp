
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "ad284b4507c2d7dd9dc176aadf00073a"

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."

        else:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:
                response = requests.get(
                    WEATHER_URL,
                    params=params,
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()

                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temperature": round(data["main"]["temp"]),
                        "feels_like": round(
                            data["main"]["feels_like"]
                        ),
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"],
                        "description": data["weather"][0]["description"].title(),
                        "icon": data["weather"][0]["icon"]
                    }

                elif response.status_code == 404:
                    error = "City not found. Check the spelling."

                elif response.status_code == 401:
                    error = (
                        "Invalid API key or key not activated. "
                        "Check your OpenWeather account."
                    )

                else:
                    error = f"Weather service error: {response.status_code}"

            except requests.exceptions.Timeout:
                error = "Request timed out. Please try again."

            except requests.exceptions.RequestException:
                error = "Connection failed. Check your internet."

    return render_template(
        "index.html",
        weather=weather,
        error=error,
        city=city
    )


if __name__ == "__main__":
    app.run(debug=True)
