import streamlit as st
from PIL import Image
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

def run_analyzer(image):
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    try:
        insert_query = "INSERT INTO images (image) VALUES (%s)"
        cursor.execute(insert_query, (image.tobytes(),))
        db.commit()
        st.write("이미지가 성공적으로 MySQL 데이터베이스에 저장되었습니다.")
    except mysql.connector.Error as err:
        st.error(f"MySQL 오류: {err}")

# Streamlit 앱 시작
st.title("의상 피팅 인풋 카메라")

# 2. 카메라 사용 허용 및 전신을 사진으로 찍거나 사진을 업로드하세요.
st.write('2. 카메라 사용 권한을 부여하고 전신을 촬영하거나 사진을 업로드하세요.')

# 3. 결과가 업로드되었다는 확인을 기다립니다.
st.write('3. 피팅된 옷을 확인합니다.')

# 빈 줄 추가
st.title("")
st.title("")

# 카메라 입력 또는 파일 업로드
cam = st.camera_input(label='전신를 사진으로 찍으세요', disabled=False)
file = st.file_uploader('또는 전신 사진을 업로드하세요', type=["png", "jpg", "jpeg"])
image_main = None

if cam is not None:
    image_main = cam
elif file is not None:
    image_main = Image.open(file)

if image_main is not None:
    run_analyzer(image_main) 
