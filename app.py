from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from dotenv import load_dotenv
load_dotenv()
import os


app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        city_name = request.form["city"]

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

        return redirect("/")

    # GET → show latest search only
    task = MyTask.query.order_by(MyTask.id.desc()).first()
    return render_template("index.html", task=task)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
