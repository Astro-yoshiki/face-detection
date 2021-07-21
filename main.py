import streamlit as st

from FaceAPI import FaceAPI

st.title("顔認識アプリ")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    api = FaceAPI(img_src=uploaded_file, SUBSCRIPTION_KEY=st.secrets["SUBSCRIPTION_KEY"])
    img = api.face_detect()
    st.image(img, caption="Uploaded Image", use_column_width=True)
