import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

from audiorecorder import audiorecorder

from datetime import datetime

get_api_key = os.environ.get('OPEN_API_KEY')

client = OpenAI(
    api_key = get_api_key
)

def STT(speech):
    #파일 저장
    filename = 'imput.mp3'
    speech.export(filename, format = "mp3")

    #음원 파일 열기
    with open(filename, "rb") as audio_file:
        #whisper 모델을 활용해 텍스트 얻기
        transcription = client.audio.transcriptions.create(
            model = "whisper-1",
            file = audio_file
        )

    os.remove(filename)

    return transcription.text

def ask_gpt(prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=prompt
    )
    return response.choices[0].message.content



def main():
    st.set_page_config(page_title="음성 로봇", layout="wide")

    # 제목
    st.header("음성 챗봇 프로그램")
                    
    # 구분선
    st.markdown("---")
    with st.expander( "음성 챗봇", expanded=True):
        st.write(
        """
        음성 번역 챗봇 프로그램의 UI는 스트림릿을 활용합니다.
            - STT(Speech-To-Text)는 OpenAI의 Whisper를 활용합니다. 
            - 답변은 OpenAI의 GPT 모델을 활용합니다. 
            - TTS(Text-To-Speech)는 OpenAI의 TTS를 활용합니다.
        """
        )

        st.markdown("")
    system_content ="You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"

    # session state 초기화

    if "chat" not in st.session_state:
        st.session_state["chat"] =[]
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": system_content}]

    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False

       
    with st.sidebar:

        # GPT 모델을 선택하기 위한 라디오 버튼
        model = st.radio(label="GPT 모델", options=["gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo"])
        st.markdown("---")

        # 리셋 버튼 생성
        if st.button(label="초기화"): 
            # 리셋 코드 
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content": system_content}]
            st.session_state["check_reset"] = True

    # # 기능 구현 공간
    col1, col2 = st.columns(2)
    with col1:
        # 왼쪽 영역 작성
        st.subheader("질문하기")

        # 음성 녹음 아이콘 추가
        audio = audiorecorder()
        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]==False):
            # 음성 재생
            st.audio(audio.export().read())

            #음원 파일에서 텍스트 추출
            question = STT(audio)

            #채팅을 시각화하기 위해 질문 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"] + [("user", now, question)]

            #GPT모델에 넣을 프롬프트를 위해 질문 내용 저장
            st.session_state["messages"] = st.session_state["messages"] + [{"role":"user", "content": question}]


    with col2:
        # 오른쪽 영역 작성
        st.subheader("질문/답변")

#실행함수
if __name__=="__main__":
    main()