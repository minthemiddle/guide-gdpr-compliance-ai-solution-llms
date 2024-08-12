# Using Presidio for Privacy-Conscious LLM Integration: A Case Study for Product and Tech Leaders

As a European product or tech leader, you may be seeking ways to balance the potential of AI with stringent privacy regulations. This case study presents an approach to handle sensitive data while utilizing advanced AI capabilities.

## What You'll Learn

By the end of this case study, you'll understand:
1. How to use Presidio to anonymize sensitive data
2. How to safely interact with powerful LLMs like GPT-4
3. How to de-anonymize results within your secure environment

This approach enables the use of advanced AI while maintaining control over sensitive data, in line with GDPR requirements.

## Who This Case Study Is For

This case study is tailored for privacy-conscious tech leaders in Europe who want to:
- Implement advanced AI solutions
- Ensure compliance with GDPR and other privacy regulations
- Protect sensitive data while leveraging external AI services

## The Challenge: AI Power vs. Data Privacy

As a tech leader, you're likely aware of the potential applications of Large Language Models (LLMs) in areas such as:

- Summarizing legal documents
- Analyzing customer feedback
- Improving various business processes

However, using these models typically involves sending data to external servers, which can raise privacy concerns, particularly when handling Personally Identifiable Information (PII).

## The Solution: Presidio + LLMs

This case study proposes integrating Presidio, an open-source data protection and anonymization toolkit, with LLMs to create a system that:

1. Identifies and anonymizes PII in your data
2. Enables safer interaction with LLMs
3. De-anonymizes the results for internal use

Let's explore how this solution works and its potential benefits for privacy-conscious organizations.

## Detailed Technical Overview

### How It Works

Our solution operates in three key steps:

1. **PII Detection and Anonymization**
   - Presidio employs advanced NLP techniques (via `spacy`) to identify various types of PII in text data.
   - It then replaces this information with placeholders, ensuring sensitive data never leaves your secure environment.
2. **Safe LLM Interaction**
   - The anonymized text is sent to the latest frontier LLM (e.g., *GPT-4o-mini*) for processing.
   - With no real PII present, the risk of data exposure is minimized.
3. **Result De-anonymization**
   - The LLM's output, still containing placeholders, is de-anonymized by replacing the placeholders with the original PII.
   - This process occurs only within your secure environment, maintaining data privacy.

### Key Components

- **Presidio Analyzer**: Detects PII entities in text using predefined or custom recognizers.
- **Presidio Anonymizer**: Anonymizes detected PII entities.
- **Custom Recognizers**: Can be added for domain-specific PII types.
- **LLM Integration**: Seamless interaction with models like GPT-4o-min using anonymized data.

### Implementation Highlights

Here's a simplified code snippet to illustrate the process:

```python
# PII Detection and Anonymization
results = analyzer.analyze(text=text, language="en")
anonymized_text, pii_map = anonymizer.anonymize(text, results)

# LLM Interaction
response = llm_client.generate(anonymized_text)

# De-anonymization
final_result = de_anonymize_text(response, pii_map)
```

This code demonstrates the three main steps: anonymization, LLM interaction, and de-anonymization.

## Advantages and Limitations

### Advantages

1. **Privacy Compliance**: Maintains GDPR compliance and other privacy standards.
2. **Access to Best Models**: Utilizes the latest LLM models without compromising data security.
3. **Cost-Effective**: Eliminates the need for expensive on-premises LLM deployments.
4. **Scalability**: Easily scales with your data processing needs.
5. **Customizability**: Can be tailored to recognize industry-specific PII types.

### Limitations

1. **Dependency on External LLMs**: Still relies on third-party AI services.
2. **Potential for Missed PII**: While highly accurate, no system is 100% foolproof in PII detection, especially for non-English languages.
3. **Context Loss**: Some nuances might be lost in the anonymization process.
4. **Processing Overhead**: Adds an extra layer of processing compared to direct LLM use.

## Comparison with Local LLM Deployment

While hosting open-source LLMs like Llama 3.1 locally offers complete data control, it comes with significant challenges:

- High infrastructure costs
- Requires specialized ML engineering expertise
- Ongoing maintenance and updates
- Potentially lower performance compared to state-of-the-art commercial models

In contrast, the Presidio + LLM approach offers a more accessible, cost-effective, and immediately implementable solution for most businesses.

