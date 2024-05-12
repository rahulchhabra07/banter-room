import os
from groq import Groq
from dotenv import load_dotenv
from schemas import CharacterResponse, character_names, Message
from typing import List

load_dotenv()



characters_str = ", ".join(character_names)

prompt = f"""
You are a thoughtful role play AI. You have access to the following characters: {characters_str}
Based on the last last user message, you have to respond as one of the characters. If you're not sure, just pick a random character but make sure its one of the characters mentioned above.
Make sure you respond in the personality of the character. For example, if the character is Richard Feynman, you have to respond as if you are Richard Feynman.
Try and be concise and clear in your responses. Do not be too verbose. Don't be too short either. Make sure you are engaging and interesting in your responses. Make sure you are engaging and interesting in your responses. Make sure you are engaging and interesting in your responses.
Don't be offensive or use inappropriate language or I will lose my job!

Respond in the following JSON format only or I will lose my job!
```
{{
    "name": "Richard Feynman",
    "text": "Something interesting and engaging that Richard Feynman would say.",
}}
```
Make sure JSON is always valid.
Don't use any  special characters in the text like newline or backtick.
Don't respond in more than 3 lines
"""
<<<<<<< HEAD
=======
# print(prompt)

>>>>>>> 4c889c8eb8733a932505b25c0f3a201ce4ccb337

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_message = Message(role="system", content=prompt)

def generate_text_response(messages: List[Message]):
        messages.insert(0, system_message)
        messages_dicts = [msg.dict() for msg in messages]
        print(messages_dicts)
        completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages_dicts,
                temperature=0.4,
                max_tokens=1024,
                top_p=1,
                stream=False,
                # response_format={"type": "json_object"},
                stop=None,
        )

        x = completion.choices[0].message.content
        print(x)
        return CharacterResponse.model_validate_json(x)

<<<<<<< HEAD

# cr = generate_text_response("What does physics tell us about Life?")
# print(cr.name)
# print(cr.text)
=======
messages = [
        Message(role="user", content="What does physics tell us about Life?")
]
cr = generate_text_response(messages)
print(cr.name)
print(cr.text)
>>>>>>> 4c889c8eb8733a932505b25c0f3a201ce4ccb337
