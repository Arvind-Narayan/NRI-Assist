import streamlit as st

st.set_page_config(page_title="About", page_icon="🇮🇳")

st.header("About Me",divider='rainbow')

col1, col2, col3 = st.columns([1.3 ,0.2, 1])

with col1:
    st.write('ipsum lorem psum lorem psum lorem psum lorem psum lorem psum lorem psum lorem  \
             psum lorem  psum lorem  psum lorem  psum lorem  psum lorem ')
    
with col3:
    st.image("./img_arv.jpeg", width=360)


# st.image('./img_arv.jpeg', width = 500 )
# # st.image('./img_arv.jpeg')
# st.title("My Story")

# st.write("About Arvind ....")