import streamlit as st


# --- PAGE SETUP ---
home_page = st.Page(
    "views/homepage.py",
    title="Homepage",
    icon=":material/account_circle:",
    default=True,
)
get_analysis = st.Page(
    "views/analysis.py",
    title="Usage Dashboard",
    icon=":material/bar_chart:",
)
mrp_forecast = st.Page(
    "views/mrp_forecast.py",
    title="MRP Record & Forecast",
    icon=":material/smart_toy:",
)


# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [home_page],
        "Projects": [get_analysis, mrp_forecast],
    }
    
)

# st.sidebar.markdown('***')
st.sidebar.write('Made by [Sushant](https://www.linkedin.com/in/sushant-singh-0a0167207/)')

# # --- SHARED ON ALL PAGES ---
st.logo("assets/app logo.png")


# --- RUN NAVIGATION ---
pg.run()
# st.sidebar.write("\n" * 15)  # Adjust the number of new lines as needed

# # Add your text
# st.sidebar.write("Made by [Sushant](https://youtube.com/@codingisfun)")
# # st.sidebar.write("Made by [Sushant](https://youtube.com/@codingisfun)")