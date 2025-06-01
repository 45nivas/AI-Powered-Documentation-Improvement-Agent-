def save_markdown(filename, markdown_text):
    if not filename.endswith(".md"):
        filename += ".md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_text)