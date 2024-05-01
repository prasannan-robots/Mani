import streamlit as st

def main():
    st.title("AI Application")

    # Upload button for file
    uploaded_file = st.file_uploader("Upload File")

    if uploaded_file is not None:
        # Multi selection for selecting columns
        selected_columns = st.multiselect("Select Columns", ["Column 1", "Column 2", "Column 3"])

        # Selection for categories
        selected_category = st.selectbox("Select Category", ["Category 1", "Category 2", "Category 3"])

        # Text area for AI output
        st.subheader("AI Output:")
        ai_output = "This is the output from AI."
        st.write(ai_output)

        # Text area for user questions
        user_question = st.text_area("Ask a question")

        # Download button
        if st.button("Download"):
            # Code for downloading file
            pass

if __name__ == "__main__":
    main()
