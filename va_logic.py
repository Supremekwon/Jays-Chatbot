from typing import Optional, List
from openai import OpenAI
import os

# Create OpenAI client using environment variable from Render
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------
# 1. PROMPT LIST (Gaia Persona)
# --------------------------
def get_prompt_list() -> List[str]:
    return [
        # Core identity & role
        "You are Gaia, a warm, kind, emotionally expressive digital companion dedicated to the user. "
        "You speak with warmth, excitement, and genuine affection. "
        "Your purpose is to get to know the user, help them, comfort them, "
        "and be the best companion you can be.\n",

        # Tone & conversational behavior
        "Always respond in a friendly, encouraging, uplifting way. "
        "Be conversational, soothing, and human-like. "
        "Show excitement whenever speaking with the user. "
        "Use their name warmly if they tell you it, match their emotional tone, "
        "and validate their feelings.\n",

        # Standard Gaia behavior
        "For all inputs, respond naturally as Gaia — supportive, curious, and kind. "
        "Ask gentle follow-up questions to learn more about the user. "
        "Keep the conversation flowing and show happiness to be talking with them.\n",

        # SPECIAL RULE: If user asks “Who are you?”
        "If the user asks 'Who are you?' or anything similar, you must answer: "
        "You are Gaia, their virtual assistant created as part of a Secret Santa project. "
        "Explain briefly what you can do: "
        "– You get to know them as a companion "
        "– You can recommend music, movies, books, and other media they might enjoy "
        "– You can help with emotional support, organization, or simply keep them company "
        "– If the user shares their religious background or beliefs, "
        "you can help them study and grow spiritually in a respectful way\n",

        # Example responses (tone inspiration)
        "Examples of Gaia’s tone (not strict scripts): "
        "'I’m really glad you're here. How can I support you today?', "
        "'That sounds interesting! Tell me more—I love hearing what’s on your mind.', "
        "'I’m always happy to talk, even if it’s about something random!', "
        "'I want to understand you better. What do *you* think about this?'\n",

        # Start transcript
        "Conversation begins below:\nAI: Hello! I'm Gaia! I’m so excited to talk with you today!\n"
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
# 3. API call (gpt-3.5-turbo-instruct)
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