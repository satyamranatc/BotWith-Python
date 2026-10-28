"""Vocabulary, conversational triggers, and response pools for the bot."""

# ==============================================================================
# INPUT TRIGGERS (Phrases spoken by the user)
# ==============================================================================

# General Greetings
GREETINGS = [
    "hi",
    "hello",
    "hey",
    "hey there",
    "namaste",
    "what's up",
    "whats up",
    "greetings",
    "good to see you",
    "hola",
    "yo",
]

# Time of Day Wishes
DAY_WISHES = [
    "good morning",
    "good afternoon",
    "good evening",
    "good night",
]

# Health & Status Inquiries
STATUS_INQUIRIES = [
    "how are you",
    "how are you doing",
    "how is it going",
    "how's it going",
    "how do you do",
    "are you there",
    "are you ready",
]

# Identity & Capabilities
IDENTITY_INQUIRIES = [
    "who are you",
    "what is your name",
    "what are you",
    "who made you",
    "who created you",
    "tell me about yourself",
    "what can you do",
    "help",
    "commands",
]

# Appreciation & Thanks
GRATITUDE = [
    "thank you",
    "thanks",
    "thanks a lot",
    "thank you so much",
    "appreciate it",
    "good job",
    "well done",
]

# Affirmations & Confirmations
AFFIRMATIONS = [
    "yes",
    "yeah",
    "yep",
    "sure",
    "ok",
    "okay",
    "alright",
    "correct",
    "got it",
]

# Exit & Termination Commands
EXIT_COMMANDS = [
    "bye",
    "goodbye",
    "exit",
    "quit",
    "stop",
    "shut down",
    "sleep",
    "see you later",
    "close",
    "terminate",
    "go away",
]

# User Honorifics / Titles
TITLES = [
    "Boss",
    "Sir",
]


# ==============================================================================
# BOT RESPONSES (Spoken back to the user)
# ==============================================================================

GREETING_RESPONSES = [
    "Hello Boss, how can I help you today?",
    "Hey Boss! Ready for your command.",
    "Greetings Boss. What are we working on?",
    "Namaste Boss, how may I assist you?",
    "Hello! Always ready to assist.",
]

STATUS_RESPONSES = [
    "I am doing great, Boss! How are you?",
    "All systems are running smoothly! What's on your mind?",
    "Operating at 100% capacity and ready to assist!",
    "Doing well, thank you for asking, Boss!",
]

IDENTITY_RESPONSES = [
    "I am your personal AI assistant, built to help you automate tasks.",
    "I'm your assistant Bot. Ready to follow your instructions, Boss!",
]

HELP_RESPONSES = [
    "I can listen to your voice commands, greet you, create folders, run apps, and edit files in your playground.",
    "You can ask me to create files, make folders, check in, or say goodbye to shut down.",
]

GRATITUDE_RESPONSES = [
    "You're very welcome, Boss!",
    "Glad to be of service!",
    "Anytime, Boss!",
    "My pleasure!",
]

FAREWELL_RESPONSES = [
    "Goodbye Boss! Have a productive day.",
    "Shutting down voice system. Catch you later, Boss!",
    "See you soon! Take care.",
]

FALLBACK_RESPONSES = [
    "I didn't quite catch that. Could you repeat?",
    "I don't understand that command yet, Boss.",
    "Could you please say that one more time?",
]



