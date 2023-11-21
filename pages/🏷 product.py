import streamlit as st
import mysql.connector

# MySQL 연결 설정
db_config = {
    "host": "project-db-stu3.smhrd.com",
    "port": 3307,
    "user": "Insa4_IOTA_final_5",
    "password": "aischool5",
    "database": "Insa4_IOTA_final_5",
}

# Streamlit 애플리케이션 시작
st.title("재고관리 페이지")

# 사용자로부터 입력 받기
user_input_product_code = st.text_input("상품코드:")
user_input_product_name = st.text_input("상품명:")
user_input_product_price = st.text_input("상품가격:")
user_input_product_cnt = st.text_input("상품재고:")
user_input_company_cd = st.text_input("회사코드:")

# 'Submit' 버튼 클릭 시 동작
if st.button("제출"):
    # MySQL에 데이터 삽입
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # 사용자 입력 데이터를 MySQL 테이블에 삽입하는 쿼리
        insert_query = "INSERT INTO tb_product (product_code, product_name, product_price, product_cnt, company_cd) VALUES (%s, %s, %s, %s, %s)"
        data = (
            int(user_input_product_code),
            user_input_product_name,
            float(user_input_product_price),
            int(user_input_product_cnt),
            int(user_input_company_cd),
        )
        cursor.execute(insert_query, data)

        # 변경 사항 커밋
        connection.commit()

        st.success("Data successfully inserted into MySQL!")

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        # 연결 닫기
        if connection.is_connected():
            cursor.close()
            connection.close()
            st.write("MySQL connection is closed.")
