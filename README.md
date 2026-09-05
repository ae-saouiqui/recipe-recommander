# Recipe Recommendation System

> An end-to-end recipe recommendation application combining data engineering, NLP-based feature extraction, recommendation techniques, a REST API, and a React web interface.

---

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Apache Parquet](https://img.shields.io/badge/Apache%20Parquet-50ABF1?style=for-the-badge&logo=apache&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Apache Zeppelin](https://img.shields.io/badge/Apache%20Zeppelin-F5A800?style=for-the-badge&logo=apache&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Recommendation Pipeline](#recommendation-pipeline)
- [Data Processing](#data-processing)
- [Backend](#backend)
- [Frontend](#frontend)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)


---

## Overview

This project implements a recipe recommendation system designed to help users discover recipes based on available ingredients and product information.

The system combines a data processing pipeline with a recommendation engine and a web-based interface.

The project is divided into two main components:

- **Backend**: Responsible for data processing, feature extraction, vectorization, recommendation logic, and exposing the recommendation functionality through an API.
- **Frontend**: A React application providing an interactive interface for entering recipe-related information and displaying recommendations.

The data processing workflow relies on Apache Spark for ETL, text preprocessing, and feature vectorization.

---

## Features

- Recipe recommendation based on user input
- Ingredient and product information extraction
- Data cleaning and preprocessing
- Text tokenization
- Stop-word removal
- TF-IDF feature extraction
- Apache Spark-based data processing
- REST API for recommendation services
- React-based user interface
- Product browsing and filtering
- Interactive recommendation results
- Parquet-based storage for processed data

---

## Architecture

The overall system follows a client-server architecture:

```text
                         ┌─────────────────────┐
                         │      React App      │
                         │   Frontend / Vite   │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │     REST API        │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Recommendation      │
                         │ Engine              │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Processed /          │
                         │ Vectorized Data      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Apache Spark     │
                         │ ETL / NLP / TF-IDF  │
                         └─────────────────────┘
```
---

## Recommendation Pipeline

The recommendation workflow consists of several stages:
```text
Raw Data
   │
   ▼
Data Cleaning
   │
   ▼
Text Preprocessing
   │
   ▼
Tokenization
   │
   ▼
Stop-word Removal
   │
   ▼
Term Frequency
   │
   ▼
Inverse Document Frequency
   │
   ▼
TF-IDF Representation
   │
   ▼
Recommendation Engine
   │
   ▼
Ranked Recommendations
   │
   ▼
REST API
   │
   ▼
React Frontend
```

The vectorization process uses an Apache Spark ML pipeline composed of:

`Tokenizer`
`StopWordsRemover`
`HashingTF`
`IDF`

---

## Data Processing

`Apache Spark` is used to process and transform the recipe and product data.

Several `Apache Zeppelin` notebooks are included in the repository to document the data engineering workflow:

```text
backend/notebooks/
├── ETL_2KVH4BXJG.zpln
├── Cleaning_2KVJYPFG9.zpln
├── Cleaning_Final_2KYH42JSP.zpln
├── Cleaning_python_2KY69J5SA.zpln
└── Recommandation_2KYGF3MH2.zpln
```
These notebooks cover different stages of the project, including:

- ETL operations
- Data cleaning
- Python-based preprocessing
- Recommendation experiments
- Feature engineering
- Vectorization
- Vectorization Pipeline

The Spark ML pipeline transforms textual information into numerical representations:
```text
Text
 │
 ▼
Tokenizer
 │
 ▼
StopWordsRemover
 │
 ▼
HashingTF
 │
 ▼
IDF
 │
 ▼
TF-IDF Vector
```

The resulting vectorizer is stored under:

`backend/vectorizer/`

The processed vectorized dataset is stored as:

`backend/vectorized_df.parquet/`

---

## Backend

The backend is implemented in Python and organized into several layers.
```text
backend/
├── api/
│   ├── controller/
│   ├── models/
│   ├── routes/
│   └── schemas/
│
├── recommander/
├── notebooks/
├── vectorizer/
├── vectorized_df.parquet/
└── app.py
```

### Recommendation Engine

The recommendation logic is located in:

`backend/recommander/`

Main components include:
| File                 | Description                        |
| -------------------- | ---------------------------------- |
| `recommander.py`     | Main recommendation logic          |
| `Recommandation.py`  | Recommendation processing          |
| `Extractor.py`       | Information and feature extraction |
| `file_extraction.py` | File and data extraction utilities |

### API Layer

The API is organized into controllers, routes, models, and schemas.
```text
backend/api/
├── controller/
│   └── recommandation_final.py
├── models/
│   └── database.py
├── routes/
│   └── recommandations.py
└── schemas/
    ├── products.py
    └── recipe.py
```

This separation allows the recommendation logic to remain independent from the API layer.

Frontend

The frontend is implemented using React and Vite.

frontend/
└── recipe_recommander/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── vite.config.js

| Component                   | Description                                             |
| --------------------------- | ------------------------------------------------------- |
| `RecipeInput.jsx`           | Interface for entering recipe or ingredient information |
| `Recommandation.jsx`        | Displays recommendation results                         |
| `ProductCard.jsx`           | Displays individual product information                 |
| `ProductListWithFilter.jsx` | Displays and filters products                           |
| `LoopText.jsx`              | Frontend text component                                 |


The frontend communicates with the backend through HTTP requests to the recommendation API.

---

## Getting Started
### Prerequisites

Make sure the following tools are installed:

- Python 3.x
- Node.js
- npm
- Apache Spark
- Apache Zeppelin, if you want to reproduce the data-processing notebooks

### Backend Setup

Navigate to the backend directory:

``bash
cd backend
``
Create a virtual environment:

```bash
python -m venv .venv
```
Activate the environment.
```bash
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```
Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:
```bash
python app.py
```

Frontend Setup


Open another terminal and navigate to the frontend:

```bash
cd frontend/recipe_recommander
```

Install the dependencies:
```bash
npm install
```
Start the development server:
```bash
npm run dev
```

Vite will display the local development URL in the terminal.
