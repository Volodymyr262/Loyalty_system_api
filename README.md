# 🏆 Loyalty Program API

A Django REST Framework-powered API that enables **application owners (admins)** to integrate a **loyalty program system** into their own apps. Admins can manage loyalty points, tiers, and user tasks through a secure and scalable backend API.

---

## 🎯 Project Purpose

This API is designed for **admins who own external applications** (e.g. e-commerce platforms, mobile apps, SaaS tools) and want to offer loyalty rewards to their users. Each admin manages:

- A unique **Loyalty Program**
- A list of **end-users** (customers)
- **Points** assigned per user based on actions
- Custom **tiers** and **tasks** for user engagement

---

## 🔗 API Endpoints

### 🔐 Authentication
| Method | Endpoint         | Description                      |
|--------|------------------|----------------------------------|
| POST   | `/api/register/` | Register a new admin user        |
| POST   | `/api/login/`    | Login and receive auth token     |
| POST   | `/api/logout/`   | Logout and revoke auth token     |

### 🧠 Loyalty Program
| Method | Endpoint                    | Description                            |
|--------|-----------------------------|----------------------------------------|
| GET    | `/api/loyalty-programs/`    | List all loyalty programs owned by admin |
| POST   | `/api/loyalty-programs/`    | Create a new loyalty program           |
| GET    | `/api/loyalty-programs/{id}/` | Retrieve a specific loyalty program   |
| PUT    | `/api/loyalty-programs/{id}/` | Update a loyalty program              |
| DELETE | `/api/loyalty-programs/{id}/` | Delete a loyalty program              |

### 💎 Tiers
| Method | Endpoint                | Description                          |
|--------|-------------------------|--------------------------------------|
| GET    | `/api/loyalty-tiers/`  | List all tiers for a program         |
| POST   | `/api/loyalty-tiers/`  | Create a new tier                    |
| GET    | `/api/loyalty-tiers/{id}/` | Retrieve a specific tier           |
| PUT    | `/api/loyalty-tiers/{id}/` | Update tier details                |
| DELETE | `/api/loyalty-tiers/{id}/` | Delete a tier                      |

### ⭐ Special Tasks
| Method | Endpoint                    | Description                            |
|--------|-----------------------------|----------------------------------------|
| GET    | `/api/special-tasks/`       | List all special tasks                 |
| POST   | `/api/special-tasks/`       | Create a new task                      |
| GET    | `/api/special-tasks/{id}/`  | Get task details                       |
| PUT    | `/api/special-tasks/{id}/`  | Update a task                          |
| DELETE | `/api/special-tasks/{id}/`  | Delete a task                          |

### 📊 Point Balance
| Method | Endpoint                           | Description                                               |
|--------|------------------------------------|-----------------------------------------------------------|
| GET    | `/api/point-balances/?program_id=` | Get point balances for owner of Loyalty program           |
| POST   | `/api/point-balances/`             | Manually create a point balance                           |

### ➕ Points Actions
| Method | Endpoint              | Description                                |
|--------|-----------------------|--------------------------------------------|
| POST   | `/api/points/earn/`   | Add points to a user’s balance             |
| POST   | `/api/points/redeem/` | Redeem points from a user’s balance        |

### 📈 Transactions
| Method | Endpoint              | Description                                |
|--------|-----------------------|--------------------------------------------|
| GET    | `/api/transactions/`  | List all transactions by user or program   |
| POST   | `/api/transactions/`  | Create a new transaction                   |

### 📌 User Task Progress
| Method | Endpoint                            | Description                              |
|--------|-------------------------------------|------------------------------------------|
| GET    | `/api/user-task-progress/`          | List progress for all tasks              |
| POST   | `/api/user-task-progress/`          | Create user task progress entry          |
| PUT    | `/api/user-task-progress/{id}/`     | Update task progress (e.g., mark done)   |

---

## 🛠️ Tech Stack

- Python 3.12
- Django 4.2
- Django REST Framework
- PostgreSQL
- Swagger (drf-yasg)
- Hosted on [Railway](https://railway.app)

---

## 📚 Documentation

Access Swagger UI at root path `/`  
e.g. [https://your-app.up.railway.app/](https://your-app.up.railway.app/)

---

## 🔐 Authentication Method

This API uses **Token Authentication**.  
Once logged in, include this in your headers:

```http
Authorization: Token <your-token>
