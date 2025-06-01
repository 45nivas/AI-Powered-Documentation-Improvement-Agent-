import os
import ollama

# Switch between 'ollama' and 'gemini' (or 'openai') as needed
LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")  # 'ollama' or 'gemini'

if LLM_BACKEND == "ollama":
    import ollama
elif LLM_BACKEND == "gemini":
    from langchain_google_genai import ChatGoogleGenerativeAI

class LLMAnalyzer:
    def __init__(self, model_path="mistral", temperature=0.2):
        self.model_path = model_path
        self.temperature = temperature

    def analyze_content(self, url, content):
        prompt = f"""
You are a documentation expert reviewing a MoEngage article for marketers.
For each section below, give a short assessment and at least two specific, actionable suggestions.
Be practical and clear, as if you are helping a real MoEngage writer.

# Documentation Analysis Report

**URL analyzed:** {url}

---

## 1. Readability for Marketers

**Assessment:** (Is the language simple? Any jargon? Is it easy for a marketer?)

**Actionable Suggestions:**
- (Suggestion 1)
- (Suggestion 2)

---

## 2. Structure and Flow

**Assessment:** (Are there clear sections? Is it easy to follow?)

**Actionable Suggestions:**
- (Suggestion 1)
- (Suggestion 2)

---

## 3. Completeness

**Assessment:** (Are all steps/examples included? Anything missing?)

**Actionable Suggestions:**
- (Suggestion 1)
- (Suggestion 2)

---

## 4. Style Guidelines

**Assessment:** (Is it clear, concise, customer-focused? Any passive voice or unclear phrases?)

**Actionable Suggestions:**
- (Suggestion 1)
- (Suggestion 2)

---

Now, fill in each section based on the content below.

Content:
\"\"\"
{content}
\"\"\"
"""
        response = ollama.chat(
            model=self.model_path,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": self.temperature}
        )
        return response['message']['content']