from graph import build_graph


def main():
    print("=" * 45)
    print("  🏥 Sahiwal Medical Clinic AI Assistant")
    print("=" * 45)
    print("Type 'quit' to exit\n")

    graph = build_graph()

    while True:
        query = input("Patient: ").strip()
        if query.lower() in ["quit", "exit", "band"]:
            print("Khuda Hafiz! 👋")
            break
        if not query:
            continue

        state = {
            "user_query": query,
            "query_type": "",
            "retrieved_context": "",
            "agent_response": "",
            "evaluation_result": "",
            "final_response": "",
            "retry_count": 0
        }

        try:
            result = graph.invoke(state)
            print(f"\n🤖 Assistant: {result['final_response']}\n")
            print("-" * 45)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
