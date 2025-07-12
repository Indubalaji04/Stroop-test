
import streamlit as st
import pandas as pd
import random
import time

# Set page config
st.set_page_config(page_title="Stroop Test", layout="centered")

# Collect participant info
st.title("Stroop Test")
st.write("Click the color of the **font**, not the word.")

with st.form("participant_form"):
    name = st.text_input("Name")
    age = st.text_input("Age")
    profession = st.text_input("Profession")
    sleep_hours = st.text_input("How many hours did you sleep last night?")
    submitted = st.form_submit_button("Start Test")

if submitted and name and age and profession and sleep_hours:
    st.success("Test started! Respond quickly.")

    colors = ["Red", "Green", "Blue", "Yellow"]
    color_map = {
        "Red": "red",
        "Green": "green",
        "Blue": "blue",
        "Yellow": "yellow"
    }

    num_trials = 10
    results = []

    for i in range(num_trials):
        st.write("---")
        word = random.choice(colors)
        font_color = random.choice(colors)
        st.markdown(f"<h2 style='color:{color_map[font_color]}'>{word}</h2>", unsafe_allow_html=True)

        start_time = time.time()
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        clicked = st.empty()

        if col1.button("Red", key=f"red_{i}"):
            clicked.button = "Red"
        elif col2.button("Green", key=f"green_{i}"):
            clicked.button = "Green"
        elif col3.button("Blue", key=f"blue_{i}"):
            clicked.button = "Blue"
        elif col4.button("Yellow", key=f"yellow_{i}"):
            clicked.button = "Yellow"

        if hasattr(clicked, "button"):
            rt = round(time.time() - start_time, 3)
            correct = clicked.button == font_color
            results.append({
                "Trial": i + 1,
                "Word": word,
                "Font Color": font_color,
                "Clicked": clicked.button,
                "Correct": correct,
                "Reaction Time (s)": rt
            })

    # Save results
    df = pd.DataFrame(results)
    df.loc[-1] = ["Participant Info", "", "", "", "", ""]
    df.loc[-2] = ["Name", name, "", "", "", ""]
    df.loc[-3] = ["Age", age, "", "", "", ""]
    df.loc[-4] = ["Profession", profession, "", "", "", ""]
    df.loc[-5] = ["Sleep Hours", sleep_hours, "", "", "", ""]
    df.index = df.index + 5
    df.sort_index(inplace=True)

    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Results", csv, f"{name}_stroop_results.csv", "text/csv")
