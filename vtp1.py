import streamlit as st
import pyautogui
from fpdf import FPDF
from io import BytesIO
from PIL import Image

# List to store screenshot images
if "screenshots" not in st.session_state:
    st.session_state.screenshots = []

# Create a function to take a screenshot and store it in the screenshots list
def take_screenshot():
    screenshot = pyautogui.screenshot()
    st.session_state.screenshots.append(screenshot)

# Define a function to create and download PDF
def create_and_download_pdf():
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    for img_data in st.session_state.screenshots:
        img = img_data
        pdf.add_page()
        
        # Convert the image to RGB mode (FPDF only supports RGB mode)
        img = img.convert('RGB')
        
        # Calculate image size and position to fit in the landscape A4 page
        img_w, img_h = img.size
        pdf_w, pdf_h = 297, 210  # A4 size in mm in landscape
        
        # Calculate the scaling ratio and new dimensions
        ratio = min(pdf_w / img_w, pdf_h / img_h)
        new_w, new_h = img_w * ratio, img_h * ratio
        
        # Center the image on the page
        x = (pdf_w - new_w) / 2
        y = (pdf_h - new_h) / 2
        
        # Save the image to a BytesIO object
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Insert the image into the PDF
        pdf.image(img_bytes, x, y, new_w, new_h)
    
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    st.download_button(label="Download PDF", data=pdf_output, file_name="output.pdf", mime="application/pdf")

# Layout
st.sidebar.header("Video to PDF Converter")
st.sidebar.divider()
st.sidebar.header("Options")
link_checkbox = st.sidebar.checkbox("Play video from a link")
file_checkbox = st.sidebar.checkbox("Play video from a file")
how_to_use=st.sidebar.checkbox("How To Use")
st.sidebar.divider()
download_button = st.sidebar.button("Download PDF")
st.sidebar.divider()
screenshot_button = st.sidebar.button("Take Screenshot")
st.sidebar.divider()


# Video from link
if link_checkbox:
    video_url = st.text_input("Enter video URL:")
    if video_url:
        st.video(video_url)
        st.header("Screenshots")

# Video from file
if file_checkbox:
    video_file = st.file_uploader("Upload a video file:")
    if video_file:
        st.video(video_file)
        st.header("Screenshots")
if how_to_use:
    st.video("https://youtu.be/oOeD2TJo96A?si=lB61klBonGrRwr0Y")

# Take screenshot if button is pressed
if screenshot_button:
    take_screenshot()
col1,col2=st.columns([1,1])
# Display screenshots in the second column
if st.session_state.screenshots:
    i=0
    for img_data in st.session_state.screenshots:
        i=i+1
        if not i%2==0:
            with col1:
                st.image(img_data)
        else:
            with col2:
                st.image(img_data)

# Download PDF button action
if download_button:
    create_and_download_pdf()
