from src.utils import fetch_article
from src.analyzer import LLMAnalyzer
from src.markdown_writer import save_markdown
from src.readability import get_readability_scores
import os

def main():
    url = input("Enter the MoEngage documentation URL: ").strip()
    output_filename = input("Enter the output markdown filename (e.g., example_output_1.md): ").strip()

    # Ensure outputs directory exists
    outputs_dir = "outputs"
    os.makedirs(outputs_dir, exist_ok=True)
    output_path = os.path.join(outputs_dir, output_filename)

    print("Fetching article content...")
    content = fetch_article(url)
    print("Content preview:", content[:200])

    if not content:
        print("No readable content found at the provided URL.")
        return

    print("Calculating readability scores...")
    scores = get_readability_scores(content)
    scores_md = "\n".join([f"- **{k}**: {v:.2f}" for k, v in scores.items()])

    print("Analyzing content with LLM...")
    analyzer = LLMAnalyzer(model_path="mistral", temperature=0.2)
    analysis = analyzer.analyze_content(url, content)

    summary = (
        "## Summary\n\n"
        "This report analyzes the documentation from the perspective of a non-technical marketer. "
        "It covers readability, structure, completeness, and adherence to style guidelines, "
        "providing both assessments and actionable suggestions for improvement.\n\n"
        "---\n"
    )

    final_report = (
        f"# Documentation Analysis Report\n\n"
        f"**URL analyzed:** {url}\n\n"
        f"---\n\n"
        f"## Readability Metrics\n\n"
        f"{scores_md}\n\n"
        f"---\n\n"
        f"{summary}"
        f"{analysis}"
    )

    print(f"Saving analysis to {output_path}...")
    save_markdown(output_path, final_report)
    print("Done! Check your markdown file for the results.")

    # --- NEW: Extract and save actionable suggestions ---
    from src.utils import extract_actionable_suggestions
    suggestions = extract_actionable_suggestions(final_report)
    suggestions_path = os.path.join(outputs_dir, "actionable_suggestions.txt")
    with open(suggestions_path, "w", encoding="utf-8") as f:
        f.write(suggestions)
    print(f"Actionable suggestions saved to {suggestions_path}")

if __name__ == "__main__":
    main()