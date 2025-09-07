from datetime import datetime

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Current Time</title>
</head>
<body>
    <h1>Current Time</h1>
    <p>{current_time}</p>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)

# print(f"Updated time to {current_time}")
