import streamlit as st

placeholder = st.empty()
temp = placeholder.title("Your console needs input, please look at the terminal.")
sys_name = input("System Name (Leave blank to keep system name from last session): ")

if sys_name != "":
    sys_file = open("sys_name.txt", "w")
    sys_file.write(sys_name)
    sys_file.close()
    print("Workspace Initialized, Editor Open")
else:
    sys_name = open("sys_name.txt", "r").read()
    print("Workspace Initialized, Editor Open")

placeholder.empty()
st.title("🌎Astraeus: Editing " + sys_name)
