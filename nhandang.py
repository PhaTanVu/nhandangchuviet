import io
import numpy as np
from PIL import Image
import pytesseract
import streamlit as st
from sympy import *
from skimage import io, color, filters, measure

# Khởi tạo các biến ký hiệu
x, y, z = symbols('x y z')

# Function to extract expressions from an image
def extract_expressions(img_arr):
    # Chuyển đổi ảnh sang ảnh đen trắng
    img_gray = color.rgb2gray(img_arr)
    img_bw = (img_gray < filters.threshold_otsu(img_gray)) * 1
    
    # Phân đoạn ảnh để tìm các vùng chứa biểu thức toán
    regions = measure.regionprops(measure.label(img_bw))

    # Duyệt qua các vùng chứa biểu thức toán và chuyển đổi sang định dạng LaTeX
    expressions = []
    for region in regions:
        # Lấy tọa độ của vùng
        minr, minc, maxr, maxc = region.bbox
        # Cắt ảnh để lấy vùng biểu thức toán
        img_expression = img_arr[minr:maxr, minc:maxc]
        # Chuyển đổi ảnh sang nội dung văn bản
        expression = pytesseract.image_to_string(img_expression)
        # Nhận dạng và chuyển đổi biểu thức sang định dạng LaTeX
        try:
            expr = parse_expr(expression)
            latex_expr = latex(expr)
            expressions.append(latex_expr)
        except:
            pass
    return expressions

# Streamlit app
st.set_page_config(page_title="Nhận dạng biểu thức toán", page_icon="🧮")
st.title("Nhận dạng biểu thức toán từ ảnh")

# File uploader
uploaded_file = st.file_uploader("Tải lên file ảnh", type=["jpg", "jpeg", "png"])

# Extract expressions button
if st.button("Trích xuất biểu thức toán"):
    # Kiểm tra xem người dùng đã tải lên file hay chưa
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img_arr = np.array(img)

        # Extract expressions from the image
        expressions = extract_expressions(img_arr)

        # Display the extracted expressions
        if len(expressions) > 0:
            st.write("Các biểu thức toán được trích xuất từ ảnh:")
            for expression in expressions:
                # Hiển thị biểu thức dưới dạng LaTeX
                st.latex(expression)
                # Chuyển đổi biểu thức sang hình ảnh và hiển thị
                expr_image = io.BytesIO()
                render_latex(expression, expr_image, fontsize=20)
                st.image(expr_image.getvalue())
        else:
            st.write("Không tìm thấy biểu thức toán trong ảnh")
