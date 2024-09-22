import streamlit as st
import os
import re

# Constants and Variables
# Non-validating pattern IPv4s including defanged addresses with optional 1-5 port suffix
IPV4_REGEX_PATTERN = r"(\b([0-9]{1,3}(\.|\[\.\]){0,1}){4}(\:{1}[0-9]{1,5}){0,1}\b)"
MD5_REGEX_PATTERN = r"(\b[0-9a-f]{32}\b)"

uploaded_files = []
file_data = {}
extracted_iocs = {
    "ipv4": [],
    "ipv6": [],
    "md5": [],
    "sha1": [],
    "sha256": [],
}

# ////////// Upload Container //////////
upload_container = st.container(
    border=True,
)
with upload_container:
    st.write("Upload your IoCs Here")

    uploaded_files = st.file_uploader(
        label="Upload IoCs",
        type=["txt", "doc", "docx"],
        accept_multiple_files=True,
        help="This is the file upload tooltip",
    )

# ////////// Contents Container //////////
contents_container = st.container(
    border=True,
)
with contents_container:
    st.write("Uploaded File Contents")
    st.write(file_data)


# ////////// Extracted Container //////////
extracted_container = st.container(
    border=True,
)
with extracted_container:
    st.write("Extracted IoCs")
    st.write(f"{extracted_iocs}")


# ////////// Core Logic //////////
# NOTE: core logic needs to update the view after processing
# Read file contents
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write(f"File: {uploaded_file.name}")
    # st.write(bytes_data.decode("utf-8"))
    # file_data.append(bytes_data.decode())
    file_data[uploaded_file.name] = bytes_data.decode()

# if file_data:
#     os.write(1,f"{file_data[0]}".encode())

# Extract IoCs from file contents
for file_name, file_contents in file_data.items():

    # IPv4
    ipv4_match_groups = re.findall(
        IPV4_REGEX_PATTERN, 
        file_contents, 
        re.IGNORECASE,
        )
    # os.write(1,f"{ipv4_match_groups}\n".encode())
    # Each item in this match group is a tuble with sub groups
    ipv4_matches = [i[0] for i in ipv4_match_groups]
    # os.write(1,f"{ipv4_matches}\n".encode())
    extracted_iocs["ipv4"] += ipv4_matches

    # MD5
    md5_match_groups = re.findall(
        MD5_REGEX_PATTERN,
        file_contents,
        re.IGNORECASE,
    )
    # Each item in this match group is a string (no subgroups)
    os.write(1,f"{md5_match_groups}\n".encode())
    md5_matches = [i for i in md5_match_groups]
    extracted_iocs["md5"] += md5_matches

extracted_container.write(extracted_iocs)


# def main():
#     is_app_running = False
#     os.write(1,f"App running: {is_app_running}\n".encode())

#     data_load_state = st.text("Waiting for IoCs...")

#     data = st.file_uploader(
#         label="Upload IoCs",
#         type=["txt", "doc", "docx"],
#         accept_multiple_files=True,
#         help="This is the file upload tooltip",
#     )
#     os.write(1,b"{}.format(data)")
#     if data:
#         os.write(1,b"There is now data!")
#         data_load_state.text = "There is now data!"

# def print_message():
#     x = "this is a print statement"
#     os.write(1,b'Something was executed.\n')
    
# def print_file_upload_message():
#     os.write(1,b"Files were uploaded:\n")

# # st.button(
# #     label="Click Me",
# #     on_click=print_message(),
# # )


# if __name__ == "__main__":
#     main()