# Personal Finance Manager

# Personal Finance Manager

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange?logo=mysql)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A desktop-based Personal Finance Management application built using Python, CustomTkinter, and MySQL.

The application helps users manage their daily finances by tracking expenses, income, budgets, reports, and savings through an intuitive graphical interface.

---

## Project Objective

The goal of this project is to provide a simple and intuitive desktop application that helps users manage their personal finances by tracking income, expenses, budgets, and financial reports in one place.

## Table of Contents

- Features
- Technologies Used
- Project Architecture
- Project Structure
- Installation Guide
- Screenshots
- Future Improvements
- Author

# Features

## User Authentication

* User login system
* User registration
* Profile management
* Update personal information

## Expense Management

* Add expenses
* View expense records
* Update expenses
* Delete expenses
* Search expenses by category
* Calculate total expenses

## Income Management

* Add income sources
* View income records
* Update income
* Delete income
* Calculate total income

## Budget Management

* Create monthly budgets
* Track category-wise budgets
* Update budgets
* Delete budgets

## Reports

* Monthly expense reports
* Monthly income reports
* Budget analysis
* Savings calculation

## Charts & Visualization

* Expense distribution charts
* Income vs expense comparison
* Monthly financial trends

## Account Settings

* View profile details
* Update profile information

---

# Technologies Used

| Technology      | Purpose                    |
| --------------- | -------------------------- |
| Python          | Core programming language  |
| CustomTkinter   | Modern GUI framework       |
| MySQL           | Database management        |
| MySQL Connector | Python-Database connection |
| Matplotlib      | Data visualization         |

---

# Project Architecture


## Architecture

This project follows an Object-Oriented Programming (OOP) architecture with a layered design:

- GUI Layer (CustomTkinter)
- Business Logic Layer (Manager Classes)
- Data Model Layer
- Database Layer (MySQL)

This separation of concerns makes the project modular, maintainable, and scalable.

```
User
 |
 |
CustomTkinter GUI
 |
 |
Pages Layer
 |
Dashboard
Expenses
Income
Budget
Reports
Charts
Account
 |
 |
Manager Layer
 |
ExpenseManager
IncomeManager
BudgetManager
ReportManager
ChartsManager
AccountManager
 |
 |
MySQL Database
 |
Users
Expenses
Income
Budgets
```

---

# Project Structure

```
Finance Manager

│
├── main.py
├── gui.py
├── database.py
├── models.py
│
├── expense.py
├── income.py
├── budget.py
├── report.py
├── charts.py
├── account.py
│
├── pages/
│   ├── dashboard_page.py
│   ├── expense_page.py
│   ├── income_page.py
│   ├── budgets_page.py
│   ├── reports_page.py
│   ├── charts_page.py
│   └── account_page.py
│
├── assets/
│
└── README.md
```

---

# Installation Guide

## 1. Clone Repository

```bash
git clone <repository-link>
```

Move into project folder:

```bash
cd Finance-Manager
```

---

## 2. Install Dependencies

Install required packages:

```bash
pip install customtkinter
pip install mysql-connector-python
pip install matplotlib
pip install CTkMessagebox
```

---

## 3. Setup MySQL Database

Create database:

```sql
CREATE DATABASE personal_finance_manager;
```

Create required tables:

* Users
* Expenses
* Income
* Budgets

Update database credentials in:

```
database.py
```

---

## 4. Run Application

Start the application:

```bash
python main.py
```

---

# Screenshots

## Login

<img width="1117" height="782" alt="image" src="https://github.com/user-attachments/assets/aa25fd63-32e3-4d12-aa26-2240f2447214" />


## Register

<img width="1112" height="780" alt="image" src="https://github.com/user-attachments/assets/2c3a2575-d2cf-4e38-bf5c-9d469d30257e" />


## Dashboard

<img width="1918" height="1020" alt="image" src="https://github.com/user-attachments/assets/b8c6eac5-5c27-469a-ae92-23d78e77a6d4" />



## Expense Management

<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/8f17721b-d05b-4beb-af86-3d2df3ec2808" />



## Income Management

<img width="1918" height="1020" alt="image" src="https://github.com/user-attachments/assets/d1b0a3b3-082b-4099-b038-677024e8322c" />


## Budget Management

<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/2017304c-dfaf-4037-b5c5-542c45a76a07" />


## Reports

<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/99d8e264-d1bd-41de-a50d-41619f34709a" />


## Charts

<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/bc6594a0-88be-4b90-846d-616972bc4a1f" />


## Account Settings

<img width="1918" height="851" alt="image" src="https://github.com/user-attachments/assets/4407aa29-ee31-4796-8039-e149b6ce735f" />


---

# Future Improvements

* Password encryption
* Export reports to PDF
* Cloud database integration
* Mobile application version
* AI-based spending recommendations

---

## License

This project is developed for educational and portfolio purposes.

# Author

**Pranidhi Bhatt**

First Year Computer Engineering Student

Built using Python, CustomTkinter, and MySQL.

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?logo=github)](https://github.com/PranidhiBhatt)

