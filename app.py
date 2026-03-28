import streamlit as st
import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import qrcode
from streamlit_autorefresh import st_autorefresh
import os

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

    st.title("Feedback Scanner")

    feedback = st.text_area("Enter your thought")

    if st.button("Submit"):
        if feedback.strip() != "":
            cursor.execute("INSERT INTO feedback(text) VALUES(?)", (feedback.strip(),))
            conn.commit()
            st.success("Feedback submitted successfully!")
            st.stop()
        else:
            st.warning("Please enter something before submitting.")

# ---------- ADMIN PAGE ----------
else:

    st.title("📡 Live Feedback Collector")

    # Clear button
    if st.button("🗑 Clear All Feedback"):
        cursor.execute("DELETE FROM feedback")
        conn.commit()
        st.success("All responses cleared!")

    # Auto refresh every 2 sec
    st_autorefresh(interval=2000, key="datarefresh")

    # your deployed app link
    url = "https://feedback-wordcloud-a9rveucbs5d38u8cbvr74d.streamlit.app/?mode=user"

    # ---------- QR CODE ----------
    qr_path = "qr.png"
    if not os.path.exists(qr_path):
        qr = qrcode.make(url)
        qr.save(qr_path)

    st.subheader("📱 Scan this QR to Submit Feedback")
    st.image(qr_path, width=250)

    # ---------- FETCH FEEDBACK ----------
    cursor.execute("SELECT text FROM feedback")
    rows = cursor.fetchall()

    # join all feedback
    words = " ".join([row[0] for row in rows if row[0].strip() != ""]).strip()

    st.markdown("---")

    # ---------- DISPLAY WORDCLOUD OR MESSAGE ----------
    if len(rows) == 0:
        st.info("No feedback received yet... Waiting!")
    elif words == "":
        st.info("Feedback exists but contains empty text only.")
    else:
        try:
            wordcloud = WordCloud(
                width=900,
                height=400,
                background_color="white"
            ).generate(words)

            fig, ax = plt.subplots()
            ax.imshow(wordcloud)
            ax.axis("off")

            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error generating word cloud: {e}")
            st.write("Raw words:", words)
