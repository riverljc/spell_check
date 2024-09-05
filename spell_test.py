# pip install audio_recorder_streamlit
# 載入套件
from openai import OpenAI
import random
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import time

client = OpenAI()

@st.cache_data
def get_question_list():
    # 讀取檔案
    with open('英文佳句座右銘.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        
        if len(line)<=0 or line == '\n': 
            continue
        
        clean_lines.append(line.split('.')[0]+'.<br>'+line.split('.')[1])
    
    return clean_lines

question_list = get_question_list()

# 建立畫面
# st.set_page_config(layout='wide')
st.title('英語測驗' + "📖")

# 測驗題目
placeholder = st.empty()

if 'key' not in st.session_state:
    question = random.choice(question_list)
    st.session_state.key = question
    placeholder.markdown(f'<span style="font-size: 24px;">{question}</span>', unsafe_allow_html=True)
    
audio_bytes = audio_recorder(pause_threshold=2.0)

tmp_audio_file = 'tmp.wav'

def filter_string(s):
    # 使用列表生成式過濾出英文字母和數字
    filtered = [char for char in s if char.isalnum()]
    # 將列表轉換回字串
    return ''.join(filtered)

if audio_bytes:    
    with open(tmp_audio_file, mode='wb') as f:
        f.write(audio_bytes)
    
    audio_file= open(tmp_audio_file, "rb")
    translation = client.audio.translations.create(model="whisper-1", file=audio_file)
    content = translation.text
        
    # 顯示回答
    st.write('')
    st.write('')
    st.write(':green[題目：' + st.session_state.key.split('.')[0] + '.]')
    st.write(':orange[回答：' + content + ']')
    
    st.markdown("## " + ':blue[答對了!!]' if filter_string(content.lower())==filter_string(st.session_state.key.split('.')[0].lower()) else "## " + ':red[答錯了!!]')

    question = random.choice(question_list)
    st.session_state.key = question
    placeholder.markdown(f'<span style="font-size: 24px;">{question}</span>', unsafe_allow_html=True)