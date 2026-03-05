
import streamlit as st
import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import qrcode
from streamlit_autorefresh import st_autorefresh

# ---------- DATABASE ----------
conn = sqlite3.connect("feedback.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT
)
""")

# ---------- CHECK MODE ----------
mode = st.query_params.get("mode")

# ---------- USER PAGE ----------
if mode == "user":

    st.title("Seminar Feedback")

    feedback = st.text_area("Enter your thought")

    if st.button("Submit"):

        if feedback.strip() != "":
            cursor.execute("INSERT INTO feedback(text) VALUES(?)",(feedback,))
            conn.commit()

            st.success("Feedback submitted successfully!")
            st.stop()

# ---------- ADMIN PAGE ----------
else:

    st.title(" Live Feedback collector")

    if st.button("Clear All Feedback"):
        cursor.execute("DELETE FROM feedback")
        conn.commit()
        st.success("All responses cleared!")
        # auto refresh every 2 seconds
    st_autorefresh(interval=2000, key="datarefresh")

    # your deployed app link
    url = "https://feedback-wordcloud-a9rveucbs5d38u2cbvr74d.streamlit.app/?mode=user"

    # generate QR
    qr = qrcode.make(url)
    qr.save("qr.png")

    st.subheader("scan this QR code")
    st.image("qr.png", width=300)

    # fetch latest feedback every refresh
    cursor.execute("SELECT text FROM feedback")
    rows = cursor.fetchall()

    words = " ".join([row[0] for row in rows])

    if words:

        wordcloud = WordCloud(
            width=900,
            height=400,
            background_color="white"
        ).generate(words)

        fig, ax = plt.subplots()
        ax.imshow(wordcloud)
        ax.axis("off")

        st.pyplot(fig)

    else:
        st.info("Waiting for feedback...")
