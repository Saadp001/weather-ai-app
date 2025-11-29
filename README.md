# 🌦️ Weather AI App — Flask + OpenWeather + Gemini AI

A clean, fast, modern **weather application** built with **Flask**, showing real-time weather data + **AI-generated insights** using **Google Gemini**.
The app uses **PostgreSQL for caching**, **reducing API calls**, and provides a smooth user experience with a responsive UI.

🔗 **Live Demo:** [https://weather-ai.up.railway.app/](https://weather-ai.up.railway.app/)

---

## 🚀 Features

### 🌤️ **Real-Time Weather Data**

* Current temperature
* Weather condition
* Humidity %
* Wind speed
* Sunrise & Sunset timings

### 🤖 **AI Weather Insights (Gemini 2.5 Flash)**

* Weather summary
* Activity suggestion
* Alerts & tips
* Short, friendly, human-like narration

### 🗄️ **Smart API Optimization**

* City data stored in PostgreSQL
* No duplicate API calls for same city
* Faster load times + lower API usage

### 🎨 **Modern UI / UX**

* Soft gradients
* Clean weather card
* Styled AI insights box
* Disabled AI button until weather is fetched

### 🌐 **Fully Deployed**

* Dockerized
* Hosted on **Railway**
* Uses environment variables for security

---

## 📸 Screenshots

<img width="1600" height="900" alt="Screenshot (669)" src="https://github.com/user-attachments/assets/55ef955e-ee42-486c-a776-b75389bdda07" />
 <img width="1600" height="900" alt="Screenshot (668)" src="https://github.com/user-attachments/assets/18aa87ca-bb5f-41d6-88ff-3cfcbbcca189" />
<img width="1600" height="900" alt="Screenshot (667)" src="https://github.com/user-attachments/assets/9ca7e8f2-e021-4b22-a09b-14835885bf6f" />


---

## 🛠️ Tech Stack

### **Backend**

* Flask
* SQLAlchemy
* PostgreSQL
* OpenWeather API
* Google Gemini (google-genai SDK)

### **Frontend**

* HTML
* CSS (custom styling)
* Vanilla JavaScript
* Jinja2

### **Deployment**

* Railway
* Docker
* Gunicorn
* Environment variables

---

## 📁 Project Structure

```
├── app.py
├── requirements.txt
├── Dockerfile
├── Procfile (if using)
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md
```

---

## ⚙️ Installation & Setup (Local Development)

### 1️⃣ Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/weather-ai-app.git
cd weather-ai-app
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set environment variables

Create a **.env** file in the root folder:

```
OPENWEATHER_API_KEY=your_openweather_key
GEMINI_API_KEY=your_gemini_key
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME
```

### 5️⃣ Run the app

```bash
python app.py
```

App runs on:
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧠 How It Works (Flow)

### 🔹 **1. User enters city name**

Form sends POST → Flask receives the city.

### 🔹 **2. Check DB**

If city exists → load cached weather.

### 🔹 **3. Else call OpenWeather API**

Fetch:

* temp
* condition
* icon
* humidity
* wind
* sunrise / sunset

Store in PostgreSQL.

### 🔹 **4. Render UI**

Weather card appears.

### 🔹 **5. If user clicks "Generate Insights"**

JS → `/generate_insights` API → Gemini → response shown on UI.

---

## 🐳 Running with Docker

### Build image

```bash
docker build -t weather-ai-app .
```

### Run container

```bash
docker run -p 8000:8000 --env-file .env weather-ai-app
```

---

## 🚀 Deployment (Railway)

1. Create New Service → Deploy from GitHub
2. Add environment variables
3. Add `Dockerfile`
4. Deploy
5. Railway will build & run using Gunicorn

---

## 🔐 Environment Variables

| Variable              | Description             |
| --------------------- | ----------------------- |
| `OPENWEATHER_API_KEY` | Weather API key         |
| `GEMINI_API_KEY`      | Gemini AI key           |
| `DATABASE_URL`        | PostgreSQL database URL |

---

## 🤝 Contributing

Pull requests are welcome!
If you want to improve UI, add features, or optimize the app — feel free to fork and submit.

---

## ⭐ Show Support

If you like this project, please ⭐ the repository — it motivates me to build more!

---

## 👨‍💻 Author

**Saad Patel**
Backend & Cloud Enthusiast
Flask | DevOps | AI | AWS

---
