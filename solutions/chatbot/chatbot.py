from openai import OpenAI
from search_pages import Retriever
from embedding_search_pages import EmbeddingRetriever

INDEX_DIR = "index"
MODEL = "gpt-4.1-mini"

OPENAI_API_KEY = open('/home/ankit/Documents/personal/cloudx/jan2026_ml_dl_ankit/jan2026_ml_dl/solutions/openapi-key').read().strip()
client = OpenAI(api_key=OPENAI_API_KEY)



class CreditCardChatbot:
    def __init__(self):
        #self.retriever = Retriever(INDEX_DIR)
        self.retriever = EmbeddingRetriever()
        self.history = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0

    def retrieve_context(self, user_question, top_k=5):
        #results = self.retriever.search(user_question, top_k=top_k)
        results, embedding_tokens = self.retriever.search(user_question, top_k=top_k)

        context_parts = []

        for i, result in enumerate(results, start=1):
            context_parts.append(
                f"""
DOCUMENT {i}
Page Name: {result["page_name"]}
Similarity Score: {round(result["score"], 4)}

{result["chunk_text"]}
"""
            )

        return "\n\n".join(context_parts), embedding_tokens

    def build_prompt(self, user_question, context):
        history_text = ""

        for message in self.history[-6:]:
            history_text += f'{message["role"].upper()}: {message["content"]}\n'

        prompt = f"""
You are an ICICI Bank credit card assistant.

Your job:
1. Help the user understand and apply for ICICI credit cards.
2. Use ONLY the provided context documents.
3. If the user wants to apply, ask the next required eligibility question.
4. Ask only ONE question at a time.
5. Do not invent eligibility rules.
6. If required information is not present in the context, say that it is not available in the provided documents.
7. Keep answers short and conversational.

Possible eligibility details may include:
- age
- income or salary
- employment type
- credit score
- existing ICICI relationship
- documents required
- city or residence
- card preference such as cashback, travel, fuel, rewards

Conversation so far:
{history_text}

Retrieved context:
{context}

Current user message:
{user_question}
"""
        return prompt

    def ask_llm(self, prompt):
        response = client.responses.create(
            model=MODEL,
            input=prompt
        )

        return (
            response.output_text,
            response.usage.input_tokens,
            response.usage.output_tokens,
            response.usage.total_tokens,
        )

    def chat(self):
        print("ICICI Credit Card Chatbot")
        print("Type 'exit' to stop.\n")

        while True:
            user_question = input("You: ")

            if user_question.lower() in ["exit", "quit"]:
                break

            #context = self.retrieve_context(user_question, top_k=2)
            context, embedding_tokens = self.retrieve_context(user_question, top_k=2)
            prompt = self.build_prompt(user_question, context)

            answer, input_tokens, output_tokens, total_tokens = self.ask_llm(prompt)

            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.total_tokens += total_tokens

            self.history.append({
                "role": "user",
                "content": user_question
            })

            self.history.append({
                "role": "assistant",
                "content": answer
            })

            print("\nBot:", answer)

            print("\n------ Token Usage ------")
            print(f"This call:")
            print(f"  Input Tokens : {input_tokens}")
            print(f"  Output Tokens: {output_tokens}")
            print(f"  Total Tokens : {total_tokens}")

            print("\nOverall:")
            print(f"  Input Tokens : {self.total_input_tokens}")
            print(f"  Output Tokens: {self.total_output_tokens}")
            print(f"  Total Tokens : {self.total_tokens}")
            print("-------------------------\n")


if __name__ == "__main__":
    bot = CreditCardChatbot()
    bot.chat()