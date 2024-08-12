import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
from typing import Dict, List
from openai import OpenAI
import json
from pydantic import BaseModel

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Sample legal case with PII
legal_case = """
On 15th March 2023, John Smith, born on 10/05/1985, filed a complaint against XYZ Corporation. 
The plaintiff, residing at 123 Main St, London, can be reached at +44 20 1234 5678 or john.smith@email.com. 
His UK ID number is AB123456C. The case alleges breach of contract...
"""

# Function to anonymize text
def anonymize_text(text: str) -> tuple[str, Dict[str, str]]:
    # Analyze text
    results = analyzer.analyze(text=text, language="en")
    
    # Anonymize text
    anonymized_text = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    ).text

    # Create mapping of anonymized to original values
    pii_map = {result.entity_type: text[result.start:result.end] for result in results}
    
    return anonymized_text, pii_map

# Anonymize the legal case
anonymized_case, pii_map = anonymize_text(legal_case)

# Initialize OpenAI client
client = OpenAI()

# Define response format
class LegalSummary(BaseModel):
    summary: str

# Send anonymized text to OpenAI LLM
completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Summarize this legal case in very short bullet points. Keep placeholders intact."},
        {"role": "user", "content": anonymized_case},
    ],
    response_format=LegalSummary,
)

# Extract summary from response
summary = completion.choices[0].message.parsed.summary
print(f"Summary: {summary}")

# Function to de-anonymize text
def de_anonymize_text(text: str, pii_map: Dict[str, str]) -> str:
    for placeholder, original in pii_map.items():
        text = text.replace(f"[{placeholder}]", original)
    return text

# De-anonymize the summary
final_summary = de_anonymize_text(summary, pii_map)

# Print the final summary with PII
print(f"Final Summary: {final_summary}")
