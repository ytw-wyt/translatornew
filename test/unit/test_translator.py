from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    # is_english, translated_content = translate_content("This is an English message.")
    # assert is_english == True
    # assert translated_content == "This is an English message."
    english_posts = [
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
        {"post": "Can we meet at 3 PM tomorrow?", "expected_answer": (True, "Can we meet at 3 PM tomorrow?")}
    ]
    for post_data in english_posts:
        is_english, translated_content = translate_content(post_data["post"])
        assert is_english == post_data["expected_answer"][0]
        assert translated_content == post_data["expected_answer"][1]

    non_english_posts = [
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
    for post_data in non_english_posts:
        is_english, translated_content = translate_content(post_data["post"])
        assert is_english == post_data["expected_answer"][0]
        assert translated_content == post_data["expected_answer"][1]

def test_llm_gibberish_response():
    gibberish_posts = [
        {"post": "gibberish text not real words", "expected_answer": (False, "Invalid language.")},
        {"post": "1234567890", "expected_answer": (False, "Invalid language.")},
        {"post": "!@#$%^&*()", "expected_answer": (False, "Invalid language.")},
        {"post": "asdfghjkl;", "expected_answer": (False, "Invalid language.")},
        {"post": "👍👍👍👍👍👍👍", "expected_answer": (False, "Invalid language.")},
        {"post": "-------", "expected_answer": (False, "Invalid language.")}
    ]
    for post_data in gibberish_posts:
        is_english, translated_content = translate_content(post_data["post"])
        assert is_english == post_data["expected_answer"][0]
        assert translated_content == post_data["expected_answer"][1]