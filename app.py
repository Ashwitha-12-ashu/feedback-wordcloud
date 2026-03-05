
TypeError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/feedback-wordcloud/app.py", line 55, in <module>
    st.image(qr_img)
    ~~~~~~~~^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/runtime/metrics_util.py", line 532, in wrapped_func
    result = non_optional_func(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/image.py", line 215, in image
    marshall_images(
    ~~~~~~~~~~~~~~~^
        self.dg._get_delta_path_str(),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        output_format,
        ^^^^^^^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/lib/image_utils.py", line 445, in marshall_images
    proto_img.url = image_to_url(
                    ~~~~~~~~~~~~^
        single_image, layout_config, clamp, channels, output_format, image_id
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/lib/image_utils.py", line 337, in image_to_url
    image_data = _ensure_image_size_and_format(image_data, layout_config, image_format)
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/lib/image_utils.py", line 186, in _ensure_image_size_and_format
    pil_image: PILImage = Image.open(io.BytesIO(image_data))
                                     ~~~~~~~~~~^^^^^^^^^^^^
