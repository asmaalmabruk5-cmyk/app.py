import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🌱 منصة تحليل وتوثيق عينات الفطريات والنباتات")
st.write("قم برفع صورة العينة الحقلية أو المجهرية لتطبيق خوارزميات المعالجة الرقمية التفاعلية.")

st.sidebar.header("إعدادات المعالجة الرقمية (Parameters)")
resize_width = st.sidebar.slider("عرض الصورة المعالجة (Pixels)", 100, 800, 400)
edge_threshold1 = st.sidebar.slider("عتبة الحواف الأولى (Canny Min)", 50, 200, 100)
edge_threshold2 = st.sidebar.slider("عتبة الحواف الثانية (Canny Max)", 100, 300, 200)

uploaded_file = st.file_uploader("اختر صورة العينة (JPG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("الصورة الأصلية للعينة")
        st.image(image, caption="العينة الحقلية / المجهرية", use_container_width=True)
    
    aspect_ratio = img_array.shape[0] / img_array.shape[1]
    new_height = int(resize_width * aspect_ratio)
    resized_img = cv2.resize(img_array, (resize_width, new_height))
    
    gray_img = cv2.cvtColor(resized_img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray_img, edge_threshold1, edge_threshold2)
    
    with col2:
        st.subheader("تحليل الحواف والحدود (Canny)")
        st.image(edges, caption="استخلاص البنية الهيكلية للأبواغ أو الأنسجة", use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 القياسات والخصائص الرقمية المستخرجة:")
    mean_intensity = np.mean(gray_img)
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("أبعاد الصورة الأصلية", f"{img_array.shape[1]} × {img_array.shape[0]}")
    col_stat2.metric("متوسط الشدة اللونية (Intensity)", f"{mean_intensity:.2f}")
    col_stat3.metric("حالة المعالجة", "مكتملة بنجاح ✅")
