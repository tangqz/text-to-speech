import tkinter as tk
import pyttsx3
from pathlib import Path
'''
import openai
from packaging import version
required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
from openai import OpenAI
from playsound import playsound
import os
'''
# 初始化引擎
engine = pyttsx3.init()
#client = OpenAI(api_key='')

# API/模块调用
def say_text_as_speech(text):
    engine.say(text)
    engine.runAndWait()
    '''
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=text
    )
    response.stream_to_file(speech_file_path)
    playsound(str(speech_file_path))
    os.remove(speech_file_path)
    '''

# 简单的文本处理，获取下一个句子
def get_next_sentence(content, start_index):
    # 支持中文句子结束的标点
    sentence_endings = ['。', '！', '？', ';', '；','，']
    end_index = start_index
    while end_index < len(content) and content[end_index] not in sentence_endings:
        end_index += 1
    return content[start_index:end_index+1]

# 主窗口类
class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.content = ''
        self.current_index = 0
		
        # 输入框
        self.text_input = tk.Text(self.root, height=10, width=50)
        self.text_input.pack()

        # 句子显示标签
        self.label_current = tk.Label(self.root, text='', font=('Arial', 12))
        self.label_current.pack()
        self.label_next = tk.Label(self.root, text='', font=('Arial', 12))
        self.label_next.pack()

        # 状态标签
        self.status_label = tk.Label(self.root, text='Ready', font=('Arial', 12))
        self.status_label.pack()

        # 播放按钮（以空格键触发代替）
        self.root.bind('<space>', self.play_next)

    # 空格键触发的功能
    def play_next(self, event=None):
        self.content = self.text_input.get("1.0", tk.END)
        next_sentence = get_next_sentence(self.content, self.current_index)
        if not next_sentence:
            self.status_label['text'] = '朗读完成.'
            return
        self.update_labels(next_sentence)
        say_text_as_speech(next_sentence)
        self.current_index += len(next_sentence)
        self.update_labels(next_sentence)

    def update_labels(self, current_sentence):
        self.label_current['text'] = '当前句: ' + current_sentence
        next_sentence = get_next_sentence(self.content, self.current_index)
        self.label_next['text'] = '下一句: ' + next_sentence

# 创建对象 运行
root = tk.Tk()
app = TextToSpeechApp(root)
root.mainloop()