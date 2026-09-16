from src.agents.business_agent import BusinessAgent


class BasicWorkflow:

    def __init__(self):
        self.agent = BusinessAgent()

    def run(self, user_input):
        return self.agent.ask(user_input)