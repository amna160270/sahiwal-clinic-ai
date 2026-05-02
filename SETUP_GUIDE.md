# 🏥 Sahiwal Clinic AI - Setup & Configuration Guide

## 📋 Quick Start

### 1️⃣ **Environment Setup**
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_actual_key_here
```

### 2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Run the Application**
```bash
python main.py
```

---

## 🏗️ **Architecture Overview**

```
User Query
    ↓
[Router Agent] → Classifies as "rag" or "general"
    ↓
    ├→ "rag" → [RAG Agent] → Retrieves from Knowledge Base (FAISS)
    │
    └→ "general" → [General Agent] → Free-form conversation
    ↓
[Evaluator Agent] → Quality check
    ↓
Final Response
```

---

## 🤖 **Agent Hierarchy**

### **BaseAgent** (Base Class)
- Initializes LLM connection securely via environment variables
- Provides `invoke(state)` method for LangGraph compatibility
- Provides `run(message)` method for standalone usage

### **RouterAgent** (inherits BaseAgent)
- Classifies queries into "rag" or "general"
- Uses both LLM and keyword-based fallback classification
- Methods:
  - `invoke(state)` - LangGraph interface
  - `_classify_with_llm(query)` - AI classification
  - `_classify_with_keywords(query)` - Fallback

### **RAGAgent** (inherits BaseAgent)
- Retrieves medical information from knowledge base
- Methods:
  - `retrieve(query)` - Search FAISS index
  - `generate(query, context)` - Generate response with context

### **GeneralAgent** (inherits BaseAgent)
- Handles non-medical queries
- Methods:
  - `respond(query)` - Free-form response

### **EvaluatorAgent** (inherits BaseAgent)
- Quality checks agent responses
- Methods:
  - `check(response)` - Validate response quality

---

## 🔐 **Security Best Practices**

✅ **What's Fixed:**
- API keys now load from `.env` file (not hardcoded)
- Environment variables checked on startup
- Graceful error handling for missing keys

⚠️ **Next Steps:**
1. Create `.env` file from `.env.example`
2. Never commit `.env` to Git
3. Add `.env` to `.gitignore`

---

## 📝 **State Management**

Your LangGraph State structure:
```python
class State(TypedDict):
    user_query: str              # Original user question
    query_type: str              # "rag" or "general"
    retrieved_context: str       # Context from knowledge base
    agent_response: str          # Raw agent response
    evaluation_result: str       # Quality check result
    final_response: str          # Final response to user
    messages: List[BaseMessage]  # Conversation history
```

---

## 🧪 **Testing Individual Agents**

```python
# Test RouterAgent
from agents.router_agent import RouterAgent

router = RouterAgent()
state = {
    "user_query": "What medicine for fever?",
    "messages": [],
    "query_type": ""
}
result = router.invoke(state)
print(result["query_type"])  # Output: "rag"
```

---

## 🐛 **Troubleshooting**

### "GROQ_API_KEY not found"
- Check if `.env` file exists
- Verify key is set: `GROQ_API_KEY=your_key`
- Reload terminal after creating `.env`

### "Module not found" errors
- Ensure all agents inherit from BaseAgent
- Check import statements match file names
- Reinstall requirements: `pip install -r requirements.txt`

### Knowledge base not loading
- Check `data/medical.txt` exists
- Verify FAISS is installed: `pip install faiss-cpu`
- Check file permissions

---

## 📚 **Next Implementation Steps**

1. ✅ **BaseAgent & RouterAgent** - DONE
2. ⏳ **RAGAgent & EvaluatorAgent** - Make sure they inherit from BaseAgent
3. ⏳ **GeneralAgent** - Make sure it inherits from BaseAgent
4. ⏳ **Test full graph workflow**

---

## 📞 **Agent Method Signatures**

```python
# All agents follow this pattern:
class MyAgent(BaseAgent):
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Process state
        # Update state fields
        return state
```

---

**Happy coding! 🎉**
