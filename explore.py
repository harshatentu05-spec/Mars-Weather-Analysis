import requests
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json"

response = requests.get(URL, timeout=20)
response.raise_for_status()

data = response.json()
df = pd.DataFrame(data["soles"])

# Columns that should contain numbers
num_cols = [
    "sol", "ls", "min_temp", "max_temp", "pressure",
    "min_gts_temp", "max_gts_temp"
]

# Convert numeric columns; invalid values such as "--" become NaN
df[num_cols] = df[num_cols].apply(
    pd.to_numeric, errors="coerce"
)

# Convert date strings into datetime values
df["terrestrial_date"] = pd.to_datetime(
    df["terrestrial_date"], errors="coerce"
)
print(df.isnull().sum())
print(df.dtypes)
print(df['sol'].min(), df['sol'].max())
print("Invalid dates:", df["terrestrial_date"].isna().sum())

print("Duplicate rows:", df.duplicated().sum())

print("Missing values in numeric columns:")
print(df[num_cols].isnull().sum())
other_cols = [
    "abs_humidity",
    "wind_speed",
    "wind_direction",
    "atmo_opacity",
    "local_uv_irradiance_index"
]

for col in other_cols:
    print(f"\n{col}:")
    print(df[col].value_counts(dropna=False).head(10))

# Create a separate copy for cleaning
clean = df.copy()

# Drop columns that contain only unavailable values
unavailable_cols = [
    "abs_humidity",
    "wind_speed",
    "wind_direction"
]

clean = clean.drop(columns=unavailable_cols)

# Replace the missing-data marker in categorical columns
categorical_cols = [
    "atmo_opacity",
    "local_uv_irradiance_index"
]

for col in categorical_cols:
    clean[col] = clean[col].replace("--", pd.NA)

# Check the results
print("Original shape:", df.shape)
print("Cleaned shape:", clean.shape)

print("\nMissing categorical values:")
print(clean[categorical_cols].isna().sum())

print("\nRemaining columns:")
print(clean.columns.tolist())
# Calculate the rolling median of minimum temperature
rolling = clean["min_temp"].rolling(
    15,
    center=True,
    min_periods=5
).median()

# Flag readings more than 15 degrees from the rolling median
clean["min_temp_outlier"] = (
    clean["min_temp"] - rolling
).abs() > 15

# Count suspicious readings
print(
    "Suspicious minimum-temperature readings:",
    clean["min_temp_outlier"].sum()
)

# Display the flagged readings for inspection
print(
    clean.loc[
        clean["min_temp_outlier"],
        ["sol", "terrestrial_date", "min_temp"]
    ].head(10)
)
# Inspect temperatures around the first flagged reading
first_index = clean.index[clean["min_temp_outlier"]][0]

start = max(clean.index.min(), first_index - 5)
end = min(clean.index.max(), first_index + 5)

print("\nTemperatures around the first flagged reading:")
print(
    clean.loc[
        start:end,
        ["sol", "terrestrial_date", "min_temp"]
    ].to_string(index=False)
)
plot_df = clean.dropna(subset=["pressure", "ls"])

# Average pressure for each solar longitude
trend = (
    plot_df.groupby("ls", as_index=False)["pressure"]
    .mean()
    .sort_values("ls")
)

plt.figure(figsize=(10, 6))
plt.plot(trend["ls"], trend["pressure"])

plt.xlabel("Solar longitude (degrees)")
plt.ylabel("Average atmospheric pressure (Pa)")
plt.title("Mars Atmospheric Pressure Across Solar Longitude")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Calculate daily temperature range
clean["temp_range"] = clean["max_temp"] - clean["min_temp"]

temp_df = (
    clean.dropna(subset=["sol", "temp_range"])
    .sort_values("sol")
    .copy()
)

# Smooth the trend using a 15-sol rolling median
temp_df["temp_range_smooth"] = (
    temp_df["temp_range"]
    .rolling(15, center=True, min_periods=5)
    .median()
)

plt.figure(figsize=(10, 6))

plt.plot(
    temp_df["sol"],
    temp_df["temp_range_smooth"]
)

plt.xlabel("Martian sol")
plt.ylabel("Temperature range (°C)")
plt.title("Smoothed Daily Temperature Range on Mars")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()