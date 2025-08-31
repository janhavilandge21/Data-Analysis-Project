# 🖼️ Image Analysis Using NumPy
📌 Project Overview

This project demonstrates image analysis and manipulation using NumPy and PIL (Python Imaging Library).
It covers converting images to arrays, exploring pixel data, and visualizing different image channels with Matplotlib.

📂 Dataset / Input

Image File: AI IMG.jpg (or any .jpg/.png image)

Dimensions Example: (360, 676, 3) → Height, Width, RGB Channels

🛠️ Technologies Used

Python 3

NumPy → Array-based image processing

Matplotlib → Image visualization

PIL (Pillow) → Image loading & manipulation

🔎 Key Analysis Steps

Load Image

from PIL import Image
img = Image.open("AI IMG.jpg")
img_arr = np.asarray(img)


Converts image into a NumPy array.

Image Properties

Shape → (Height, Width, Channels)

Data type → uint8

Visualization

Display original image with plt.imshow(img_arr)

Show individual RGB channels using slicing:

plt.imshow(img_arr[:,:,0], cmap='Reds')   # Red channel
plt.imshow(img_arr[:,:,1], cmap='Greens') # Green channel
plt.imshow(img_arr[:,:,2], cmap='Blues')  # Blue channel


Color Maps

Experiment with gray, Reds, Blues, Purples, PuBu etc.

Helps visualize pixel intensity variations.

📊 Insights & Findings

Images are essentially 3D NumPy arrays → (height × width × 3 channels).

Individual channels reveal color intensity contributions.

NumPy makes it easy to filter, modify, or transform images.

🚀 How to Run

Run the Jupyter Notebook:

jupyter notebook "Image Analysis Using Numpy.ipynb"

📌 Future Improvements

Implement grayscale conversion.

Apply edge detection filters (Sobel, Canny).

Perform image compression using PCA.

Build an interactive image analyzer with Streamlit.
