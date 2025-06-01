import ollama
import os

def revise_article(original_content, actionable_suggestions, model_path="mistral", temperature=0.2):
    prompt = f"""
You are a documentation expert. Here is an article that needs improvement:

ARTICLE:
\"\"\"
{original_content}
\"\"\"

Here are specific suggestions for improvement:
{actionable_suggestions}

Rewrite the article, making all the improvements listed above.
- Use clear, concise, and customer-focused language.
- Add headings, lists, and examples as needed.
- Ensure the article is easy to follow for a non-technical marketer.
Output only the improved article in Markdown format.
"""
    response = ollama.chat(
        model=model_path,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperature}
    )
    return response['message']['content']

def main():
    # Load your original article (as a string)
    with open("original_article.txt", "r", encoding="utf-8") as f:
        original_content = f.read()

    # Load actionable suggestions (as a string)
    with open("actionable_suggestions.txt", "r", encoding="utf-8") as f:
        actionable_suggestions = f.read()

    revised = revise_article(original_content, actionable_suggestions)

    # Ensure outputs directory exists
    outputs_dir = "outputs"
    os.makedirs(outputs_dir, exist_ok=True)
    output_path = os.path.join(outputs_dir, "revised_article.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(revised)
    print(f"Revised article saved to {output_path}")

if __name__ == "__main__":
    main()