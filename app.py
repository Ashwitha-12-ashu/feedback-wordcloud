
import streamlit as st
import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import qrcode

# Database
conn = sqlite3.connect("feedback.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT
)
""")

# Page mode
mode = st.query_params.get("mode")

# ---------------- USER PAGE ----------------
if mode == "user":

    st.title("Seminar Feedback")

    feedback = st.text_area("Enter your feedback")

    if st.button("Submit"):

        if feedback.strip() != "":
            cursor.execute("INSERT INTO feedback(text) VALUES(?)", (feedback,))
            conn.commit()
            st.success("Thank you for your feedback!")

# ---------------- ADMIN PAGE ----------------
else:

    st.title("Live Seminar Feedback")

    url = "https://feedback-wordcloud-a9rveucbs5d38u2cbvr74d.streamlit.app/?mode=user"

    qr = qrcode.make(url)

    st.subheader("Students scan this QR code")
    st.image(qr)

    cursor.execute("SELECT text FROM feedback")
    data = cursor.fetchall()

    words = " ".join([row[0] for row in data])

    if words:

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white"
        ).generate(words)

        fig, ax = plt.subplots()
        ax.imshow(wordcloud)
        ax.axis("off")

        st.pyplot(fig)

    st.caption("Refresh page to update WordCloud")
