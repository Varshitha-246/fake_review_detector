import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Load datasets
print("Loading primary Amazon dataset...")
amazon_df = pd.read_csv("dataset_ai.csv")  # JialuenYang dataset
amazon_df = amazon_df.rename(columns={"body": "text", "isAI": "origin"})
amazon_df["origin"] = amazon_df["origin"].map({0: "HUMAN", 1: "AI", 2: "AI"})
print("Primary distribution:\n", amazon_df["origin"].value_counts())

print("\nLoading BOT dataset (deceptive opinion corpus)...")
bot_df = pd.read_csv("deceptive-opinion.csv")
bot_df = bot_df.rename(columns={"text": "text"})
bot_df["origin"] = bot_df["deceptive"].map({
    "deceptive": "BOT",
    "truthful": "HUMAN"
})
bot_df = bot_df[["text", "origin"]]
print("BOT distribution:\n", bot_df["origin"].value_counts())

print("\nLoading synthetic AI & BOT samples...")
syn_ai = pd.read_csv("synthetic_ai.csv")
syn_bot = pd.read_csv("synthetic_bot.csv")

# Combine datasets
full_df = pd.concat([
    amazon_df[["text", "origin"]],
    bot_df,
    syn_ai,
    syn_bot
], ignore_index=True)

print("\nCombined distribution:\n", full_df["origin"].value_counts())

# 🧹 CLEAN DATA
full_df["text"] = full_df["text"].astype(str)
full_df = full_df[full_df["text"].str.strip() != ""]
full_df.dropna(subset=["text", "origin"], inplace=True)

print("\nAfter cleaning:", full_df.shape)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    full_df["text"], full_df["origin"], test_size=0.2, random_state=42, stratify=full_df["origin"]
)

print("\nTraining model...")
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", SGDClassifier(loss="log_loss", max_iter=2000))
])

model.fit(X_train, y_train)

preds = model.predict(X_test)

print("\nValidation Report:")
print(classification_report(y_test, preds))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, preds))

# ------- FIX: Ensure directory exists -------
MODEL_DIR = "ml_models"
os.makedirs(MODEL_DIR, exist_ok=True)

save_path = os.path.join(MODEL_DIR, "review_origin_pipeline.joblib")
joblib.dump(model, save_path)

print("\nModel saved to:", save_path)
