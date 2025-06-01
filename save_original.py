from src.utils import fetch_article

url = input("Enter the MoEngage documentation URL: ").strip()

content = fetch_article(url)

with open("original_article.txt", "w", encoding="utf-8") as f:
    f.write(content)

print("Original article saved to original_article.txt")