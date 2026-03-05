
import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import qrcode
import time

# ---------- DATABASE CONNECTION ----------

conn = mysql.connector.connect(
    host="localhost",
    user="feedbackuser",
    password="1234",
    database="feedback_db"
)

cursor = conn.cursor()

# ---------- READ URL PARAMETER ----------

params = st.query_params
mode = params.get("mode", "admin")

# ---------- STUDENT PAGE ----------

if mode == "user":

    st.title("Seminar Feedback")

    feedback = st.text_area("Enter your feedback")

    if st.button("Submit"):

        if feedback.strip() == "":
            st.warning("Please enter feedback")

        else:
            cursor.execute(
                "INSERT INTO feedback(text) VALUES (%s)",
                (feedback,)
            )
            conn.commit()

            st.success("Thank you! Your feedback was submitted.")

# ---------- ADMIN PAGE ----------

else:

    st.title("Live Seminar Feedback")

    # Your laptop IP
    ip = "192.168.10.34"

    link =link = "https://unfeared-pseudoaristocratical-kellye.ngrok-free.dev/?mode=user"

    # ---------- QR CODE ----------

    qr = qrcode.make(link)

    qr.save("qr.png")

    st.subheader("Students scan this QR code")

    st.image("qr.png")

    st.write(link)

    st.divider()

    # ---------- WORD CLOUD ----------

    st.subheader("Live WordCloud")

    cursor.execute("SELECT text FROM feedback ORDER BY id DESC LIMIT 200")

    data = cursor.fetchall()

    text = " ".join([row[0] for row in data])

    if text.strip() == "":
        st.write("Waiting for feedback...")
    else:

        wc = WordCloud(
            width=1000,
            height=500,
            background_color="white",
            font_path="/home/user/.local/lib/python3.10/site-packages/wordcloud/DroidSansMono.ttf"
        ).generate(text)

        fig, ax = plt.subplots()

        ax.imshow(wc)

        ax.axis("off")

        st.pyplot(fig)

    # ---------- AUTO REFRESH ----------

    time.sleep(3)
    st.rerun()
