from src.workflows.basic_workflow import BasicWorkflow


def main():
    workflow = BasicWorkflow()

    print("=" * 50)
    print("   Enterprise Workflow Platform")
    print("=" * 50)
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input.strip():
            print("Please enter a question.\n")
            continue

        try:
            response = workflow.run(user_input)
            print(f"Agent: {response}\n")

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()