import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
        }
        </style>
""",
    unsafe_allow_html=True

)

st.title("Data Sweeper Starling Integrator By Yousuf Khan")
st.write("This is a tool to integrate data from Starling Bank to a CSV file")


uploaded_file = st.file_uploader("Upload Your Files (accepts only CSV or Exal)", type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1] .lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
             df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type {file_ext}")
            continue


        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())


        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Cleaning Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")


                    with col2:
                        if st.button(f"Fill Missing Values for {file.name}"):
                            numeric_cols = df.select_dtypes(include=["number"]).columns
                            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                            st.write("Missing Values Filled")

                st.subheader("Select Columns to Keep")
                columns = st.multiselect(f"Choice Columns for {file.name}", df.columns, default=df.columns)
                df = df[columns]


                st.subheader("Data Visualization")
                if st.checkbox(f"Show Visualization for {file.name}"):
                    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])



                    st.subheader("Conversion Options")
                    conversion_type = st.radio(f"Convert {file.name} to", ["CSV", "Excel"], key=file.name)
                    if st.button(f"Covnert {file.name} "):
                        buffer = BytesIO()
                        if conversion_type =="CSV":
                            df.to_csv(buffer, index=False)
                            file_name = file.name.replace(file_ext, ".csv")
                            mime_type = "text/csv"

                        elif conversion_type == "Excel":
                            df.to_excel(buffer, index=False)
                            file_name = file.name.replace(file_ext, ".xlsx")
                            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        buffer.seek(0)

                        st.download_button(
                            label=f"Dowload {file_name} as {conversion_type}",
                            data=buffer,
                            file_name=file_name,
                            mime=mime_type,
                        )

st.success("All Files Processed Successfully")