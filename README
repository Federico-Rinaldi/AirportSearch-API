# AirportSearch API

![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?logo=postgresql)
![Docker](https://img.shields.io/badge/Container-Docker%20%7C%20Podman-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✈️ AirportSearch API

**AirportSearch API** is the official backend service for the **AirportSearch web application**.  
It exposes a high-performance, scalable REST API built with **FastAPI**, designed to serve structured aviation data to modern frontend clients.

This repository represents the **backend layer** of the AirportSearch ecosystem.

---

## 🧩 Ecosystem Overview

AirportSearch is composed of two main components:

### 🔹 Frontend
- Modern web application (React / Next.js)
- User interface for searching and exploring airport data
- Consumes this API exclusively

### 🔹 Backend (this repository)
- FastAPI-based REST API
- PostgreSQL database
- Alembic-managed schema and migrations
- Container-ready for production deployments

> This repository is intended to be used **together with the AirportSearch frontend**.

---

## 🏗️ Tech Stack

- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL**
- **Uvicorn**
- **Docker / Podman**

---

## 🗄️ Database Schema

This project includes:

- ✅ Complete **PostgreSQL schema**
- ✅ SQLAlchemy ORM models
- ✅ Alembic migration history

The schema reflects the **real production structure** used by AirportSearch and allows developers to:

- Recreate the database locally
- Apply migrations automatically
- Prepare for future public datasets

⚠️ **Important:**  
The **database data itself is currently private** and **not included** in this repository.  
A public data release is under evaluation and may be provided in the future.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-org/airportsearch-api.git
cd airportsearch-api
```
> **If you are using a container orchestration or container runtime solution, please refer to the Docker/Podman section.**

### **2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate
  ```
  
### **3. Install dependencies**
```bash
pip install -r requirements.txt
  ```
  
## **⚙️ Environment Configuration**

The application is configured **entirely via environment variables**, making it suitable for containers and cloud deployments.

Example:
```bash
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/airportsearch
  ```
> Environment files (.env) are intentionally excluded from version control.

##### Run Alembic migration here *see Migration Section

## **🚀 Running the API**

```bash
uvicorn app.main:app --reload
  ```

The API will be available at:

```bash
http://localhost:8000
  ```

## **🐳 Docker / Podman**

##### use Dockerfile.dev for local dev mode
##### use host.containers.internal:5432 only if DB is on another container
```bash
podman build -f Dockerfile.prod -t airport-api .
podman run -d --name airport-api \
  -p 8000:8000 \
  --env DATABASE_URL='postgresql://dbuser:dbpassword@host.containers.internal:5432/dbname?options=-csearch_path%3DSchemaDb' \
  airport-api
```

## **🛠️ Database Migrations (Alembic)**

#### **Apply all migrations**
```bash
alembic upgrade head
```
#### **Generate a new migration**
```bash
alembic revision --autogenerate -m "describe your change"
```

## **🔐 Data Availability**


Current status:

-   ❌ Production data is **not publicly available**
    
-   ✅ Database **schema is open and versioned**
    
-   🔜 Public dataset release is **planned / under evaluation**