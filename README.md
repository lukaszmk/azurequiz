# 📘 Azure Quiz For cloud Concepts

## ✨ Overview

This Project is designed to upload an simple quiz app to Azure App Service.

## 🚀 Features

* Multiple choice questions

* Randomized quizzes

* Instant feedback on answers

* Score tracking

* Categories (e.g., Networking, Security, Compute, Storage)


##

## 🛠️ Technologies Used
- FastAPI: Python web framework for building the application and handling HTTP routes.

- Uvicorn: ASGI server for running the FastAPI app locally and on Azure App Service.
- Jinja2: Templating engine for rendering HTML templates (index.html, results.html).
- Python: Programming language (version 3.9 or higher) for the app’s backend logic.
- Python-Multipart: Library for parsing form data in FastAPI (used for quiz submission).
- Tailwind CSS: CSS framework (via CDN) for styling the quiz interface.
- HTML: Markup language for creating the web interface templates.
- Azure App Service: Cloud platform for deploying and hosting the app.
- Azure CLI: Command-line tool for deploying and managing the app on Azure.
- Git: Version control system for managing code and deploying to GitHub/Azure.
- VS Code: Integrated development environment for writing, testing, and deploying the app.


# 📦 Prerequsites

* Python 3.9 or higher: Download Python

* Git: Download Git

* Azure CLI: Install Azure CLI (for deployment)

* VS Code: Recommended for development and deployment (optional)

* Azure Account: Required for deployment to Azure App Service






## Start the APP

- pip install -r requirements.txt

Then activate the Virtual Enviroment

```bash
- python -m venv venv
```
```bash
- .\venv\Scripts\activate
```
After that run the app locally 
```bash
- uvicorn app:app --reload
```
Check if the APP is working in the browser.

Now the app is ready to uplod it to Azure App Service.

## Deploy APP to Azure
```bash
az group create --name AzureQuizRG --location westeurope

az appservice plan create --name AzureQuizPlan --resource-group AzureQuizRG --sku F1 --is-linux

az webapp create --name azurequizapp --resource-group AzureQuizRG --plan AzureQuizPlan --runtime "PYTHON:3.13"

az webapp config set --resource-group AzureQuizRG --name azurequizapp --startup-file "uvicorn app:app --host 0.0.0.0 --port 8000"
```
