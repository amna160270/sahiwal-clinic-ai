from graph import app
from langchain_core.messages import HumanMessage

print("=============================================")
print("🏥 Sahiwal Clinic AI Assistant")
print("=============================================")
print("Type 'quit' to exit\n")

while True:
    query = input("Patient: ")

    if query.lower() == "quit":
        print("Allah Hafiz! 👋")
        break

    # Initialize state with proper types
    state = {
        "user_query": query,
        "query_type": "",
        "retrieved_context": "",
        "agent_response": "",
        "evaluation_result": "",
        "final_response": "",
        "messages": [HumanMessage(content=query)]  # Initialize with user query
    }

    try:
        result = app.invoke(state)

        print("\n--- DEBUG INFO ---")
        print(f"Type: {result['query_type']}")
        print(f"Evaluation: {result['evaluation_result']}")
        print("\n--- RESPONSE ---")
        print(f"Assistant: {result['final_response']}")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please try again.\n")
        print("--------------\n")

        print("AI:", result["final_response"])
        print("---------------------------------\n")

    except Exception as e:
        print("❌ Error:", str(e))
