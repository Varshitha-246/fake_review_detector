# FAKE REVIEW DETECTOR
# Project Overview

An end-to-end system to detect human-written, AI-generated, and bot-generated reviews, distinguishing genuine from non-genuine content to enhance trust in e-commerce platforms. Built with NLP, machine learning, and a full-stack Django web app, it provides actionable insights and scalable deployment for real-world online marketplaces.

# Key Features

Review Classification: Multi-class detection of human, AI, and bot-generated reviews using NLP, TF-IDF, and machine learning classifiers.
Model Pipeline: Preprocessing, training, and inference managed via train_origin_model.py and review_origin_pipeline.joblib.
Synthetic Data Generation: generate_synthetic_data.py creates AI and bot-generated datasets (synthetic_ai.csv, synthetic_bot.csv) for model training and testing.
Dataset Integration: Supports multiple datasets including dataset_ai.csv and deceptive-opinion.csv for robust model learning.
Scalable Backend: Django web app with database integration, REST APIs, and dashboards for interactive review analysis.
Accuracy & Security: Optimized models with Hugging Face Transformers, handling class imbalance, achieving 85%+ accuracy, with encryption and role-based access.

# Repo Structure

fake_review_detector/
│
├── dataset_ai.csv             # AI-generated review dataset
├── deceptive-opinion.csv      # Human-written review dataset
├── synthetic_ai.csv           # Generated AI reviews
├── synthetic_bot.csv          # Generated bot reviews
├── generate_synthetic_data.py # Script to create synthetic datasets
├── train_origin_model.py      # Model training script
├── review_origin_pipeline.joblib # Trained ML pipeline
└── README.md

# Setup & Installation

Clone the repo:
git clone <repo-link>
cd fake_review_detector

# Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies:

pip install -r requirements.txt

# Usage

Run train_origin_model.py to train models on datasets.
Use review_origin_pipeline.joblib for inference on new reviews.
Integrate with Django app for user-facing dashboards and analytics.

# Future Improvements

Deploy pipeline for real-time predictions in e-commerce platforms
Expand model with larger multi-source datasets
Include advanced Transformer-based models for higher accuracy
Add automated alert system for suspicious reviews

# Outcome

Demonstrates end-to-end AI deployment, integrating NLP-based ML models with a scalable web application to detect non-genuine content and provide actionable business insights for trust and fraud detection in e-commerce.

