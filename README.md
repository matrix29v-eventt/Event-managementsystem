# Secure Event Management System (EMS) Monorepo

## 🌟 Project Overview

This repository contains a full-stack, secure Event Management System (EMS) designed to streamline the booking and management of events, venues, and vendors.

The system features robust **Role-Based Access Control (RBAC)** implemented using JWT authentication, distinguishing between standard clients and administrative users.

### Tech Stack

| Component | Technology | Role/Framework |
| :--- | :--- | :--- |
| **Backend (API)** | Python 3.11+ | FastAPI, SQLAlchemy (ORM), PostgreSQL |
| **Frontend (UI)** | JavaScript/Node.js | ReactJS |
| **Authentication** | Python-jose, Passlib | JWTs & Bcrypt Hashing |
| **Containerization** | Docker, Docker Compose | Orchestration for deployment |

## 🚀 Getting Started (Docker Deployment)

The fastest and most reliable way to run this entire application is using Docker Compose, which manages the Frontend, Backend, and PostgreSQL database as three interconnected services.

### Prerequisites

1.  **Docker Desktop** (Required to run Docker containers).
2.  **Git** (Required for cloning the repository).

### Step 1: Clone the Repository

```bash
git clone [https://github.com/matrix29v-eventt/Event-managementsystem.git](https://github.com/matrix29v-eventt/Event-managementsystem.git)
cd Event-managementsystem
