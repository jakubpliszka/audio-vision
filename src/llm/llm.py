import openai


class LLM:
    def __init__(self, model_id: str = "gpt-3.5-turbo") -> None:
        self.model_id = model_id
        self.conversation = [
            {"role": "system", "content": "Hello"}]  # initial message

    def chat(self, message: list) -> str:
        self.conversation.append({"role": "user", "content": message})

        # create a chat completion object
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=self.conversation
        )

        # get the response message
        response_message = response.choices[-1].message
        self.conversation.append(response_message)

        return response_message.content
