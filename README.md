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
