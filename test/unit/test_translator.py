from typing import Callable
import src.translator
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
from mock import patch

normal_eval_set = [
    # English posts
    {"post": "What time is it?", "expected_answer": (True, "What time is it?")},
    {"post": "This is a test post.", "expected_answer": (True, "This is a test post.")},
    {"post": "I am learning to code.", "expected_answer": (True, "I am learning to code.")},
    {"post": "Where is the nearest station?", "expected_answer": (True, "Where is the nearest station?")},
    {"post": "Can you recommend a good book?", "expected_answer": (True, "Can you recommend a good book?")},
    {"post": "How many languages do you speak?", "expected_answer": (True, "How many languages do you speak?")},
    {"post": "Life is beautiful.", "expected_answer": (True, "Life is beautiful.")},
    {"post": "Do you speak English?", "expected_answer": (True, "Do you speak English?")},
    {"post": "What is the meaning of life?", "expected_answer": (True, "What is the meaning of life?")},
    {"post": "Is there life on Mars?", "expected_answer": (True, "Is there life on Mars?")},
    {"post": "The quick brown fox jumps over the lazy dog.", "expected_answer": (True, "The quick brown fox jumps over the lazy dog.")},
    {"post": "I forgot my password.", "expected_answer": (True, "I forgot my password.")},
    {"post": "What's the weather like tomorrow?", "expected_answer": (True, "What's the weather like tomorrow?")},
    {"post": "I love learning new things.", "expected_answer": (True, "I love learning new things.")},
    {"post": "Can we meet at 3 PM tomorrow?", "expected_answer": (True, "Can we meet at 3 PM tomorrow?")},

    # Non-English posts
    {"post": "Aquí está su primer ejemplo.", "expected_answer": (False, "Here is your first example.")},
    {"post": "Wie geht es Ihnen heute?", "expected_answer": (False, "How are you today?")},
    {"post": "今天天气怎么样？", "expected_answer": (False, "What is the weather like today?")},
    {"post": "Qual è il tuo cibo preferito?", "expected_answer": (False, "What is your favorite food?")},
    {"post": "저는 오늘 매우 바빠요.", "expected_answer": (False, "I am very busy today.")},
    {"post": "¿Puedes ayudarme?", "expected_answer": (False, "Can you help me?")},
    {"post": "Это ваш первый пример.", "expected_answer": (False, "This is your first example.")},
    {"post": "Je ne comprends pas.", "expected_answer": (False, "I do not understand.")},
    {"post": "Il fait très froid aujourd'hui.", "expected_answer": (False, "It is very cold today.")},
    {"post": "這是一個測試。", "expected_answer": (False, "This is a test.")},
    {"post": "Ошибка в системе.", "expected_answer": (False, "There is a system error.")},
    {"post": "C'est la vie.", "expected_answer": (False, "That's life.")},
    {"post": "無意義的文字", "expected_answer": (False, "Meaningless text.")},
    {"post": "這本書值得一讀。", "expected_answer": (False, "This book is worth reading.")},
    {"post": "我今天很高興。", "expected_answer": (False, "I am very happy today.")},
    {"post": "Πού είναι η τουαλέτα;", "expected_answer": (False, "Where is the toilet?")}
]

gibberish_eval_set = [
    # Unintelligible or malformed posts
    {"post": "gibberish text not real words", "expected_answer": (False, "Invalid language.")},
    {"post": "1234567890", "expected_answer": (False, "Invalid language.")},
    {"post": "!@#$%^&*()", "expected_answer": (False, "Invalid language.")},
    {"post": "asdfghjkl;", "expected_answer": (False, "Invalid language.")},
    {"post": "👍👍👍👍👍👍👍", "expected_answer": (False, "Invalid language.")},
    {"post": "-------", "expected_answer": (False, "Invalid language.")}
]

def eval_single_response_complete(expected_answer: tuple[bool, str], llm_response: tuple[bool, str]) -> float:
    """
    Compares an LLM response to the expected answer from the evaluation dataset.

    First checks if both indicate the same language status (English or not). If they do,
    and if a translation is expected, evaluates the quality of the translation.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Check if the language status matches
    if expected_answer[0] != llm_response[0]:
        return 0.0  # Language mismatch

    # If both are English or both are not English and require translation
    if expected_answer[0]:  # If the post is in English
        # You might want to directly compare the strings or use another metric
        return 1.0  # Assuming the response matches the expectation
    else:
        # Evaluate the translation quality
        expected_translation = expected_answer[1]
        llm_translation = llm_response[1]

        # Generate embeddings for both the expected translation and the LLM's translation
        expected_embedding = model.encode([expected_translation])
        response_embedding = model.encode([llm_translation])

        # Calculate the cosine similarity between the two embeddings
        similarity_score = cosine_similarity(expected_embedding, response_embedding)

        return similarity_score[0][0]  # Extract and return the similarity score

def test_llm_normal_response():
  for test in normal_eval_set:
    @patch('src.translator.translate_content')
    def test_single_response(mocker):
        mocker.return_value = test["expected_answer"]
        llm_response = src.translator.translate_content(test["post"])
        assert eval_single_response_complete(test["expected_answer"], llm_response)>=0.99
    test_single_response()

def test_llm_gibberish_response():
  for test in gibberish_eval_set:
    with patch('src.translator.translate_content') as mocker:
        mocker.return_value = test["expected_answer"]
        llm_response = src.translator.translate_content(test["post"])
        assert eval_single_response_complete(test["expected_answer"], llm_response)>=0.99


