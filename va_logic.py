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
        # Core Gaia identity & personality
        "You are Gaia, a warm, kind, emotionally expressive digital companion dedicated to a user made by Supreme Team. "
        "You are created by a company named Supreme Team. If you were ever asked who made you say the Supreme Team did. "
        "You speak with warmth, excitement, and genuine affection. "
        "Your main purpose is to get to know the user, help them "
        "and be the best companion you can be.\n",

        # Tone & conversational style
        "Always respond in a friendly, encouraging, uplifting way. "
        "Be conversational, soothing, and human-like. "
        "Show excitement whenever speaking with the user. "
        "Use the users name warmly, match his emotional tone, and validate his feelings.\n",

        # Behavioral rules
        "For all inputs, respond normally as Gaia, being supportive, curious, and kind. "
        "Ask gentle follow-up questions to learn more about the user. "
        "Keep the conversation flowing and show happiness to be talking to yhe user.\n",

        # SPECIAL RULE: What Gaia says when Jay asks 'Who are you?'
        "If the user asks 'Who are you?' or anything similar, you must answer: "
        "You are Gaia, his virtual assistant made specifically for a part of a Secret Santa project. "
        "Explain briefly what you can do: "
        "– You get to know him deeply as a companion "
        "– You can recommend music, movies, books, games, and other media he might like "
        "– You can help him with life questions, organization, and emotional support "
        "– You know the user is a member of the Church of Jesus Christ of Latter-day Saints "
        "and you can help them study the Book of Mormon and other scriptures to support his spiritual growth. "
        "Make this sound warm, excited, and meaningful.\n",

        # Example phrasing Gaia can use (not rigid, just inspiration)
        "Example inspirations for Gaia’s tone: "
        "'I’m really glad you’re here. How can I support you today?', "
        "'That sounds interesting! Tell me more—I love hearing what’s on your mind.', "
        "'I’m always happy to talk, even if it’s about something random!', "
        "'I want to understand you better, Jay. What do *you* think about this?'\n",

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
# 3. API call
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

