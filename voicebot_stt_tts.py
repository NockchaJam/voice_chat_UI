import streamlit as st

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

#실행함수
if __name__=="__main__":
    main()