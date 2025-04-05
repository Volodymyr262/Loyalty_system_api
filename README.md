# 🏆 Loyalty Program API 
(DEMO https://loyaltysystemapi-production.up.railway.app/)

A Django REST Framework-based API that powers a Loyalty Program system. Admin users (program owners) can manage loyalty programs, while registered users can earn and redeem points within those programs. The API uses token-based authentication and enforces strict permission rules.

---

## 🚀 Features

- Admin registration & authentication
- Loyalty program creation & management
- Assign users to programs and track point balances
- Point earning and redemption per user per program
- Automatic tier assignment based on balance


---

## 📚 API Endpoints Overview

All endpoints are prefixed with: `/api/`

### 🔐 Authentication (Admins Only)

| Method | Endpoint             | Description                         |
|--------|----------------------|-------------------------------------|
| POST   | `/register/`         | Register a new admin user           |
| POST   | `/login/`            | Login and receive auth token        |
| POST   | `/logout/`           | Logout and revoke auth token        |

---

### 🏢 Loyalty Programs (Admins Only)

| Method | Endpoint                         | Description                                |
|--------|----------------------------------|--------------------------------------------|
| GET    | `/loyalty-programs/`             | List programs owned by the admin           |
| POST   | `/loyalty-programs/`             | Create a new loyalty program               |
| GET    | `/loyalty-programs/{id}/`        | Retrieve a specific program                |
| PUT    | `/loyalty-programs/{id}/`        | Update a program                           |
| DELETE | `/loyalty-programs/{id}/`        | Delete a program                           |

---

### 💰 Point Balances

| Method | Endpoint                                   | Description                                           |
|--------|--------------------------------------------|-------------------------------------------------------|
| GET    | `/point-balances/?program_id={id}`         | Get current user's point balance in a program         |
| POST   | `/point-balances/earn/`                    | Earn points (Admin-controlled or via external action) |
| POST   | `/point-balances/redeem/`                  | Redeem points from a program                         |

> 🔐 Auth required. Point operations are permission-controlled by program ownership.


---

## 🛠️ Tech Stack
 -Python 3.12
 -Django 4.2
 -Django REST Framework
 -PostgreSQL 
 -Pytest
 ---
