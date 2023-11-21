import streamlit as st

# 이미지를 가운데로 정렬하기 위한 CSS 스타일
style = """
    <style>
        div.stImage {
            display: flex;
            justify-content: center;
        }
    </style>
"""

# 스타일 적용
st.markdown(style, unsafe_allow_html=True)

# 이미지 추가
st.image(".\뉴로고.jpg")

