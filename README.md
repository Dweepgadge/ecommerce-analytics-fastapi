# 🛒 Data-Driven E-Commerce Analytics Platform

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Cloud%20Neon-blue.svg)
![Pytest](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)
![Security](https://img.shields.io/badge/Auth-JWT%20%2B%20Bcrypt-red.svg)

A production-grade, full-stack data analytics and order management platform built with **FastAPI**, **Cloud PostgreSQL (Neon)**, and **Pandas**. Features automated **Pydantic** data validation, stateless **JWT Authentication**, automated unit testing with **Pytest**, and an interactive **Streamlit** machine learning dashboard.

---

## 🏗️ System Architecture

```text
       [ Client / Frontend (Tailwind CSS / Streamlit) ]
                             │  (REST API with Bearer JWT)
                             ▼
                [ FastAPI Application Server ]
                             │
     ┌───────────────────────┼───────────────────────┐
     ▼                       ▼                       ▼
[ Pydantic Engine ]    [ SQLAlchemy ORM ]     [ Pandas Engine ]
(Data Validation)             │             (Live Business Analytics)
                             ▼
               [ Cloud PostgreSQL (Neon DB) ]

🚀 Key Features
RESTful API Backend: High-performance asynchronous routes for order processing, inventory tracking, and data lookup.
Database & ORM: Cloud-hosted PostgreSQL (Neon) integrated via SQLAlchemy ORM with session dependency injection to prevent connection leaks.
Enterprise Security: User registration and login powered by Bcrypt password hashing and stateless JWT (JSON Web Tokens).
Live Business Analytics: Embedded Pandas pipeline computing real-time KPIs (Total Revenue, Average Order Value, Sales Volume).
Automated Testing Suite: 100% passing unit tests using Pytest and FastAPI TestClient covering security, validation, and CRUD operations.
Interactive ML Dashboard: Built with Streamlit (pure Python) for real-time customer churn prediction and revenue visualization.
Containerized Deployment: Packaged using a lightweight multi-layer Docker image (python:3.11-slim).

🛠️ Tech Stack
Backend: Python 3.11+, FastAPI, Pydantic, Uvicorn
Database: Cloud PostgreSQL (Neon), SQLAlchemy ORM
Security: PyJWT, Bcrypt, OAuth2 Password Bearer
Data Processing & ML: Pandas, NumPy, Scikit-learn
Testing & DevOps: Pytest, HTTPX TestClient, Docker, Git/GitHub
UI & Dashboards: Streamlit, Tailwind CSS, HTML5

📡 API Endpoints Overview
Method	Endpoint	Description	Auth Required?
POST	/register	Register a new user with hashed password	No
POST	/login	Authenticate user and issue JWT Bearer Token	No
GET	/orders/	Fetch all orders from PostgreSQL database	No
POST	/orders/	Create a new verified order	Yes (Bearer JWT)
GET	/orders/{id}	Fetch a single order by ID	No
DELETE	/orders/{id}	Delete an order by ID	Yes (Bearer JWT)
GET	/analytics/	Compute live revenue and AOV using Pandas	No
GET	/docs	Interactive Swagger UI API documentation	No
