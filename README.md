# Focused-Resume: AI-Powered CV Matcher 🚀

**Focused-Resume** is an automated resume screening and tagging application designed to streamline the hiring process. By leveraging Natural Language Processing (NLP), the system analyzes candidate CVs against job descriptions to extract key skills and calculate a compatibility score.

## 🛠 Tech Stack

- **Frontend:** React, Tailwind CSS, Vite
- **Backend:** Django, Django REST Framework (DRF)
- **Environment Management:** Poetry
- **NLP & Processing:** spaCy, PyMuPDF (fitz)

## 🌟 Key Features

- **Automated Skill Extraction:** Uses Named Entity Recognition (NER) to identify technical skills from PDF resumes.
- **Job Description Matching:** Compares extracted resume data with job requirements provided via URL or text.
- **Interactive Dashboard:** A React-based UI to view extracted skills as tags and see matching results.
- **PDF Parsing:** High-performance text extraction from PDF files using PyMuPDF.

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or 3.14
- Node.js & npm
- Poetry (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd focused-resume
   Setup Backend:
   ```

Bash
poetry install
poetry run python -m spacy download en_core_web_sm
Setup Frontend:

Bash
cd frontend
npm install
🏗 Project Structure
Plaintext
├── backend/ # Django project & DRF API
├── frontend/ # React + Vite application
├── pyproject.toml # Poetry dependencies & configuration
└── README.md # Project documentation
📝 Roadmap
[x] Initial Project Setup (Poetry, React, Django).

[ ] Integration of spaCy for NER Skill Extraction.

[ ] Implementation of PDF upload and parsing.

[ ] Scoring algorithm for Job-CV matching.
