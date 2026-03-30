import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🔍 PCB Component Identifier")

uploaded_file = st.file_uploader("Upload PCB Image", type=["jpg", "png"])

def detect_components(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    components = []

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)

            if w > h:
                comp = "Resistor"
            elif h > w:
                comp = "Capacitor"
            else:
                comp = "IC"

            components.append((x, y, w, h, comp))

    return components

if uploaded_file:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    components = detect_components(image_np)

    for (x, y, w, h, comp) in components:
        cv2.rectangle(image_np, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image_np, comp, (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    st.image(image_np, caption="Detected Components", use_column_width=True)

    st.subheader("Detected Components:")
    for c in components:
        st.write(f"📌 {c[4]}")
