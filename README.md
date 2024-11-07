# WriteFlow - A Flask and PostgreSQL-based Blog Management Project 🚀

## 📖 Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation and Setup](#installation-and-setup)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Front-end Integration](#front-end-integration)
8. [Contributing](#contributing)
9. [License](#license)

## 🌐 Introduction
WriteFlow is a blog management web application built using the Flask web framework and PostgreSQL as the database. This project aims to provide a comprehensive platform for users to create, manage, and publish blog posts.

## ✨ Features
- User registration and authentication 🔒
- Create, edit, and delete blog posts ✍️
- Categorize and tag blog posts 🏷️

## 🛠️ Technology Stack
- Python 
- Flask 
- PostgreSQL 🗄
- SQLAlchemy 
- Jinja2 (for templates) 
- Bootstrap (for UI) 

## 🧑‍🔧 Installation and Setup

### 📋 Prerequisites
- Python 3.x 
- PostgreSQL 
- (Optional) Virtual environment management tool (e.g., venv, pipenv, conda) 🌐

### 🛠 Setup
1. Clone the repository: 
   ```
   git clone https://github.com/justparthi/Write-Flow.git
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv env
   source env/bin/activate
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the PostgreSQL database:
   - Create a new database
   - Update the database connection details in the project's configuration file
5. Run database migrations (if applicable):
   ```
   flask db upgrade
   ```
6. Start the development server:
   ```
   flask run
   ```
## 🌐 Deployment

1. **Deploy on Vercel**: Next.js works seamlessly with Vercel. Push your repository to GitHub and import it into Vercel.
2. **Set Environment Variables**: Add your Supabase environment variables in Vercel’s dashboard.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.


## 📞 Support

For any questions, please open an issue or contact us directly.
