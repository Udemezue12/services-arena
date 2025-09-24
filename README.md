🎨✨ SERVICES ARENA ✨🎨

🌍 Live Demo 👉 Services Arena

🚀💡 What is Services Arena?

🎯 Services Arena is a dynamic platform where:

🛠️ Providers create and showcase their services

📅 Users can book providers for specific needs

⭐ Clients leave reviews & ratings after booking

🔔 Real-time updates ensure seamless interactions

Think of it as your digital marketplace for skills and services!

🛠️⚙️ Tech Stack
Layer	Tech
🌐 Backend	Flask 3.0.3 + Flask-SQLAlchemy + Flask-Migrate
🎨 Frontend	Flask Templates (Jinja2, HTML, CSS, JS, Bootstrap/Tailwind)
🗄️ Database	SQLAlchemy ORM + Alembic
🔒 Auth	Flask-Login + Flask-Bcrypt
💌 Email	Flask-Mail (notifications)
💳 Payments	Paystack Integration
🔄 Realtime	Flask-SocketIO (WebSocket support)
🚀 Deployment	Gunicorn / Waitress + Whitenoise + Render
📂📁 Project Structure
services-arena/
│── book/               # Booking module
│── instance/           # Config + SQLite DB (if used)
│── migrations/         # Database migrations (Alembic)
│── __pycache__/        # Python cache
│── config.py           # App configuration
│── package.json        # JS dependencies (frontend assets)
│── package-lock.json
│── Procfile            # For deployment (Render/Heroku)
│── requirements.txt    # Python dependencies
│── run.py              # App entry point
│── samole.py           # Sample/test script

🔑📦 Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/services-arena.git
cd services-arena

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables (.env)
SECRET_KEY=supersecret
SQLALCHEMY_DATABASE_URI=sqlite:///services.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_password
PAYSTACK_SECRET_KEY=your_paystack_secret

5️⃣ Run Database Migrations
flask db init
flask db migrate
flask db upgrade

6️⃣ Start Server
python run.py


🌍 App will run at 👉 http://127.0.0.1:5000

🌟🎉 Key Features

🛠️ Service Creation – providers can create, edit, and manage services

📅 Booking System – users book providers with scheduling support

💳 Payment Integration – secure payments via Paystack

⭐ Review System – users can leave ratings & reviews

🔔 Notifications & Emails – confirmations & updates

⚡ Realtime Updates – booking confirmations with Flask-SocketIO

🎨 Modern UI – clean & responsive design

🐳🐙 Deployment (Render/Heroku/Docker)

🟣 Render (Current Live) → https://services-arena-ya5s.onrender.com

🐳 Docker Support (if enabled):

docker build -t services-arena .
docker run -p 5000:5000 services-arena

🤝💬 Contributing

🍴 Fork the repo

🌱 Create a feature branch (feature/amazing-feature)

✅ Commit changes

🚀 Push branch

🔥 Open Pull Request

📜📌 License

📝 Licensed under the MIT License — free to use & modify!

✨ Ready to book a service or share your skills?
👉 Visit: https://services-arena-ya5s.onrender.com