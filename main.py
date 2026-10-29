import random
from skills import phrases, system_actions, voice

from skills.groQLLM import ask_groq

# Example voice fallback or query answering:


def main():
    voice.speak("Hello Boss, I am online and listening.")

    while True:
        user_said = voice.listen().strip()
        if not user_said:
            continue

        # Check for exit/shutdown commands
        if any(cmd in user_said for cmd in phrases.EXIT_COMMANDS):
            voice.speak(random.choice(phrases.FAREWELL_RESPONSES))
            break

        # Check for greetings
        # elif any(greet in user_said for greet in phrases.GREETINGS):
        #     voice.speak(random.choice(phrases.GREETING_RESPONSES))
        #
        # # Check for status questions
        # elif any(q in user_said for q in phrases.STATUS_INQUIRIES):
        #     voice.speak(random.choice(phrases.STATUS_RESPONSES))
        #
        # # Check for identity questions
        # elif any(q in user_said for q in phrases.IDENTITY_INQUIRIES):
        #     voice.speak(random.choice(phrases.IDENTITY_RESPONSES))
        #
        # # Check for appreciation / thanks
        # elif any(thanks in user_said for thanks in phrases.GRATITUDE):
        #     voice.speak(random.choice(phrases.GRATITUDE_RESPONSES))

        elif "use ai" in user_said:
            answer = ask_groq(user_said)
            voice.speak(answer)




if __name__ == "__main__":
    main()