import streamlit as st
import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

st.title("Plant viewer")


upload_file = st.file_uploader("choose image file")
if upload_file is not None:
    st.header("use your picture")
    # image_data = upload_file.read()

    file_bytes = np.asarray(bytearray(upload_file.read()))
    img = cv2.imdecode(file_bytes, 1)
    # img = cv2.imread(stringio.name)
else:
    st.header("use sample pics")
    img = cv2.imread("./sample_pics/sample_img.jpeg")


h_l, h_u = st.slider("Hue (色相)", 0.0, 180.0, (25.0, 75.0), 1.0)
s_l, s_u = st.slider("Saturation Chroma(彩度)", 0.0, 255.0, (0.0, 255.0), 1.0)
v_l, v_u = st.slider("Value Brightness (明度)", 0.0, 255.0, (0.0, 255.0), 1.0)

vmin = 0
vmax = 180
norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
fig, ax = plt.subplots(figsize=(10, 0.3))
cmap = plt.get_cmap("hsv")
cbar = mpl.colorbar.ColorbarBase(
    ax=ax,
    cmap=cmap,
    norm=norm,
    orientation="horizontal",
)
st.pyplot(fig)

lower = (h_l, s_l, v_l)
upper = (h_u, s_u, v_u)


im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower, upper)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(im_rgb, im_rgb, mask=mask)

# fig, axes = plt.subplots(1, 3, figsize=(10, 10))

cols = st.beta_columns(2)

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(mask)

cols[0].header("segment image")
cols[0].pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(res)
cols[1].header("masked image")
cols[1].pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(im_rgb)
st.header("origin image")
st.pyplot(fig)
