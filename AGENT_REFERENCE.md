# 🤖 Agent Quick Reference Guide

## Agent Architecture Pattern

All agents follow this pattern:

```python
from agents.base_agent import BaseAgent
from typing import Any, Dict

class MyAgent(BaseAgent):
    def __init__(self):
        system_prompt = "Your role and instructions..."
        super().__init__(name="MyAgent", system_prompt=system_prompt)
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """LangGraph interface - update and return state"""
        query = state.get("user_query", "")
        
        # Process query
        result = self._process(query)
        
        # Update state
        state["agent_response"] = result
        return state
    
    def _process(self, query: str) -> str:
        """Your specific logic"""
        return self.run(query)
```

---

## Agent Roles & Responsibilities

### 1️⃣ **RouterAgent**
**Purpose:** Classify incoming queries

```python
Input Query:  "How to treat fever?"
  ↓
RouterAgent.invoke()
  ↓
Output: state["query_type"] = "rag"
```

**Key Methods:**
- `invoke(state)` - Main interface
- `_classify_with_llm(query)` - AI classification
- `_classify_with_keywords(query)` - Keyword fallback

**Output:** `state["query_type"]` = "rag" or "general"

---

### 2️⃣ **RAGAgent** 
**Purpose:** Answer medical questions using knowledge base

```python
Input: query="Fever symptoms?"
  ↓
retrieve(query)  → Search FAISS for context
  ↓
generate(query, context)  → Generate response with context
  ↓
Output: state["agent_response"] = "Answer based on medical KB"
```

**Key Methods:**
- `invoke(state)` - Main interface
- `retrieve(query)` - Search knowledge base (FAISS)
- `generate(query, context)` - Generate response

**Output:** 
- `state["retrieved_context"]` - Context from KB
- `state["agent_response"]` - Generated response

---

### 3️⃣ **GeneralAgent**
**Purpose:** Handle non-medical queries and general chat

```python
Input: query="What are your clinic hours?"
  ↓
respond(query)
  ↓
_handle_clinic_query() or self.run(query)
  ↓
Output: state["agent_response"] = "Clinic information or general response"
```

**Key Methods:**
- `invoke(state)` - Main interface
- `respond(query)` - Generate response
- `_handle_clinic_query(query)` - Special clinic Q&A

**Output:** `state["agent_response"]` - General response

---

### 4️⃣ **EvaluatorAgent**
**Purpose:** Quality check responses

```python
Input: response="Generated response text"
  ↓
check(response)
  ↓
_quick_check_fail()  → Fast hardcoded checks
  ↓
If passed: use LLM for detailed evaluation
  ↓
Output: state["evaluation_result"] = "pass" or "fail"
```

**Key Methods:**
- `invoke(state)` - Main interface
- `check(response)` - Evaluate quality
- `_quick_check_fail(response)` - Quick validation

**Output:** `state["evaluation_result"]` - "pass" or "fail"

---

## LangGraph State Interface

All agents work with this State:

```python
class State(TypedDict):
    user_query: str              # ← Input from user
    query_type: str              # ← Set by RouterAgent
    retrieved_context: str       # ← Set by RAGAgent
    agent_response: str          # ← Set by RAG/General Agent
    evaluation_result: str       # ← Set by EvaluatorAgent
    final_response: str          # ← Set by EvaluatorAgent
    messages: List[BaseMessage]  # ← Conversation history
```

### State Flow in Graph

```
Entry: router_node
  ↓ (router.invoke(state))
  ├→ "rag": rag_node
  │        ↓ (rag.invoke(state))
  │        └→ evaluator_node
  │
  └→ "general": general_node
               ↓ (general.invoke(state))
               └→ evaluator_node
                   ↓ (evaluator.invoke(state))
                   └→ Exit
```

---

## Common Agent Patterns

### Pattern 1: Simple Query-Response

```python
def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
    query = state.get("user_query", "")
    response = self.run(query)
    state["agent_response"] = response
    return state
```

### Pattern 2: Query + Context Processing

```python
def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
    query = state.get("user_query", "")
    context = self._retrieve_context(query)
    response = self._generate_with_context(query, context)
    
    state["retrieved_context"] = context
    state["agent_response"] = response
    return state
```

### Pattern 3: Evaluation/Checking

```python
def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
    response = state.get("agent_response", "")
    result = self.check(response)
    
    state["evaluation_result"] = result
    if result == "fail":
        state["final_response"] = "Error message"
    else:
        state["final_response"] = response
    return state
```

---

## Testing Individual Agents

### Test RouterAgent
```python
from agents.router_agent import RouterAgent

router = RouterAgent()
state = {
    "user_query": "What medicine for cough?",
    "messages": [],
    "query_type": ""
}
result = router.invoke(state)
print(result["query_type"])  # Expected: "rag"
```

