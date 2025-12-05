import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 1. Load the dataset
# -------------------------------
df = pd.read_csv("weather.csv")

print("\n--- Dataset Head ---")
print(df.head())

print("\n--- Dataset Info ---")
print(df.info())

print("\n--- Dataset Describe ---")
print(df.describe())

# -------------------------------
# 2. Convert date column and sort
# -------------------------------
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
df = df.sort_values(by='date') 

# -------------------------------
# 3. Plot Temperature & Humidity
# -------------------------------
plt.figure(figsize=(12, 8))

# Temperature plot
plt.subplot(2, 1, 1)
plt.plot(df['date'], df['temperature'])
plt.title("Temperature Trend")
plt.xlabel("Year")
plt.ylabel("Temperature (°C)")

# Humidity plot
plt.subplot(2, 1, 2)
plt.plot(df['date'], df['humidity'], color="orange")
plt.title("Humidity Trend")
plt.xlabel("Year")
plt.ylabel("Humidity (%)")

plt.tight_layout()
plt.show()