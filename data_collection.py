import requests
import pandas as pd
url = "https://api.spacexdata.com/v4/launches"
response = requests.get(url)

data = response.json()

print("Number of launches:", len(data))
launches_list=[]
for launch in data: # data هي قائمة من الإطلاقات (launches)، ولهذا نستخدم for.
    launch_data = {
        "flight_number": launch.get("flight_number"),
        "name": launch.get("name"),
        "date_utc": launch.get("date_utc"),
        "rocket": launch.get("rocket"),
        "launchpad": launch.get("launchpad"),
        "success": launch.get("success")
    }

launches_list.append(launch_data)

df = pd.DataFrame(launches_list)
df.head()
df = df.dropna(subset=["success"])
df["success"] = df["success"].astype(int)
df.head()
df.to_csv("spacex_launch_data.csv", index=False)
print("Dataset saved successfully!")
