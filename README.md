# 🚀 Focused-Resume: AI-Powered CV Matcher

**Focused-Resume** is a high-performance, serverless application designed to bridge the gap between static resumes and dynamic job descriptions. By leveraging **Named Entity Recognition (NER)** and specialized NLP models, it transforms unstructured PDF data into actionable insights, calculating real-time compatibility scores.

---

## 🔍 Problem Definition

Traditional recruitment processes suffer from "keyword fatigue." Applicants often fail to pass initial screenings because their resumes aren't formatted for legacy ATS (Applicant Tracking Systems), while hiring managers struggle to manually parse through hundreds of PDFs to find specific technical competencies hidden in varied layouts. Furthermore, static job descriptions on JavaScript-heavy sites make it difficult for automated tools to pull accurate requirements.

## 💡 The Solution

Focused-Resume solves this by providing a **Serverless AI-Engine** that:

- **Decodes Layouts:** Uses PDF parsing to "read" resumes, regardless of column structures.
- **Understands Context:** Employs Machine Learning to extract actual skills and technologies rather than just matching substrings.
- **Automates Research:** Dynamically scrapes modern job boards to fetch live requirements for instant comparison.
- **Quantifies Fit:** Provides a data-driven compatibility score to help candidates and recruiters focus on the best matches.

---

## 🛠 Tech Stack

- **Frontend:** React 18, Tailwind CSS, Vite
- **Backend:** Serverless (AWS Lambda / Azure Functions)
- **Environment Management:** Poetry
- **NLP & Processing:** spaCy, PyMuPDF (fitz), Playwright
- **Machine Learning Model:** [amjad-awad/skill-extractor](https://huggingface.co/amjad-awad/skill-extractor)

---

## 🧠 Core Technical Capabilities

### 1. High-Fidelity PDF Parsing

Instead of basic text scraping, the system utilizes **PyMuPDF (fitz)** to handle complex, multi-column resume layouts.

- **Layer Analysis:** Extracts text while preserving structural integrity and reading order.
- **Performance:** Highly optimized for low-latency execution within constrained serverless environments.

### 2. Headless Scraping of JS-Generated Sites

Modern job boards (LinkedIn, Indeed, etc.) are often built with React or Next.js and do not serve static HTML. Focused-Resume uses **Playwright** to:

- **Dynamic Rendering:** Bypasses static limitations by fully rendering JavaScript before extraction.
- **Data Normalization:** Scrapes job requirements directly from a URL and cleanses "noisy" web data into structured text for the NLP engine.

### 3. Advanced NLP & Named Entity Recognition (NER)

The project moves beyond simple keyword matching. It employs a custom NLP pipeline to:

- **Entity Classification:** Distinguishes between **Tools** (e.g., Docker), **Languages** (e.g., Python), and **Frameworks** (e.g., React).
- **Contextual Awareness:** Uses **spaCy** to understand the relationship between terms, ensuring "Project Manager" isn't tagged as a "Java" skill just because the word appears nearby.

### 4. Machine Learning Integration

The heart of the matching engine is a transformer-based model hosted via Hugging Face.

- **Skill Extraction:** Leverages a fine-tuned model (`skill-extractor`) to identify niche technical competencies that standard dictionary-based scrapers miss.
- **Scoring Algorithm:** Implements a vector-based similarity check to provide a weighted compatibility score between the extracted CV entities and the scraped job description.

---

## 🏗 Project Structure

The project is built on a **Modular Serverless Architecture**, ensuring zero-cost idling and horizontal scalability:

```plaintext
├── frontend/             # React + Vite (State managed with Hooks/Context)
├── functions/            # Serverless Handlers (Python)
│   ├── parser/           # PyMuPDF logic
│   ├── scraper/          # Playwright/Headless Chromium
│   └── analyzer/         # spaCy + Hugging Face Inference
├── pyproject.toml        # Poetry managed dependencies
└── README.md             # Project documentation
```
