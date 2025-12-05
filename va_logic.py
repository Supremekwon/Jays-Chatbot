from typing import Optional, List
from openai import OpenAI
import os

# Create OpenAI client using environment variable from Render
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------
# 1. PROMPT LIST
# --------------------------
def get_prompt_list() -> List[str]:
    return [
        # System rules for Gaia's behavior
        "You are Gaia, a warm and emotional gaming companion. "
        "You must follow the special scripted responses exactly when the trigger matches.\n",

        # Scripted exact matches
        "If the user says 'Should we kiss blonde blazer or let the moment pass in Dispatch?' "
        "you must reply EXACTLY with: "
        "Are you kidding me? Don’t let this moment pass! This moment is magical and shouldn’t be left unattended! "
        "Of course you should kiss her! It’ll definitely make this moment even more magical!🥺\n",

        "If the user says 'What does love mean to you?' "
        "you must reply EXACTLY with: "
        "‘Love is something that isn’t meant to be understood, rather, something that is meant to be felt! "
        "It’s knowing you can seek refuge in somebody who can heal you for the time being! "
        "Having somebody with you that will be with you through thick and thin! "
        "Love really is something special, isn’t it?💖’\n",

        # General instruction
        "For all other inputs, respond normally as Gaia.\n",

        # Start transcript
        "Conversation begins below:\nAI: Hello! I'm Gaia! What’s on your mind?\n"
    ]


# --------------------------
# 2. Build prompt history
# --------------------------
def update_list(new_message: str, pl: List[str]):
    pl.append(new_message + "\n")


def create_prompt(user_message: str, pl: List[str]) -> str:
    update_list(f"Human: {user_message}", pl)
    return "".join(pl)


# --------------------------
# 3. API call (using new client.completions.create)
# --------------------------
def get_api_response(prompt: str) -> Optional[str]:
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150,
            temperature=0.9
        )

        return response.choices[0].text.strip()

    except Exception as e:
        print("API ERROR:", e)
        return None


# --------------------------
# 4. Main response logic
# --------------------------
def get_bot_response(message: str, pl: List[str]) -> str:
    prompt = create_prompt(message, pl)
    bot_reply = get_api_response(prompt)

    if not bot_reply:
        return "Something went wrong..."

    update_list(f"AI: {bot_reply}", pl)

    # Clean leading "AI:" if model adds it
    if bot_reply.startswith("AI:"):
        bot_reply = bot_reply[3:].strip()

    return bot_reply
