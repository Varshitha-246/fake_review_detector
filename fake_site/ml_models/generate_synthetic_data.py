import random
import pandas as pd

# ----------- Synthetic AI Reviews -----------
synthetic_ai = [
    "This product provides exceptional performance and outstanding quality far beyond ordinary expectations.",
    "An innovative solution delivering seamless functionality and remarkable efficiency across every task.",
    "The design is unbelievably refined, and the results exceeded all measurable standards.",
    "This revolutionary item has redefined convenience, offering unparalleled reliability and performance.",
    "Absolutely extraordinary experience overall — flawless execution and exceptional craftsmanship.",
    "Impressive functionality accompanied by effortless usability and precision-driven engineering."
]

# ----------- Synthetic BOT Reviews -----------
synthetic_bot = [
    "Buy now best deal!!! Limited time only!!! Click fast before gone!!!",
    "Super offer! Best product guaranteed!!! Order now now now!!!",
    "Great discount today only!!! Hurry up buy now free shipping!!!",
    "Amazing product!!! Best seller!!! Must buy!!! Unbeatable price!!!",
    "Click the link now !! Discount discount discount!!! Best results!!!",
    "Order today!!! Great choice great price great product!!!"
]

# Duplicate to increase dataset size
extended_ai = synthetic_ai * 180  # ~1080 samples
extended_bot = synthetic_bot * 180  # ~1080 samples

df_ai = pd.DataFrame({"text": extended_ai, "origin": "AI"})
df_bot = pd.DataFrame({"text": extended_bot, "origin": "BOT"})

df_ai.to_csv("synthetic_ai.csv", index=False)
df_bot.to_csv("synthetic_bot.csv", index=False)

print("Synthetic datasets created successfully.")
