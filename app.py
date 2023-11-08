import cv2
import streamlit as st

# OpenCV를 사용하여 웹캠 비디오 캡처
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠을 가리킵니다. 다른 카메라를 사용하려면 적절한 인덱스를 사용하세요.

# Streamlit 애플리케이션 정의
st.title("웹캠 비디오 스트림")
st.image([], channels="BGR")

while True:
    ret, frame = cap.read()  # 웹캠에서 프레임 읽기

    # 프레임을 Streamlit 이미지로 변환하여 표시
    st.image(frame, channels="BGR", width=640)  # width를 조절하여 이미지 크기를 설정하세요.

# Streamlit 애플리케이션을 실행하려면:
# streamlit run your_script.py
