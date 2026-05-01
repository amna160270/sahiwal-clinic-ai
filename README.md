🏥 Sahiwal Clinic AI Assistant 🤖

An AI-powered medical assistant built using a Multi-Agent System and Retrieval-Augmented Generation (RAG).

  🚀 Features
- Multi-Agent architecture (Router, RAG, Evaluator, General Agent)
- Medical knowledge base (Doctors, Medicines, FAQs)
- Retrieval-Augmented Generation (RAG)
- Intelligent response routing system
- Python-based backend chatbot

   🧠 How It Works

1. User enters a medical query  
2. Router Agent decides best agent  
3. RAG Agent searches medical knowledge base  
4. General Agent handles fallback responses  
5. Evaluator Agent checks response quality  

   📁 Project Structure
   
- agents/ → AI agent logic
- tools/ → RAG implementation tools
- knowledge_base/ → Medical dataset
- main.py → Entry point

   ⚙ Installation

```bash
pip install -r requirements.txt
