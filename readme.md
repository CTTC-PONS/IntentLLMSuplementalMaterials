# Intent-Based Networking Dataset and Resources

This repository contains key resources to support the evaluation, testing, and explainability of an intent-based networking system within an SDN (Software-Defined Networking) environment. The materials cover performance measurement, dataset structure, sample intent requests, and pretrained linguistic variations for intent explanation.

## 📂 File Descriptions

### 🟢 `breakDownOfTimeResults.xls`
**Description:**  
This Excel file provides a detailed breakdown of the execution time results for the various stages of the intent processing pipeline.

**Contents:**  
- Time measurements for the following phases:
  - Parsing
  - Validation
  - Translation
  - Enforcement
- Statistical results across multiple test iterations for performance assessment.

**Purpose:**  
To analyze system efficiency and identify potential bottlenecks in the processing of intent requests.

---

### 🟠 `site.db`
**Description:**  
This Markdown document defines the structure of the dataset used for storing intents when establishing direct communication with the SDN controller.

**Contents:**  
- Field descriptions (e.g., intent ID, user ID, intent description, parameters, timestamps).
- Schema examples (JSON structure or database table format).
- Explanation of relationships between stored intents and network entities.

**Purpose:**  
To ensure clarity and consistency in how intents are recorded and accessed within the system.

---

### 🔵 `dynamoDBexamples.csv`
**Description:**  
This JSON file contains **seven sample intent request cases** that were generated directly by users. These examples represent common scenarios in the operation of the intent-based system.

**Contents:**  
- Realistic intent statements provided by users.
- Relevant parameters, such as:
  - Source and destination nodes
  - Bandwidth requirements
  - Priority levels
- Proper formatting for submission to the intent processing pipeline.

**Purpose:**  
To illustrate the variety of requests the system handles and to serve as input examples for testing and validation.

---

### 🟣 `sampleUtterances file.txt`
**Description:**  
The text files include a sample of utterances used as inputs for the LLM, aimed at covering a broad spectrum of linguistic variations.

**Contents:**  
- Example intents paired with corresponding explanation phrases.
- Multiple phrasings for similar intent types, enhancing linguistic diversity.
- Designed to improve natural language understanding and generation for user explanations.

**Purpose:**  
To support the development of explainability features by exposing the system to varied language patterns, improving its capacity to generate accurate and user-friendly intent explanations.

---

## ✅ Summary of Use

The files in this folder provide the following capabilities:
- Performance evaluation of intent handling workflows.
- Documentation of intent storage structure for SDN controllers.
- Testing with real-world intent requests.
- Training and validation of intent explanation mechanisms.

These resources are essential for analyzing, validating, and enhancing the performance and usability of intent-based networking solutions.

---
