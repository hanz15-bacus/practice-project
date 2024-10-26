from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'your_api_key'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather_data = get_weather(city)
            if weather_data:
                return render_template("index.html", weather=weather_data)
            else:
                return render_template("index.html", error="City not found!")
    return render_template("index.html")

def get_weather(city):
    try:
        complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        # Check if the response contains the expected data
        if data.get("cod") == 200:
            main = data.get("main", {})
            wind = data.get("wind", {})
            weather = data["weather"][0]

            weather_info = {
                "city": city,
                "temperature": main.get("temp", "N/A"),
                "pressure": main.get("pressure", "N/A"),
                "humidity": main.get("humidity", "N/A"),
                "description": weather["description"].capitalize(),
                "wind_speed": wind.get("speed", "N/A"),
                "icon": weather["icon"]
            }
            return weather_info
        else:
            print("Error:", data.get("message", "City not found"))
            return None
    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    app.run(debug=True)