### Test RAGAgent
```python
from agents.rag_agent import RAGAgent
from langchain_groq import ChatGroq
from knowledge_base.kb import MedicalKnowledgeBase
import os

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"))
kb = MedicalKnowledgeBase()
kb.build_db("data/medical.txt")

rag = RAGAgent(llm, kb)
state = {
    "user_query": "Fever?",
    "messages": [],
    "retrieved_context": "",
    "agent_response": ""
}
result = rag.invoke(state)
print(result["agent_response"])
```

### Test GeneralAgent
```python
from agents.general_agent import GeneralAgent

general = GeneralAgent()
state = {
    "user_query": "What are your clinic hours?",
    "messages": [],
    "agent_response": ""
}
result = general.invoke(state)
print(result["agent_response"])
```

### Test EvaluatorAgent
```python
from agents.evaluator_agent import EvaluatorAgent

evaluator = EvaluatorAgent()
state = {
    "agent_response": "This is a helpful response about medical treatment.",
    "messages": [],
    "evaluation_result": ""
}
result = evaluator.invoke(state)
print(result["evaluation_result"])  # Expected: "pass"
```

---

## Error Handling Best Practices

### In Your Agent Methods

```python
def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
    try:
        query = state.get("user_query", "")
        result = self._process(query)
        state["agent_response"] = result
    except Exception as e:
        print(f"Error in {self.name}: {e}")
        state["agent_response"] = "Unable to process request"
    
    return state
```

### Always Return State

```python
# ✅ CORRECT
def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
    state["agent_response"] = self.run(state["user_query"])
    return state  # ← Must return state!

# ❌ WRONG
def invoke(self, state: Dict[str, Any]):
    return self.run(state["user_query"])  # ← Returns string, not state
```

---

## Security Checklist

✅ **DO:**
- Use `os.getenv("GROQ_API_KEY")` for API keys
- Store keys in `.env` file
- Validate keys exist before using
- Never hardcode API keys
- Add `.env` to `.gitignore`

❌ **DON'T:**
- Hardcode API keys in source code
- Commit `.env` to Git
- Log API keys
- Share `.env` files
- Use test keys in production

---

## Performance Tips

### 1. Use Keyword-Based Fallback
```python
# Fast classification without API call
def _classify_with_keywords(self, query: str) -> str:
    if any(kw in query.lower() for kw in ["fever", "pain", "medicine"]):
        return "rag"
    return "general"
```

### 2. Cache Knowledge Base
```python
# Build once, reuse many times
kb = MedicalKnowledgeBase()
kb.build_db("data/medical.txt")

rag = RAGAgent(llm, kb)  # Use same kb instance
```

### 3. Parallel Processing
```python
# Future enhancement: process multiple queries simultaneously
# Use asyncio or ThreadPoolExecutor
```

---

## Debugging Tips

### Print State at Each Step
```python
def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"\n[{self.name}] Input State:")
    print(f"  user_query: {state.get('user_query')}")
    
    # ... process ...
    
    print(f"\n[{self.name}] Output State:")
    print(f"  agent_response: {state.get('agent_response')}")
    
    return state
```

### Check Type of Messages
```python
from langchain_core.messages import BaseMessage
assert isinstance(state["messages"], list), "messages must be list"
assert all(isinstance(m, BaseMessage) for m in state["messages"])
```

---

## Adding New Agents

### Template for New Agent
```python
from agents.base_agent import BaseAgent
from typing import Any, Dict

class MyNewAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
Your instructions here.
What you do.
How you behave.
"""
        super().__init__(name="MyNewAgent", system_prompt=system_prompt)
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query = state.get("user_query", "")
        result = self._do_something(query)
        state["my_field"] = result
        return state
    
    def _do_something(self, query: str) -> str:
        # Your implementation
        return self.run(query)
```

### Register in graph.py
```python
from agents.my_new_agent import MyNewAgent

my_agent = MyNewAgent()

def my_node(state: State) -> State:
    return my_agent.invoke(state)

graph.add_node("my_node", my_node)
```

---

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Forgetting to return state | Always end with `return state` |
| Not initializing messages | Start with `messages: []` then use `BaseMessage` |
| Hardcoded API keys | Use `os.getenv("KEY")` from .env |
| Wrong state field names | Check TypedDict definition |
| Not inheriting BaseAgent | All agents must inherit from BaseAgent |
| Missing invoke() method | Every agent needs `invoke(state) -> state` |

---

**Reference maintained! 📖**

For more details, check IMPLEMENTATION_SUMMARY.md or SETUP_GUIDE.md.
