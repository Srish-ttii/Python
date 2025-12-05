import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("weather.csv")
print(df.head())
print(df.info())
print(df.describe())


df['date'] = pd.to_datetime(df['date'])
df = df.dropna()

df = df[['date', 'temperature', 'humidity', 'rainfall']]



daily_mean = df['temperature'].mean()
monthly_stats = df.resample("M", on="date").mean()
yearly_stats = df.resample("Y", on="date").mean()



plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['temperature'])
plt.title("Daily Temperature Trend")
plt.savefig("temp_trend.png")
plt.close()

monthly_rain = df.resample("M", on="date")['rainfall'].sum()
plt.bar(monthly_rain.index, monthly_rain.values)
plt.title("Monthly Rainfall")
plt.savefig("rainfall.png")
plt.close()

plt.scatter(df['temperature'], df['humidity'])
plt.xlabel("Temp")
plt.ylabel("Humidity")
plt.savefig("scatter.png")
plt.close()

# Combined figure
fig, ax = plt.subplots(2, 1, figsize=(12, 10))
ax[0].plot(df['date'], df['temperature'])
ax[1].bar(monthly_rain.index, monthly_rain.values)
plt.savefig("dashboard.png")
plt.close()



monthly_group = df.groupby(df['date'].dt.month).mean()



df.to_csv("cleaned_weather.csv", index=False)

with open("summary.txt", "w") as f:
    f.write("Weather Data Summary\n")
    f.write(f"Avg Temp: {daily_mean}")
