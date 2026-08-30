# personal_finance_intelligence


A privacy-first personal finance web application designed to help users track, understand, and improve their financial behavior.

The system combines financial record keeping with budgeting, goal tracking, investment analysis, and statistical insights.

Project 1 of a three-project engineering progression.

The primary goal of this project is to build a complete production-minded system from scratch while developing strong backend, database, analytics, and ML engineering fundamentals.

# Overview
Managing personal finances is not only about recording expenses.

A useful financial system should help a user answer questions such as:

Where is my money going?
How much am I actually spending in each category?
Am I staying within my budget?
What is my current net worth?
Am I progressing toward my financial goals?
How is my spending changing over time?
What recurring expenses do I have?
How are my investments performing?

This project aims to turn raw financial activity into useful financial understanding and decision support.

Core loop:
Track -> Understand -> Plan -> Act -> Measure -> Improve

# Features

## core features
- User authentication
- Multi-device data synchronization
- Manual transaction entry
- CSV transaction import
- Transaction categorization
- Account management
- Budget planning
- Budget vs. actual spending
- Financial goal tracking
- Net worth calculation
- Monthly and category-based spending analysis
- Recurring transaction detection
- Investment and holding tracking
- XIRR-based investment return calculation

## Planned Intelligence Features
- Automatic transaction categorization
- Spending anomaly detection
- Advanced statistical analysis
- Personalized financial insights
- What-if financial simulations
- Natural-language "Ask Your Data"

ML features will only be introduced when they provide a meaningful advantage over simpler approaches.

# Tech Stack
- Python 3.14
- FastAPI
- PostgreSQL 18.4 (Docker)
- SQLAlchemy 2.x ORM
- Alembic for migrations
- Pydantic for validation

# Current Status
- ✅ Core database models (User, Account, Category, Transaction)
- ✅ Database constraints and validation
- ⏳ Backend API endpoints
- ⏳ Frontend UI

# Architecture

The project follows a modular monolith architecture.

The goal is to keep the system simple enough to develop and understand while maintaining clear boundaries between different areas of the application.

                    Web Frontend
                         │
                         │ HTTP / REST API
                         ▼
                ┌─────────────────┐
                │    FastAPI      │
                │    Backend      │
                └────────┬────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
       Business       Analytics       Auth
        Logic         / ML Logic      / Security
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  ┌─────────────┐
                  │ PostgreSQL  │
                  └─────────────┘

The backend is organized into domain-oriented modules rather than being split into microservices.


