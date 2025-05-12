import streamlit as st
from datetime import date

st.title("Test Lottery App")

# Create a date input
today = date.today()
draw_date = st.date_input("Draw Date", value=today)
st.write(f"Selected date: {draw_date}")