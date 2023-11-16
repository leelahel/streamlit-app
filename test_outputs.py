import streamlit as st
from PIL import Image
from google.cloud import storage
from io import BytesIO
import mysql.connector

# MySQL 연결 설정
connection = mysql.connector.connect(
    host="project-db-stu3.smhrd.com",
    port=3307,
    user="Insa4_IOTA_final_5",
    password="aischool5",
    database="Insa4_IOTA_final_5"
)

cursor = connection.cursor()

def save_image_to_gcs(image, bucket_name, blob_name, target_size=(192, 256)):
    # 이미지를 PIL Image로 변환
    image_pil = Image.open(image)

    # 이미지의 크기를 가져옵니다.
    width, height = image_pil.size
    
    left = max(0, (width - target_size[0]) // 2)
    top = max(0, (height - target_size[1]) // 2)
    
    right = min(width, left + target_size[0])
    bottom = min(height, top + target_size[1])

    # 이미지를 자르고 파일로 저장합니다.
    cropped_image = image_pil.crop((left, top, right, bottom))

    # Google Cloud Storage에 연결
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    # 이미지를 BytesIO로 변환
    image_bytes = BytesIO()
    cropped_image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    # GCS에 이미지 업로드
    blob = bucket.blob(blob_name)
    blob.upload_from_file(image_bytes, content_type='image/jpeg')

    # GCS에 업로드된 이미지의 공개 URL을 반환
    image_url = f"https://storage.googleapis.com/{bucket_name}/{blob_name}"

    return image_url

def save_file_path_to_mysql(image_url):
    # 파일 정보를 MySQL에 저장
    query = "INSERT INTO tb_images (image_loc) VALUES (%s)"
    cursor.execute(query, (image_url,))
    
    # 변경사항을 반영
    connection.commit()

    # 마지막으로 삽입된 행 ID를 가져와서 image_number로 사용
    cursor.execute("SELECT LAST_INSERT_ID()")
    image_number = cursor.fetchone()[0]

    return image_number

# GCS 버킷 이름과 Blob 이름
bucket_name = "streamlit_input"
blob_name = "test.jpg"

st.title("")
st.write('1. 카메라 사용 권한을 허용하고 전신이 들어오게 사진을 찍어주세요!.')
st.write('2. 결과가 업로드된 사진을 확인하세요.')
st.title("")
st.title("")

# 캡처할 이미지의 크기를 지정합니다.
target_size = (192, 256)

# 카메라 입력을 받아옵니다.
cam = st.camera_input(label='전신 촬영', disabled=False)

# 카메라에서 가져온 이미지가 있으면 실행합니다.
if cam is not None:
    # 이미지를 GCS에 업로드하고 이미지 URL을 받아옵니다.
    with st.spinner('제출 중입니다'):
        image_url = save_image_to_gcs(cam, bucket_name, blob_name, target_size=target_size)
        image_number = save_file_path_to_mysql(image_url)
        st.success(f'이미지가 성공적으로 저장되었습니다! MySQL에 파일 정보가 저장되었습니다. Image Number: {image_number}')

# 연결 해제
cursor.close()
connection.close()
