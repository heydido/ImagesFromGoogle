import glob
import os
import streamlit as st
from src.image_scrapper import ImagesFromGoogle
from PIL import Image

# Page layout
st.set_page_config(
    page_title="Images from Google",
    page_icon="🔍",
    layout="wide"
)

# User interface
st.header("Images from Google!")

# User inputs
st.sidebar.subheader('User Inputs:')
_search_item = st.sidebar.text_input('What/Who are you looking for?')
search_item = _search_item.replace(' ', '') if ' ' in _search_item else _search_item

# Scrapper
google_images = ImagesFromGoogle()
# Fake user agent to avoid getting blocked by Google
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/58.0.3029.110 Safari/537.36"}

if search_item:
    image_urls = google_images.scrape_images(search_item=search_item)
    image_paths = google_images.save_images(search_item=search_item)

    images = []
    for img_path in glob.glob(f'images/{search_item}*jpg'):
        image = Image.open(img_path)
        image = image.resize((140, 140))
        images.append(image)

    # All Images
    st.subheader(f'Found these images for {_search_item}:')
    st.image(images)
