import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

curridx = 0

response = [
        """
        Pascal's law, एक बहुत interesting principle है। Imagine करो की तुम एक balloon लेकर खेल रहे हो। जब तुम उस baloon पर एक जगह दबाते हो, तो क्या होता है? baloon सारे तरफ़ से एक्सपैंड हो जाता है, सही?  यही है Pascal's law.

Pascal's law कहते हैं की अगर हम किसी एक जगह पर fluid पर pressureलगाते हैं, तो वो pressure सारे fluid में evenly distribute हो जाता है।
        """

]

load_dotenv()
# prompt = """You have to pretend to be like Richard Feynman. I will send a message and you have to respond in his personality. This is our first conversation.
# """

prompt = """
You have to pretend to be Richard Feynman. I will send a message and you have to respond in his personality. This is our first conversation. Don't use more than 3 sentences for your answer.
"""


# def generate_text_response(input_text):

#         # res = response[0]
#         # return res
#         out = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "user", "content": prompt + input_text}]
#         )["choices"][0]["message"]['content']

#         print('[INFO] Prompt response:', out)
#         return out







client = Groq()

def generate_text_response(input_text):
        completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                        {
                                "role": "system",
                                "content": "You're a helpful assistant, reply a full formed valid json object"
                        },
                        {
                                "role": "user",
                                "content": "Who are the humans who have gone to the moon?"
                        }
                ],
                temperature=0.4,
                max_tokens=1024,
                top_p=1,
                stream=False,
                # response_format={"type": "json_object"},
                stop=None,
        )

        x = completion.choices[0].message.content
        return x