# MoEngage AI-Powered Documentation Improvement Agent

## 🚀 Overview

This project was built as part of a technical coding assignment. It aims to improve the clarity, usability, and accessibility of documentation articles from the MoEngage Help Center using AI.

The project features two intelligent agents:

---

## 🛠️ Features

### 🔹 Agent 1: Documentation Analyzer

- Accepts a MoEngage article URL as input.
- Uses Selenium and BeautifulSoup to scrape article content.
- Applies readability metrics (Flesch-Kincaid Grade, Flesch Reading Ease, Gunning Fog).
- Leverages an LLM (via Ollama, or optionally OpenAI) to generate a structured report.
- Outputs a Markdown report with assessments and actionable suggestions across:
  - Readability for marketers
  - Structure and flow
  - Completeness of content and examples
  - Style guidelines (based on Microsoft Style Guide)

### 🔹 Agent 2 (Bonus): Documentation Revision Agent

- Takes the original article and suggestions from Agent 1.
- Uses an LLM to revise the documentation automatically.
- Outputs a revised Markdown file with improved structure, clarity, and tone.

---

## 📁 Project Structure

```
moengage-doc-agent/
├── main.py                # Runs Agent 1 (analysis)
├── revise.py              # Runs Agent 2 (revision)
├── save_original.py       # Downloads original doc content
├── outputs/
│   ├── example_output_1.md      # Analysis output
│   ├── example_output_2.md      # Analysis output
│   └── revised_article_task2.md # Revised article
├── src/
│   ├── utils.py           # Web scraping logic
│   ├── analyzer.py        # LLM analysis logic
│   └── readability.py     # Calculates FK/Flesch/Gunning scores
├── requirements.txt       # Python dependencies
└── README.md              # You're reading it!
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.9+
- Chrome + ChromeDriver
- Ollama (for running local LLMs like mistral)

### Installation

```sh
pip install -r requirements.txt
```

### Selenium Setup

- ChromeDriver must be installed and added to PATH.
- Selenium is run in non-headless mode to bypass MoEngage’s "I'm not a robot" check.

### Ollama Setup (Optional: for local LLM)

```sh
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama run mistral
```

---

## ▶️ How to Run Each Agent

### 🔹 Run Agent 1 (Analyze an article)

```sh
python main.py
```
- Input the article URL when prompted.
- Input the filename to save the output.
- Output saved to: `outputs/example_output_1.md`

### 🔹 Run Agent 2 (Revise article)

```sh
python revise.py
```
- This script will load the original article and suggestions.
- Output saved to: `outputs/revised_article_task2.md`

### 🔹 Save the original content (Optional)

```sh
python save_original.py
```

---

## 📝 Example Output (Snippet)

```
## 1. Readability for Marketers
Assessment: The language is simple, but it lacks marketer-specific context.
Suggestions:
- Add use cases relevant to campaign managers.
- Define terms like "dashboard" or "event analytics".
```
See the full output in `outputs/example_output_1.md`.

---

## 🧠 Assumptions Made

- Marketers are the primary audience.
- Most MoEngage articles require basic readability and structural improvements.
- LLMs (like Mistral) can follow structured prompts to assess tone, clarity, and examples.
- Web scraping is allowed for this assignment since no API was provided.

---

## 💡 Design Choices & Approach

- Used Selenium to handle MoEngage's bot detection.
- Decoupled scraping, analysis, and revision into separate files.
- Used markdown format for human-friendly output.
- Used textstat for readability scoring.
- Structured prompts for LLMs for actionable, context-aware feedback.

---

## 🏔️ Challenges Faced & Solutions

| Challenge                     | Solution                                   |
|-------------------------------|--------------------------------------------|
| MoEngage’s bot protection     | Used Selenium in non-headless mode         |
| Inconsistent LLM responses    | Ran multiple LLM passes, picked best       |
| Avoiding generic suggestions  | Injected full article text into prompt     |
| Formatting output clearly     | Structured prompts + markdown output       |

---

### 🔹 Automatic Extraction of Actionable Suggestions

When you run `main.py`, the script will:
- Analyze the article and save the full report in the `outputs` folder.
- **Automatically extract actionable suggestions from the report and save them as `outputs/actionable_suggestions.txt`.**
- This file is then used directly by Agent 2 (`revise.py`) for the revision step.





