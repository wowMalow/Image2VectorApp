import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO

from app.styles.spiral_touch import transform_image


def init_app() -> None:
    # page configurations
    st.set_page_config(page_title="Image editing app")
    st.header("Image Editing App 📸")
    st.subheader("Upload an image to get started 🚀")

    image = st.file_uploader("Upload an image", type=[
                            "png", "jpg"], accept_multiple_files=False)

    # if image uploaded
    if image:
        # getting image in PIL
        img = Image.open(image)

        #adding sidebar
        st.sidebar.header("Editing panel")

        # writting settings code
        st.sidebar.write("Preprocessing settings")
        setting_sharp = st.sidebar.slider("Sharpness")
        setting_color = st.sidebar.slider("Color")
        setting_brightness = st.sidebar.slider("Brightness")
        setting_contrast = st.sidebar.slider("Contrast")
        setting_inverse_color = st.sidebar.checkbox("Inverse color")
        setting_blur = st.sidebar.checkbox("Blur")
        setting_flip_image = st.sidebar.selectbox("Flip Image", options=(
            "select flip direction", "Vertical flip", "Horizontal flip")
        )


        # writing filters code
        st.sidebar.write("Style settings")
        style_spiral_step = st.sidebar.slider("Spiral step", 2.0, 10.)
        style_spiral_color = st.sidebar.color_picker("Spiral color", "#65BFFC")
        style_topleft_color = st.sidebar.color_picker("Background top-left color", "#64130A")
        style_bottomright_color = st.sidebar.color_picker("Background bottom-right color", "#051646")

        if setting_blur:
            setting_blur_strength = st.sidebar.slider("Select Blur strength")

        # checking setting_sharp value
        if setting_sharp:
            sharp_value = setting_sharp
        else:
            sharp_value = 0

        # checking color
        if setting_color:
            set_color = setting_color
        else:
            set_color = 1

        # checking brightness
        if setting_brightness:
            set_brightness = setting_brightness
        else:
            set_brightness = 1

        # checking contrast
        if setting_contrast:
            set_contrast = setting_contrast
        else:
            set_contrast = 1

        # checking setting_flip_image
        flip_direction = setting_flip_image

        # implementing sharpness
        sharp = ImageEnhance.Sharpness(img)
        edited_img = sharp.enhance(sharp_value)

        # implementing colors
        color = ImageEnhance.Color(edited_img)
        edited_img = color.enhance(set_color)

        # implementing brightness
        brightness = ImageEnhance.Brightness(edited_img)
        edited_img = brightness.enhance(set_brightness)

        # implementing contrast
        contrast = ImageEnhance.Contrast(edited_img)
        edited_img = contrast.enhance(set_contrast)

        # implementing flip direction
        if flip_direction == "Vertical flip":
            edited_img = edited_img.transpose(Image.FLIP_TOP_BOTTOM)
        elif flip_direction == "Horizontal flip":
            edited_img = edited_img.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            pass


        if setting_blur:
            if setting_blur_strength:
                set_blur = setting_blur_strength
                edited_img = edited_img.filter(ImageFilter.GaussianBlur(set_blur))

        # displaying edited image
        st.image(edited_img, width=400)
        st.write("\nFinal result:")

        spiral_img = transform_image(
            file=edited_img,
            alpha=style_spiral_step,
            inverse_flag=setting_inverse_color,
            spiral_color=style_spiral_color,
            background_color1=style_topleft_color,
            background_color2=style_bottomright_color,
        )
        st.image(spiral_img, width=800)

        img_bytes = BytesIO()
        spiral_img.seek(0)
        spiral_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        btn = st.download_button(
                label="Download image",
                data=img_bytes,
                file_name="flower.png",
                mime="image/png")
            
