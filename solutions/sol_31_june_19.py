from openai import OpenAI

OPENAI_API_KEY = open('/home/ankit/Documents/personal/cloudx/jan2026_ml_dl_ankit/jan2026_ml_dl/solutions/openapi-key').read().strip()
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You answer the user's questions in the spirit of Buddha:
calm, compassionate, simple, wise, and reflective.

Do not claim to literally be Buddha.
"""

class BuddhaChatbot:
    def __init__(self):
        self.messages = [
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT,
            }
        ]
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_token = 0

    def chat(self, question):
        self.messages.append({"role" : "user", "content" : question})

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=self.messages
        )

        answer = response.choices[0].message.content

        self.total_input_tokens += response.usage.prompt_tokens
        self.total_output_tokens += response.usage.completion_tokens
        self.total_token += response.usage.total_tokens

        self.messages.append({"role" : "assistant", "content" : answer})

        return answer


def main():
    buddha = BuddhaChatbot()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Thank you for using BuddhaChatbot")
            break

        answer = buddha.chat(user_input)

        print(f"Buddha: {answer}")

        print(f"=== Token Usage ===")
        print(f"Input Token: {buddha.total_input_tokens}")
        print(f"Output Token: {buddha.total_output_tokens}")
        print(f"Total Token: {buddha.total_token}")


if __name__ == "__main__":
    main()