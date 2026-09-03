# 🎓 College AI Assistant

An AI-powered College Assistant that helps students get answers to their college-related questions using **Retrieval-Augmented Generation (RAG)**.

The application retrieves relevant information from uploaded college documents and uses the **Llama 3.2 AI model through Ollama** to generate clear, context-based answers.

---

## 🚀 Project Overview

Students often need information about academics, examinations, fees, placements, hostel facilities, college policies, and other college-related topics.

Searching through multiple documents can be time-consuming.

The **College AI Assistant** solves this problem by allowing students to ask questions in natural language.

The system:

1. Accepts a student's question.
2. Searches the uploaded college documents.
3. Retrieves the most relevant information.
4. Sends the retrieved context to an AI model.
5. Generates a clear and concise answer.
6. Displays the answer through a simple web interface.

This project uses a **Retrieval-Augmented Generation (RAG)** approach to reduce hallucinations and ensure that answers are based on the available documents.

---

## ✨ Features

### 👨‍🎓 Student Features

- 💬 Ask questions using natural language
- 🤖 AI-generated answers
- 📚 Answers based on uploaded college documents
- 🔎 Semantic document search
- ⚡ Fast question-answering interface
- 🖥️ Simple and user-friendly web interface

Students can ask questions related to:

- Academic information
- Examinations
- Fees
- Hostel
- Placements
- College policies
- Courses
- Rules and regulations
- Other information available in college documents

---

### 👨‍💼 Admin Features

The application also provides an admin section for managing college documents.

Admin functionality includes:

- 🔐 Admin login
- 📄 Upload PDF documents
- 📚 View uploaded documents
- 🚪 Admin logout
- 🗂️ Manage the documents used by the AI assistant

---

## 🧠 How RAG Works

The project follows a Retrieval-Augmented Generation pipeline.

```text
             Student Question
                    │
                    ▼
          ┌──────────────────┐
          │   Flask Web App  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Semantic Search  │
          └────────┬─────────┘
                   │
                   ▼
        Relevant Document Chunks
                   │
                   ▼
          ┌──────────────────┐
          │   RAG Context    │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │   Llama 3.2      │
          │     Ollama       │
          └────────┬─────────┘
                   │
                   ▼
             AI Answer
                   │
                   ▼
             Student UI