## Conclusion: Balancing Innovation and Privacy

For privacy-conscious European tech leaders, the combination of Presidio and LLMs offers a practical approach to utilizing AI capabilities while adhering to data protection standards. This solution:

- Aims to balance innovation and compliance
- Can help businesses remain competitive in the evolving AI landscape
- Supports data privacy principles

Adopting this approach can demonstrate your company's commitment to responsible AI use, balancing technological advancement with ethical data handling – an important consideration in the privacy-focused European market.

## Deep Dive: Understanding the Implementation

Let's take a closer look at the implementation in `main.py` (Link to the full code), breaking down each step and explaining its purpose and technical details.

### 1. Setting Up the Environment

```python
import spacy
import re
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
from typing import Dict, List
from openai import OpenAI
import json
from pydantic import BaseModel

nlp = spacy.load("en_core_web_md")
```

This section imports necessary libraries and loads the spaCy model. spaCy is used for advanced NLP tasks, while Presidio provides the core PII detection and anonymization functionality. The OpenAI library is used to interact with the LLM.

### 2. Initializing Presidio Components

```python
registry = RecognizerRegistry()
registry.load_predefined_recognizers()

company_regex = r"\b[A-Z][a-z]+\s(?:Limited|Ltd|Plc|LLP|LP|Corporation|Inc\.|Incorporated)\b"

company_recognizer = PatternRecognizer(
    supported_entity="COMPANY",
    name="company_recognizer",
    patterns=[
        Pattern(
            name="company",
            regex=company_regex,
            score=0.7
        )
    ]
)
registry.add_recognizer(company_recognizer)

analyzer = AnalyzerEngine(registry=registry)
anonymizer = AnonymizerEngine()
```

Here, we set up the Presidio components. We create a custom recognizer for company names using a regex pattern and add it to the registry. This allows Presidio to identify and anonymize company names in addition to its predefined PII types.

### 3. Loading a Sample Legal Case

Before we can anonymize the text, we need to load a sample legal case. In a real-world scenario, this might come from a database or user input. For our example, we'll use a hardcoded string:

```python
legal_case = """
On 15th March 2023, John Smith, born on 10/05/1985, filed a complaint against XYZ Corporation. 
The plaintiff, residing at 123 Main St, London, can be reached at +44 20 1234 5678 or john.smith@email.com. 
His UK ID number is AB123456C. The case alleges breach of contract...
"""
```

This sample case contains various types of PII, including names, dates of birth, addresses, phone numbers, email addresses, and ID numbers. It will serve as our input for the anonymization process.

### 4. Anonymization Function

```python
def anonymize_text(text: str) -> tuple[str, Dict[str, str]]:
    results = analyzer.analyze(text=text, language="en")
    
    pii_map = {}
    for i, result in enumerate(results):
        placeholder = f"<{result.entity_type}_{i}>"
        original = text[result.start:result.end]
        pii_map[placeholder] = original
    
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"] and ent.text not in [v for v in pii_map.values()]:
            placeholder = f"<COMPANY_{len(pii_map)}>"
            pii_map[placeholder] = ent.text
    
    anonymized_text = text
    for placeholder, original in sorted(pii_map.items(), key=lambda x: len(x[1]), reverse=True):
        anonymized_text = anonymized_text.replace(original, placeholder)
    
    return anonymized_text, pii_map
```

This function is the core of our PII protection strategy. It performs these steps:
1. Uses Presidio's analyzer to identify PII in the text.
2. Creates a mapping between placeholders and original PII values.
3. Uses spaCy to identify additional entities (like organizations) that Presidio might have missed.
4. Replaces the original PII with placeholders in the text.

The function returns both the anonymized text and the PII mapping, which will be used later for de-anonymization.

### 4. LLM Integration

```python
client = OpenAI()

class LegalSummary(BaseModel):
    summary: str

completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Summarize this legal case in very short bullet points. Keep placeholders intact."},
        {"role": "user", "content": anonymized_case},
    ],
    response_format=LegalSummary,
)

summary = completion.choices[0].message.parsed.summary
```

This section demonstrates how to interact with the LLM (in this case, GPT-4o-mini) using the anonymized text. We use the OpenAI client to send a request to the model, asking it to summarize the anonymized legal case. The `LegalSummary` class defines the expected response format.

