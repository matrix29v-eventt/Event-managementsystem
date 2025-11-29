# 🎉 Event Management System (FastAPI + SQLAlchemy)

A backend API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** to manage clients, venues, vendors, events, bookings, and payments.

---

## 🚀 Features
- Manage **Clients, Venues, Vendors, Events, Bookings, and Payments**
- PostgreSQL database integration
- Pydantic models for validation
- Organized modular structure
- RESTful API with FastAPI
- Interactive API docs via **Swagger UI** (`/docs`)

---

## 📂 Project Structure
event-management-system/
│── app/
│ ├── init.py
│ ├── main.py # FastAPI entrypoint
│ ├── db.py # Database setup
│ ├── models/ # SQLAlchemy models
│ │ ├── init.py
│ │ └── models.py
│ ├── schemas/ # Pydantic schemas
│ │ ├── init.py
│ │ └── schemas.py
│ ├── routers/ # API endpoints
│ │ ├── init.py
│ │ ├── clients.py
│ │ ├── venues.py
│ │ ├── vendors.py
│ │ ├── events.py
│ │ ├── bookings.py
│ │ └── payments.py
│ └── crud/ # CRUD operations
│ ├── init.py
│ └── crud.py
│── requirements.txt # Dependencies
│── README.md # Documentation
│── .env # Environment variables
│── .gitignore



## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/anzer-farooq/event-management-system.git
cd event-management-system
2. Create Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure Environment
Create a .env file in the root directory:

ini
Copy code
DATABASE_URL=postgresql://username:password@localhost:5432/eventdb
(replace username, password, and eventdb with your DB credentials)

5. Run the Server
bash
Copy code
uvicorn app.main:app --reload
Server will start at:

cpp
Copy code
http://127.0.0.1:8000
📖 API Docs
FastAPI provides interactive docs:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

📝 Example Requests
Create a Client
json
Copy code
POST /clients/
{
  "name": "Joshua",
  "email": "joshua@example.com",
  "phone": "1234567890",
  "password": "securepass"
}
Create a Venue
json
Copy code
POST /venues/
{
  "name": "Grand Hall",
  "location": "New York",
  "capacity": 500
}
Create a Vendor
json
Copy code
POST /vendors/
{
  "name": "Elite Catering",
  "service_type": "Catering",
  "contact": "9876543210"
}
Create an Event
json
Copy code
POST /events/
{
  "name": "Wedding Ceremony",
  "date": "2025-09-20",
  "client_id": 1,
  "venue_id": 1
}
Create a Booking
json
Copy code
POST /bookings/
{
  "event_id": 1,
  "vendor_id": 1,
  "service_cost": 1500.00
}
Create a Payment
json
Copy code
POST /payments/
{
  "event_id": 1,
  "booking_id": 1,
  "amount": 1500.00,
  "method": "Credit Card",
  "status": "Completed",
  "date": "2025-09-12"
}
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature-name)

Commit changes (git commit -m "Added new feature")

Push to branch (git push origin feature-name)

Create a Pull Request

📜 License
This project is licensed under the MIT License – free to use and modify.
