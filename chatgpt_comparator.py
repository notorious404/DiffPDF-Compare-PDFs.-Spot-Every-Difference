import json
from typing import Dict, List, Any

# NEW SDK import
from openai import OpenAI

from config import MODEL_NAME, MAX_TOKENS, TEMPERATURE


class ChatGPTComparator:
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
    ):
        # IMPORTANT: no arguments here – it reads OPENAI_API_KEY from env
        self.client = OpenAI()
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def compare_pdfs(self, pdf_contents: Dict[str, str]) -> Dict[str, Any]:
        pdf_names = list(pdf_contents.keys())
        contents = [pdf_contents[name] for name in pdf_names]

        summaries = self._extract_summaries(contents, pdf_names)
        comparison = self._perform_detailed_comparison(summaries)
        insights = self._generate_insights(comparison, pdf_names)

        return {
            "pdf_names": pdf_names,
            "summaries": summaries,
            "comparison": comparison,
            "insights": insights,
        }

    def _extract_summaries(
        self, contents: List[str], names: List[str]
    ) -> Dict[str, str]:
        summaries: Dict[str, str] = {}

        for name, content in zip(names, contents):
            prompt = f"""
You are an analyst. Read this PDF content and output a structured JSON summary.

PDF name: {name}

Content (truncated):
\"\"\"{content[:8000]}\"\"\"

Return ONLY valid JSON, no extra text, with this structure:
{{
  "title": "Detected or inferred title",
  "key_points": ["bullet 1", "bullet 2"],
  "sections": {{"section name": "short summary"}},
  "word_count": <integer total words in content>
}}
"""
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            summaries[name] = response.choices[0].message.content.strip()

        return summaries

    def _perform_detailed_comparison(self, summaries: Dict[str, str]) -> Dict[str, Any]:
        docs_block = "\n\n".join(
            [f"Document: {name}\nSummary JSON: {summary}" for name, summary in summaries.items()]
        )

        comparison_prompt = f"""
You are comparing multiple documents.

Here are their summaries (JSON-like):
{docs_block}

Create a JSON object describing the comparison. Return ONLY valid JSON with:
{{
  "similarities": ["common aspect 1", "common aspect 2"],
  "differences": [
    {{
      "category": "what differs",
      "documents": {{
        "doc_name_1": "detail",
        "doc_name_2": "detail"
      }}
    }}
  ],
  "strengths_by_document": {{
    "doc_name_1": ["strength 1", "strength 2"],
    "doc_name_2": ["strength 1", "strength 2"]
  }},
  "overall_similarity_score": "0-100"
}}
"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": comparison_prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        raw = response.choices[0].message.content.strip()
        return {"raw_comparison": raw}

    def _generate_insights(self, comparison: Dict[str, Any], names: List[str]) -> Dict[str, str]:
        insights_prompt = f"""
You are a consultant. Based on this comparison JSON:

{comparison["raw_comparison"]}

Generate concise, actionable bullet-point insights for these documents:
{", ".join(names)}

Focus on:
- Key differences that matter
- When to use which document
- Any risks or gaps

Return plain text bullet points, no JSON.
"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": insights_prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        text = response.choices[0].message.content.strip()
        return {"insights": text}
