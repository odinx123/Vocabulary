from googletrans import Translator
import langid
import pyttsx3
import threading

lock = threading.Lock()

def dectect_lang(text):
    lang, _ = langid.classify(text)
    return lang

def translate_text(text):  # 回傳翻譯的語言
    detected_lang, _ = langid.classify(text)
    translator = Translator()
    if detected_lang == 'zh':
        translation = translator.translate(text, dest='en')
        lang = 'en'
    else:
        translation = translator.translate(text, dest='zh-TW')
        lang = 'zh'

    return translation.text, lang

def text_to_speech(text, lang, flag):
    lock.acquire(blocking=True)
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # 設置語速 (words per minute)
    engine.setProperty('volume', 1)  # 設置音量 (0.0 to 1.0)
    engine.setProperty('voice', engine.getProperty('voices')[not lang=='zh'].id)  # 男生聲音
    engine.say(text)
    engine.runAndWait()
    lock.release()
    flag.set()

if __name__ == '__main__':
    # print(dectect_lang('我'))

    text, lang = translate_text('rule of thumb')
    text_to_speech(text, lang)

    text, lang = translate_text('我很好')
    text_to_speech(text, lang)
