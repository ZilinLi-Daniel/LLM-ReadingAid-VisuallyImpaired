from openai import OpenAI

class NewsAgent:
    def __init__(self, api_key, base_url, model, messages=[]):
        self.client = OpenAI(api_key=api_key,base_url = base_url)
        self.model = model
        self.messages = messages

    def run(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        return response.choices[0].message.content

    def environmental_feedback(self, feedback):
        self.messages.append({
            'role': 'system',
            'content': feedback
        })

    def continue_conversation(self, user_input):
        self.messages.append({
            'role': 'user',
            'content': user_input
        })

        assistant_response = self.run()
        self.messages.append({
            'role': 'assistant',
            'content': assistant_response
        })

        return assistant_response