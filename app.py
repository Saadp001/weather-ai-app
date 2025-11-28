from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from dotenv import load_dotenv
load_dotenv()
import google.genai as genai

import os


app = Flask(__name__)

# configure api of gemini for ai use 


#will get the data from route /ai-insights
def generate_ai_insights(city, temperature, condition, humidity, wind):
    prompt = f"""
    You are a friendly weather assistant. Using the data below, generate a SHORT and CLEAN 3-section response:

    City: {city}
    Temperature: {temperature}°C
    Condition: {condition}
    Humidity: {humidity}%
    Wind: {wind} m/s

    FORMAT EXACTLY LIKE THIS (no extra lines):

    🌤️ **Weather in {city}:**
    • One fun, simple sentence about the weather.

    🧭 **Activity Tip:**
    • One short idea based on the weather.

    ⚠️ **Alert:**
    • Give a warning ONLY if needed.
    • If no risks → say: "No major risks today 🌈".

    Keep it short, friendly, and emoji-friendly.
    """


    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))    # storing gemini key inside client 

    # api calling to gemini and storing the response/output in response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )


    return response.text

# Database 
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  # configure sqlalchemy(orm) db to postgressql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_ofdb = db.Column(db.String(50), nullable=False)
    temperature_ofdb = db.Column(db.Float, nullable=False)
    condition_ofdb = db.Column(db.String(50), nullable=False)
    icon_ofdb = db.Column(db.String(100))

    humidity_ofdb = db.Column(db.Integer, nullable=False)
    wind_ofdb = db.Column(db.Float, nullable=False)
    sunrise_ofdb = db.Column(db.String(10), nullable=False)
    sunset_ofdb = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return f"<Task {self.city_ofdb}>"

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        city_name = request.form["city"]
        
        # 1. Check if city exists in DB
        new_task = MyTask.query.filter_by(city_ofdb=city_name).first()

        # 2. If not found → call API and store
        if not new_task:
        # Weather API
            API_KEY = os.getenv("OPENWEATHER_API_KEY")

            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
            geo_res = requests.get(geo_url).json()

            if not geo_res:
                return render_template("index.html", error="City not found!", task=None)

            lat = geo_res[0]["lat"]
            lon = geo_res[0]["lon"]

            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
            data = requests.get(weather_url).json()


        # url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},&appid={API_KEY}"
        # response = requests.get(url)
        # data = response.json()

        # Handle city not found
            if data.get("cod") != 200:
                return render_template("index.html", task=None, error="City not found!")

        # Extract required data
            temperature = data['main']['temp'] - 273.15
            condition = data['weather'][0]['main']
            icon_code = data['weather'][0]['icon']
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
            sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")


        # Create ONE database row
            new_task = MyTask(
    
                city_ofdb = city_name,
                temperature_ofdb = temperature,
                condition_ofdb = condition,
                icon_ofdb = icon_code,
                humidity_ofdb = humidity,
                wind_ofdb = wind,
                sunrise_ofdb = sunrise,
                sunset_ofdb = sunset
            )

            db.session.add(new_task)
            db.session.commit()

        return render_template("index.html", new_task=new_task)

    # GET → shows nothing at first 
    # task = MyTask.query.order_by(MyTask.id.desc()).first()
    # return render_template("index.html", task=none)
        # 3. Return page with this city's data
    return render_template("index.html", new_task=None)


#will get data from js 
@app.route('/ai-insights', methods=['POST'])
def ai_insights():
    #storing the values in diff variables this variables are not connected to flask other variables 
    #we are just creating new variables inside this route to store teh data 
    city = request.form.get("city")
    temperature = request.form.get("temperature")
    condition = request.form.get("condition")
    humidity = request.form.get("humidity")
    wind = request.form.get("wind")

# giving the values through variables of this route to teh function and calling it and then storing the ans in insights
    insights = generate_ai_insights(city, temperature, condition, humidity, wind)

    return jsonify({"insights": insights})
#now this will return to the js and then js will show the output to webpage 

if __name__ == "__main__":

    app.run(debug=True)
