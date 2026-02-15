import requests

url = "http://localhost:8000/api/v1/opportunities/abeab5e4-7f21-4246-aa40-e7ad581d22b3/apply"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyOTFmNmU5Yy0zYjU5LTRhYzQtYTYwYi0zMGIxZTFlMTRiMzciLCJlbWFpbCI6InN0dWRlbnQyQHN0dWRlbnRzLmlpdG1hbmRpLmFjLmluIiwicm9sZSI6IlNUVURFTlQiLCJleHAiOjE3NzExNTgzMzd9.9uLUkJjrG6QXd0uOXA_lL9ws1IH7kOXY5tInmV61AOQ",
    "Content-Type": "application/json"
}
data = {
    "cover_letter": "I am interested in this opportunity."
}

try:
    print(f"Sending POST request to {url}")
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
