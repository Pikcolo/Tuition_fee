import requests
import pandas as pd

# Load JSON data
url = "https://my-tcas.s3.ap-southeast-1.amazonaws.com/mytcas/courses.json"
response = requests.get(url)
data = response.json()

# Keywords to match (broader matching)
keywords = [
    "วิศวกรรมคอมพิวเตอร์",
    "Computer Engineering",
    "วิศวกรรมปัญญาประดิษฐ์",
    "Artificial Intelligence Engineering",
]

results = []

for item in data:
    field_name_th = item.get("field_name_th", "").lower()
    program_name_th = item.get("program_name_th", "").lower()
    field_name_en = item.get("field_name_en", "").lower()
    program_name_en = item.get("program_name_en", "").lower()

    if any(keyword.lower() in field_name_th or
           keyword.lower() in program_name_th or
           keyword.lower() in field_name_en or
           keyword.lower() in program_name_en
           for keyword in keywords):

        cost_info = item.get("cost", "")
        cost_link = ""
        if "http" in cost_info:
            cost_link = "http" + cost_info.split("http", 1)[1]

        results.append({
            "University": item.get("university_name_th", ""),
            "Campus": item.get("campus_name_th", ""),
            "Faculty": item.get("field_name_th", ""),
            "Program": item.get("program_name_th", ""),
            "Tuition Fee": cost_info,
        })

# Convert to DataFrame
df = pd.DataFrame(results)

output_path = "data/tuition_data.xlsx"  
df.to_excel(output_path, index=False)

print(f"Saved: {output_path} ({len(df)} records)")
