import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "5Itauod8y2VYwMU89tTY5A", "isbns": "9781632168146"})
print(res.json())
