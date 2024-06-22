import streamlit as st
import requests

def main():
    st.title("File Uploader and Service Status")

    # Create a file uploader widget that accepts both CSV and Excel files
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        try:
            # Display the file type and details
            st.write(f"Uploaded file details: {uploaded_file}")
            st.write(f"File type: {type(uploaded_file)}")

            # Send file to backend for processing
            files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post('http://127.0.0.1:5000/process', files=files)

            if response.status_code == 200:
                st.success("Service monitoring and logging completed.")
                st.write(f"Logs are saved to {response.json()['log_file_path']}")
            else:
                st.error(f"Error: {response.json()['error']}")

        except Exception as e:  
            st.error(f"Error processing the file: {e}")

if __name__ == "__main__":
    main()
