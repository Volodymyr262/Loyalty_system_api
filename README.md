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
| GET    | `/api/point-balances/?program_id=` | Get point balance for logged-in user & program ID         |
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
