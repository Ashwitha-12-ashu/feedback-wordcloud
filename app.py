import streamlit as st
import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import qrcode
from streamlit_autorefresh import st_autorefresh

# ---------------- DATABASE ----------------
conn = sqlite3.connect("feedback.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT
)
""")

# ---------------- CHECK MODE ----------------
mode = st.query_params.get("mode")

# ---------------- USER FEEDBACK PAGE ----------------
if mode == "user":
    st.title("Seminar Feedback")

    feedback = st.text_area("Enter your thought")

    if st.button("Submit"):
        if feedback.strip() != "":
            cursor.execute("INSERT INTO feedback(text) VALUES(?)", (feedback,))
            conn.commit()

            st.success("Feedback submitted successfully 🎉")
            st.stop()

# ---------------- ADMIN PAGE ----------------
else:
    st.title("📌 Live Feedback Collector (Admin)")

    if st.button("Clear All Feedback"):
        cursor.execute("DELETE FROM feedback")
        conn.commit()
        st.success("All responses cleared!")

    # auto-refresh every 2 sec
    st_autorefresh(interval=2000, key="data_refresh")

    # your LIVE Streamlit URL (IMPORTANT)
    url = "https://feedback-wordcloud-a9rveucbs5d38u2cbvr74d.streamlit.app/?mode=user"

    # Generate QR Code
    qr = qrcode.make(url)
    qr.save("qr.png")

    st.subheader("📱 Scan this to Submit Feedback")
    st.image("qr.png", width=300)

    # Fetch all feedback
    cursor.execute("SELECT text FROM feedback")
    rows = cursor.fetchall()

    words = " ".join([row[0] for row in rows])

    if words.strip() != "":
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
