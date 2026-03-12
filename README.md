# CompanyVacationPolicy-RAG

A **Retrieval-Augmented Generation (RAG)** system that allows users to query company vacation policies and employee leave records. The system combines **PDF and Excel document loaders**, **vector embeddings with FAISS**, and an **LLM (Ollama)** to provide accurate answers based on company data.

---

## Features

- Load and index company vacation policies (PDF) and employee leave data (Excel)
- Split documents into chunks for better retrieval
- Use FAISS vector store for semantic search
- Query system via Python CLI or API
- Generates concise answers about:
  - Employee vacation days taken and remaining
  - Department and position
  - Company vacation policies
- Handles unknown employees gracefully
- Fully customizable prompt template for company-specific rules

---

## Tech Stack

- **Python 3.10+**
- **LangChain** – Document loading, splitting, and RAG chains
- **FAISS** – Vector database for document embeddings
- **Ollama LLM** – Large language model for response generation
- **Pandas** – For reading and processing Excel files
- **FastAPI (optional)** – Build a web interface or API for querying
- **HTML/CSS (optional)** – Frontend interface for users

----

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/CompanyVacationPolicy-RAG.git
cd CompanyVacationPolicy-RAG
