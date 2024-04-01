from src.translator import translate_content

def test_correct_return_type(mocker):
    mocker.patch("src.translator.translate_content", return_value=(False, "This is a Chinese message"))
    res = translate_content("这是一条中文消息")
    assert isinstance(res, tuple)
    assert len(res) == 2
    assert isinstance(res[0], bool)
    assert isinstance(res[1], str)

def test_lang_valid_input(mocker):
    mocker.patch("src.translator.translate_content", return_value=(False, "This is a Chinese message"))
    res = translate_conten("这是一条中文消息")
    assert res == (False, "This is a Chinese message")

    mocker.patch("src.translator.translate_content", return_value=(True, "This is an English message"))
    res = translate_content("这是一条英文消息")
    assert res == (True, "This is an English message")

def test_invalid_lang(mocker):
    mocker.patch("src.translator.translate_content", return_value=(None, "Failed translating this post"))
    res = translate_content("sdfgdsfadfd")
    assert res == (None, "Failed translating this post")

