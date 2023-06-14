import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import io
import seaborn as sns
import numpy as np

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")
    
    num_rows = len(df)
    st.write("Number of rows: ", num_rows)
    
    num_columns = len(df.columns)
    st.write("Number of columns: ", num_columns)

    categorical_variables = df.select_dtypes(include=['object']).columns
    st.write("Number of Categorical Columns", len(categorical_variables))

    numerical_variables = df.select_dtypes(include=['float64', 'int64']).columns
    st.write("Number of Numerical Columns", len(numerical_variables))

    bool_variables = df.select_dtypes(include=['bool']).columns
    st.write("Number of Bool Columns", len(bool_variables))

    if show_df:
      st.write(df)

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      #selected_varible = st.selectbox("Select a variable", df.columns.tolist())
      if numerical_column:
        st.subheader("Five Number Summary")
        numerical_data = df[numerical_column]
        summary = numerical_data.describe()
        st.write(summary)

      @st.cache_data
      def convert_df(df):
        return df.to_csv().encode('utf-8')
      
      csv = convert_df(df[numerical_column])

      st.download_button(
        label = "Download Numerical column as CSV",
        data = csv,
        file_name = "Numerical Column.csv",
        mime='text/csv',
        )
      
    #barplot 

    if column_type == "Categorical":
      categorical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['object']).columns)
      
      # Barplot
      choose_color = st.color_picker('Pick a Color', "#C39DEC")
      choose_opacity = st.slider(
        'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      bar_title = st.text_input('Set Title', 'Bar Plot')
      bar_xtitle = st.text_input('Set x-axis Title', categorical_column)
    
      fig, ax = plt.subplots()
      df[categorical_column].value_counts().plot(kind='bar', ax=ax, color=choose_color)
      plt.xlabel(categorical_column)
      plt.ylabel('Count')
      plt.title('Bar Plot')
      
      st.pyplot(fig)

      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      if categorical_column:
        st.subheader("Five Number Summary")
        categorical_data = df[categorical_column]
        summary = categorical_data.describe()
        st.write(summary)