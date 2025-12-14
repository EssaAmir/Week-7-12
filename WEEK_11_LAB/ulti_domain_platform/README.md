# Multi-Domain Intelligence Platform

**Student Name:** [Your Name Here]
**Student ID:** [Your ID Here]
**Module:** CST1510 - Coursework 2

## 📖 Project Overview
The Multi-Domain Intelligence Platform is a centralized command center designed to unify workflows for three distinct technical domains:
1.  **🛡️ Cybersecurity:** Incident tracking and threat analytics (solving the "Phishing Surge" bottleneck).
2.  **📊 Data Science:** Dataset governance and resource tracking (solving the "Data Sprawl" issue).
3.  **💻 IT Operations:** Ticket management and staff performance monitoring (solving the "Service Desk Latency" issue).

This project implements a **Tier 3 (High Distinction)** scope, delivering functional dashboards for all three domains using a micro-service architecture.

## 🚀 How to Run the Application

### 1. Prerequisites
Ensure you have Python installed. Install the required dependencies using the following command:
```bash
pip install streamlit openai bcrypt pandas
2. OpenAI API Setup
To enable the AI Assistant features, you must configure your API key:

Create a folder named .streamlit in the root directory.

Create a file named secrets.toml inside that folder.

Add your API key to the file:

Ini, TOML

OPENAI_API_KEY = "sk-proj-..."
3. Launching the Application
Navigate to the project directory in your terminal and run the main application file:

Bash

cd ulti_domain_platform
streamlit run Home.py
🏗️ System Architecture (Week 11 Refactoring)
The application has been refactored from a procedural script into a modular Object-Oriented structure:

models/: Contains entity classes (User, SecurityIncident, Dataset, ITTicket) that encapsulate data and business logic.

services/: Contains manager classes (AuthManager, DatabaseManager, AIAssistant) that handle data persistence, security, and external API calls.

pages/: Contains the Streamlit frontend files, strictly separated from the backend logic.

🔑 Default Credentials
Username: admin

Password: (Please register a new user on the Login page to start)