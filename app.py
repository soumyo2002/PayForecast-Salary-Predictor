import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np



def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = pickle.load(open("saved_steps.pkl", "rb"))

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("PayForecast: Unveiling Tomorrow's Compensation Today")

    st.write("""### Please answer some of our questions""")

    countries = (
        "United States of America",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )
    
    skill_levels = {
        "Beginner",
        "Advanced" ,
        "Intermediate"
    }

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    expericence = st.slider("Years of Experience", 0, 50, 3)
    skill_level = st.selectbox("Skill Level", skill_levels)

    if skill_level == "Beginner":
        skill = 1
    elif skill_level == "Intermediate":
        skill = 2
    else:
        skill = 3

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, expericence, skill]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


df = pd.read_csv("processed_data.csv")

col1, col2 = st.columns([1, 2])
with col2:
    st.write("# Major Project 2023")
with col1:
    st.image('images.png', width=200)  



def show_explore_page():
    st.title("Explore Salaries Stats")

    st.write(
        """
    ### Stack Overflow Developer Survey 2023
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal") 

    st.write("""#### Data gathered from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)


page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))
if page == "Predict":
    show_predict_page()
else:
    show_explore_page()

st.sidebar.markdown("## Mentor:")
st.sidebar.markdown("- **Professor Ajit Kumar Pasayat**")

st.sidebar.markdown("## Contributors:")
st.sidebar.markdown("- **Soumyo Chakravorty**")
st.sidebar.markdown("- **Pratik Jha**")
st.sidebar.markdown("- **Mohit Kumar Nanda**")
st.sidebar.markdown("- **Harshit Sharma**")
st.sidebar.markdown("- **Vishesh Ranjan**")


footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f4f4f4;
    color: #555;
    text-align: center;
    padding: 10px 0;
}
</style>
<div class="footer">© 2023 KIIT. Made with \u2764\ufe0f.</div>
"""
st.markdown(footer, unsafe_allow_html=True)

email_address = "20051110@kiit.ac.in"

st.markdown('### Contact Us')
st.markdown(f'<a href="mailto:{email_address}?Subject=Hello" target="_blank">Click here</a>', unsafe_allow_html=True)
