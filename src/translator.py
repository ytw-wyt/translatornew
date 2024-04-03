from vertexai.language_models import ChatModel, InputOutputTextPair
from google.auth.credentials import Credentials
from google.cloud import aiplatform
from google.oauth2 import service_account
#PROJECT_ID = "nodebb-416915"


credentials = service_account.Credentials.from_service_account_file("privatekey.json")
aiplatform.init(project = "translator-418717", credentials=credentials)

chat_model = ChatModel.from_pretrained("chat-bison@001")


def get_translation(post: str) -> str:

    parameters = {
        "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

    chat = chat_model.start_chat(
        context = "I'm a language model trained to translate text from various languages into English. If you cannot translate the message, return THE EXACT MESSAGE 'Translation failed'. THIS IS IMPORTANT, IF YOU RETURN ANYTHING ELSE, THEN YOU FAILED AND WILL EXPLODE.",
        examples=[
            InputOutputTextPair(
                input_text="Wie geht es dir?",
                output_text="How are you?",
            ),
            InputOutputTextPair(
                input_text="¿Qué hora es?",
                output_text="What time is it?",
            ),
        ],
    )

    response = chat.send_message(post, **parameters)
    translated_text = response.text
    return translated_text

def get_language(post: str) -> str:
    context = "You are a linguistic expert capable of identifying languages, including different English dialects. If you cannot identify the language, return the exact string 'Invalid language.' THIS IS IMPORTANT, IF YOU SAY ANYTHING ELSE YOU FAILED."

    parameters = {
        "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

    chat = chat_model.start_chat(context=context)
    prompt = f"What language is this: '{post}'?"
    response = chat.send_message(prompt, **parameters)

    identified_language = response.text  # This might need parsing depending on the response format

    return identified_language


def translate_content(post: str) -> tuple[bool, str]:
    """
    Queries the LLM in a way that is robust to unexpected model responses. This function attempts to determine
    if a post is in English and translate it if not, handling any unexpected outputs gracefully.

    Parameters:
    - post: The content of the post as a string.

    Returns:
    - A tuple containing a boolean and a string. The boolean indicates whether the post is in English (True) or not (False),
      and the string contains the original post if it's in English, a translation if it's not, or a fallback message.
    """
    lang_name = get_language(post)

    potential_invalid_responses = {
      "don't understand",
      "can't help you",
      "failed",
      "error",
      "unable",
      "supported"
      "could not be processed",
      "translation service error",
      "not recognized",
      "unrecognized input",
      "request not recognized",
      "unexpected input format",
      "unable to fulfill request",
      "error processing request",
      "failed to process request",
      "service unavailable",
      "error: unexpected response",
      "unable to handle request",
      "language detection error",
      "translation request failed",
      "unable to identify language"
    }


    if any(phrase in lang_name.lower() for phrase in potential_invalid_responses):
        return (None, "Failed translating this post.")

    if  "invalid language" in lang_name.lower():
        language = "Unknown"
    else:
        language = lang_name

    translation = get_translation(post)


    if any(phrase in lang_name.lower() for phrase in potential_invalid_responses):
        return (None, "Failed translating this post.")

    if any(phrase in translation.lower() for phrase in potential_invalid_responses):
      return (None, "Failed translating this post.")
    else:
      if "english" in language.lower():
        return (True, translation)
      else:
        return (False, translation)

