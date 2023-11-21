import streamlit as st
from PIL import Image
from google.cloud import storage
from io import BytesIO
import mysql.connector

# MySQL 연결 정보
mysql_host = "project-db-stu3.smhrd.com"
mysql_port = 3307
mysql_user = "Insa4_IOTA_final_5"
mysql_password = "aischool5"
mysql_db = "Insa4_IOTA_final_5"

# MySQL 연결
conn = mysql.connector.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, database=mysql_db)
cursor = conn.cursor()

# Google Cloud Storage에 연결
client = storage.Client.from_service_account_json('C:/Users/gjaischool/streamlit-app/formidable-pact-405301-da7de3cda556.json')

def save_image_to_gcs_and_mysql(image, bucket, blob_name, target_size=(192, 256)):
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

    # 이미지를 BytesIO로 변환
    image_bytes = BytesIO()
    cropped_image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    # GCS에 이미지 업로드
    blob = bucket.blob(blob_name)
    blob.upload_from_file(image_bytes, content_type='image/jpeg')

    # GCS에 업로드된 이미지의 공개 URL을 반환
    image_url = f"https://storage.googleapis.com/{bucket.name}/{blob_name}"

    # MySQL에 이미지 정보 저장
    sql = "INSERT INTO tb_images (image_loc) VALUES (%s)"
    cursor.execute(sql, (image_url,))
    conn.commit()

    return image_url

st.title("")
st.write('1. 카메라 권한 허용 후 전신 사진을 찍어주세요.')
st.write('2. 결과가 업로드된 사진을 확인하세요.')
st.write('3. 모바일에 경우는 전신사진을 업로드 해주세요.')
st.title("")
st.title("")

# GCS 버킷 이름과 Blob 이름
bucket_name_input = "streamlit_input"
blob_name_input = "test.jpg"

bucket_name_output = "streamlit_output"
images_output = ["output1.png", "output2.png", "output3.png", "output4.png"]

# 캡처할 이미지의 크기를 지정합니다.
target_size = (192, 256)

# 카메라 입력을 받아옵니다.
cam = st.camera_input(label='전신 촬영', disabled=False)

# 파일 업로드 기능을 추가합니다.
uploaded_file = st.file_uploader("또는 파일 업로드", type=["jpg", "jpeg"])

# 이미지 URL을 담을 리스트 초기화
image_urls_output = []

# 이미지 파일의 URL을 가져와서 리스트에 추가
bucket_output = client.get_bucket(bucket_name_output)
for image_name_output in images_output:
    blob_output = bucket_output.blob(image_name_output)
    image_url_output = f"https://storage.googleapis.com/{bucket_name_output}/{image_name_output}"
    image_urls_output.append(image_url_output)

# 업로드된 파일 또는 카메라에서 가져온 이미지가 있으면 실행합니다.
if uploaded_file is not None or cam is not None:
    if uploaded_file is not None:
        # 업로드된 파일을 GCS에 업로드하고 MySQL에 이미지 정보 저장
        with st.spinner('제출 중입니다'):
            image_url_input = save_image_to_gcs_and_mysql(uploaded_file, client.get_bucket(bucket_name_input), blob_name_input, target_size=target_size)
            st.success(f'이미지가 성공적으로 저장되었습니다! GCS와 MySQL에 파일 정보가 저장되었습니다. Image URL: {image_url_input}')
    elif cam is not None:
        # 카메라에서 가져온 이미지를 GCS에 업로드하고 MySQL에 이미지 정보 저장
        with st.spinner('제출 중입니다'):
            image_url_input = save_image_to_gcs_and_mysql(cam, client.get_bucket(bucket_name_input), blob_name_input, target_size=target_size)
            st.success(f'이미지가 성공적으로 저장되었습니다! GCS와 MySQL에 파일 정보가 저장되었습니다. Image URL: {image_url_input}')

# 똑같은 크기의 버튼 4개를 가로로 만들기
col1, col2, col3, col4 = st.columns(4)

# 각 버튼에 대한 동작 설정
if col1.button("버튼 1"):
    # 버튼 1이 클릭되었을 때, 이미지 표시
    st.image(image_urls_output[0], caption='이미지 1', use_column_width=False, width=300)

if col2.button("버튼 2"):
    # 버튼 2이 클릭되었을 때, 이미지 표시
    st.image(image_urls_output[1], caption='이미지 2', use_column_width=False, width=300)

if col3.button("버튼 3"):
    # 버튼 3이 클릭되었을 때, 이미지 표시
    st.image(image_urls_output[2], caption='이미지 3', use_column_width=False, width=300)

if col4.button("버튼 4"):
    # 버튼 4이 클릭되었을 때, 이미지 표시
    st.image(image_urls_output[3], caption='이미지 4', use_column_width=False, width=300)
st.write("Image URLs:", image_urls_output)

# MySQL 연결 종료
cursor.close()
conn.close()
