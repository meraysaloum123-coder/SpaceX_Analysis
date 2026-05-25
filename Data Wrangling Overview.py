import requests
import pandas as pd
launch_url = "https://api.spacexdata.com/v4/launches"
launch_data = requests.get(launch_url).json()

df = pd.DataFrame(launch_data)
df = df[["flight_number", "date_utc", "rocket", "launchpad", "payloads", "success"]]
df.head()
rocket_url = "https://api.spacexdata.com/v4/rockets" 
rocket_data = requests.get(rocket_url).json()
rocket_df = pd.DataFrame(rocket_data)[["id", "name"]] # تحويل JSON إلى DataFrame مع اختيار أعمدة فقط
rocket_df.columns = ["rocket", "rocket_name"]
df = df.merge(rocket_df, on="rocket", how="left")
df.head()
pad_url = "https://api.spacexdata.com/v4/launchpads" # جلب launchpads
pad_data = requests.get(pad_url).json()
pad_df = pd.DataFrame(pad_data)[["id", "name", "locality"]]
pd.DataFrame(pad_data)
pad_df.columns = ["launchpad", "launch_site", "site_location"]

df = df.merge(pad_df, on="launchpad", how="left")
df.head()
payload_url = "https://api.spacexdata.com/v4/payloads" # معالجة payloads (أهم خطوة)

payload_data = requests.get(payload_url).json()

payload_df = pd.DataFrame(payload_data)[["id", "mass_kg"]] # mass_kg الحمولة
payload_df.columns = ["payloads", "payload_mass"]
df["payloads"] = df["payloads"].apply(lambda x: x[0] if len(x) > 0 else None)
df = df.merge(payload_df, on="payloads", how="left")
df.head()
df = df.dropna(subset=["payload_mass"])
df["success"] = df["success"].fillna(0).astype(int)
final_df = df[[
    "flight_number",
    "date_utc",
    "rocket_name",
    "launch_site",
    "site_location",
    "payload_mass",
    "success"
]]
final_df.head()
final_df.to_csv("spacex_cleaned_data.csv", index=False)

print("Clean dataset saved!")

