import streamlit as st
import mysql.connector

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host="project-db-stu3.smhrd.com",
    port=3307,
    user="Insa4_IOTA_final_5",
    password="aischool5",
    database="Insa4_IOTA_final_5"
)

cursor = db.cursor()

# 'run_analyzer' 함수 정의
def run_analyzer(text_data):
    st.write(f"업로드된 텍스트 데이터: {text_data}")
    
    processed_data = process_text_data(text_data)
    
    try:
        # 테이블 이름과 컬럼 이름 변경
        insert_query = "INSERT INTO tb_product (product_code) VALUES (%s)"
        cursor.execute(insert_query, (processed_data,))
        db.commit()
        st.write("텍스트 데이터가 성공적으로 MySQL 데이터베이스에 저장되었습니다.")
    except mysql.connector.Error as err:
        st.error(f"MySQL 오류: {err}")

# 텍스트 데이터 처리 함수 정의
def process_text_data(text_data):
    # 여기에 데이터를 가공하는 로직을 추가
    return text_data

# Streamlit 앱 시작
st.title("텍스트 업로더")
st.write('텍스트를 업로드하세요.')
st.title("")
st.title("")

# 텍스트 업로드
uploaded_text = st.text_area('텍스트 입력')

if uploaded_text:
    run_analyzer(uploaded_text)
