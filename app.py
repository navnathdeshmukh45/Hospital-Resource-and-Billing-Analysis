import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Hospital Dashboard", layout="wide")
st.title("🏥 Hospital Data Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload Hospital Dataset (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean data
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    df['Billing Amount'] = df['Billing Amount'].replace('[\$,]', '', regex=True).astype(float)
    df['Billing Amount'] = df['Billing Amount'].apply(lambda x: 0 if x < 0 else x)
    df['Length of Stay'] = (df['Discharge Date'] - df['Date of Admission']).dt.days

    st.subheader("👤 Patient Demographics")

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df['Gender'].value_counts())
    with col2:
        st.bar_chart(df['Blood Type'].value_counts())

    st.subheader("💵 Billing Amount Analysis")
    st.bar_chart(df.groupby('Hospital')['Billing Amount'].sum())

    st.subheader("🩺 Top Medical Conditions")
    top_conditions = df['Medical Condition'].value_counts().head(10)
    st.bar_chart(top_conditions)

    st.subheader("📆 Length of Stay Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['Length of Stay'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    st.subheader("📋 Doctor Performance (Patients Count)")
    st.bar_chart(df['Doctor'].value_counts().head(10))

    st.success("✅ Analysis Completed.")
