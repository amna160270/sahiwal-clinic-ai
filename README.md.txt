# 🏥 Sahiwal Clinic AI Assistant

## 📌 Overview
Sahiwal Clinic AI Assistant is a **Multi-Agent Medical AI System** built using **LangGraph + Agentic RAG + FAISS + Groq LLM**.

It intelligently processes medical queries and generates structured, safe, and contextual responses.

---

## 🚀 Key Features

- 🧠 Multi-Agent Architecture (Router, RAG, General, Evaluator)
- 🔗 LangGraph Workflow Orchestration
- 📚 Agentic RAG using FAISS Vector Database
- 🤖 LLM Integration (Groq API)
- 📄 Medical Knowledge Base Support
- 🧪 Query Evaluation System
- 💬 Interactive CLI Chat Interface

---

## 🧠 System Architecture

```mermaid
graph TD;
User[User Query] --> Router[Router Agent]
Router --> RAG[RAG Agent]
Router --> General[General Agent]
RAG --> Evaluator[Evaluator Agent]
General --> Evaluator
Evaluator --> Final[Final Response]