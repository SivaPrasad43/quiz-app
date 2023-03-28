import streamlit as st
import pandas as pd
import random

data = pd.read_csv("combined_data.csv")

def run_quiz():
    st.title("QUIZ APP")
    st.write("all data")
    data
    questions_for_quiz(data)

def questions_for_quiz(data):
    question_array = [random.randint(1,5) for _ in range(10)]
    st.text(question_array)
    # data.iloc[question_array,[3,4,5,6,7]]
    dummy = input("eneter a number")

if __name__ == "__main__":
    run_quiz()