For more complex legal cases with consistent output criteria, you could define a more detailed schema. This approach allows for structured and consistent summaries across different cases. For example:

```python
class LegalCaseSummary(BaseModel):
    case_type: str
    plaintiff: str
    defendant: str
    filing_date: str
    key_allegations: List[str]
    relief_sought: str
    jurisdiction: str
    potential_precedents: List[str]
    estimated_case_duration: str
```

By using a more detailed schema like this, you ensure that the LLM provides specific information for each field, making it easier to process and analyze large numbers of legal cases consistently. This structured approach can be particularly useful for legal analytics, case management systems, or automated legal research tools.

### 5. De-anonymization Function

```python
def de_anonymize_text(text: str, pii_map: Dict[str, str]) -> str:
    for placeholder, original in pii_map.items():
        text = text.replace(placeholder, original)
    return text
```

This function reverses the anonymization process. It takes the anonymized text (in this case, the summary from the LLM) and the PII mapping, and replaces all placeholders with their original values.

### 6. Putting It All Together

```python
anonymized_case, pii_map = anonymize_text(legal_case)
final_summary = de_anonymize_text(summary, pii_map)

print("Anonymized case:")
print(anonymized_case)

print("\nSummary before de-anonymization:")
print(summary)

print("\nFinal Summary:")
print(final_summary)

print("\nPII Map:")
for placeholder, original in pii_map.items():
    print(f"{placeholder}: {original}")
```

This final section demonstrates the full workflow:
1. Anonymize the input text
2. Send the anonymized text to the LLM
3. De-anonymize the LLM's response
4. Print various stages of the process for debugging and verification

Here's the output from running our example:

```yaml 
# Output from running python3 main.py
# Line breaks changed slightly to make it more readable

Anonymous LLM content:
On <DATE_TIME_1>, <PERSON_2>, born on <DATE_TIME_3>, filed a complaint against <COMPANY_7>.
The plaintiff, residing at 123 <LOCATION_4>, <LOCATION_5>, can be reached at <PHONE_NUMBER_10> or <EMAIL_ADDRESS_0>.
His <LOCATION_6> ID number is <US_DRIVER_LICENSE_11>. The case alleges breach of contract...

Anonymized case:
On <DATE_TIME_1>, <PERSON_2>, born on <DATE_TIME_3>, filed a complaint against <COMPANY_7>.
The plaintiff, residing at 123 <LOCATION_4>, <LOCATION_5>, can be reached at <PHONE_NUMBER_10> or <EMAIL_ADDRESS_0>.
His <LOCATION_6> ID number is <US_DRIVER_LICENSE_11>. The case alleges breach of contract...

Summary before de-anonymization:
- On <DATE_TIME_1>, <PERSON_2> filed a complaint against <COMPANY_7>.
- Plaintiff's birth date: <DATE_TIME_3>.
- Residing at: 123 <LOCATION_4>, <LOCATION_5>.
- Contact info: <PHONE_NUMBER_10>, <EMAIL_ADDRESS_0>.
- Location ID: <US_DRIVER_LICENSE_11>.
- Allegation: breach of contract.

Final Summary:
- On 15th March 2023, John Smith filed a complaint against XYZ Corporation.
- Plaintiff's birth date: 10/05/1985.
- Residing at: 123 Main St, London.
- Contact info: +44 20 1234 5678, john.smith@email.com.
- Location ID: AB123456C.
- Allegation: breach of contract.

PII Map:
<EMAIL_ADDRESS_0>: john.smith@email.com
<DATE_TIME_1>: 15th March 2023
<PERSON_2>: John Smith
<DATE_TIME_3>: 10/05/1985
<LOCATION_4>: Main St
<LOCATION_5>: London
<LOCATION_6>: UK
<COMPANY_7>: XYZ Corporation
<URL_8>: john.sm
<URL_9>: email.com
<PHONE_NUMBER_10>: +44 20 1234 5678
<US_DRIVER_LICENSE_11>: AB123456C
```

By following this process, we ensure that no PII is sent to the external LLM service, while still leveraging its capabilities to process and summarize the information.

Remember, while this implementation provides a strong foundation for privacy-preserving AI integration, it's crucial to thoroughly test and validate the system with your specific use cases and data types. Always consult with legal and compliance teams to ensure adherence to relevant privacy regulations.
