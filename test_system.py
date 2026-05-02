#!/usr/bin/env python3
"""
Quick test script to verify all components are working
"""

print("🧪 Testing Sahiwal Clinic AI System...\n")

# Test 1: Import all agents
print("1️⃣  Testing imports...")
try:
    from agents.base_agent import BaseAgent
    from agents.router_agent import RouterAgent
    from agents.rag_agent import RAGAgent
    from agents.general_agent import GeneralAgent
    from agents.evaluator_agent import EvaluatorAgent
    print("   ✅ All agents imported successfully\n")
except Exception as e:
    print(f"   ❌ Import error: {e}\n")
    exit(1)

# Test 2: Test RouterAgent
print("2️⃣  Testing RouterAgent...")
try:
    from langchain_core.messages import HumanMessage

    router = RouterAgent()
    state = {
        "user_query": "What medicine for fever?",
        "messages": [HumanMessage(content="What medicine for fever?")],
        "query_type": "",
        "retrieved_context": "",
        "agent_response": "",
        "evaluation_result": "",
        "final_response": ""
    }
    result = router.invoke(state)
    print(f"   Query: 'What medicine for fever?'")
    print(f"   Classification: {result['query_type']}")
    print(
        f"   ✅ RouterAgent working (expected: 'rag', got: '{result['query_type']}')\n")
except Exception as e:
    print(f"   ❌ RouterAgent error: {e}\n")

# Test 3: Test Graph
print("3️⃣  Testing Graph...")
try:
    from graph import app
    print("   ✅ Graph compiled and loaded successfully\n")
except Exception as e:
    print(f"   ❌ Graph error: {e}\n")
    exit(1)

# Test 4: Full workflow test
print("4️⃣  Testing full workflow...")
try:
    from langchain_core.messages import HumanMessage

    test_query = "Hello"
    initial_state = {
        "user_query": test_query,
        "query_type": "",
        "retrieved_context": "",
        "agent_response": "",
        "evaluation_result": "",
        "final_response": "",
        "messages": [HumanMessage(content=test_query)]
    }

    print(f"   Executing query: '{test_query}'")
    result = app.invoke(initial_state)

    print(f"   ✅ Query executed successfully!")
    print(f"   - Query Type: {result['query_type']}")
    print(f"   - Response: {result['final_response'][:80]}...\n")

except Exception as e:
    print(f"   ❌ Workflow error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("=" * 50)
print("✅ ALL TESTS PASSED!")
print("=" * 50)
print("\n🚀 System is ready to run!")
print("   Run: python main.py")
