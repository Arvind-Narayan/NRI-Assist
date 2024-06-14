import streamlit as st
# from utils import hide_github_icon

st.set_page_config(page_title="About", page_icon="🇮🇳")

#hide
# Add custom CSS to hide the GitHub icon
hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

st.header("My Story",divider='rainbow')

col1, col2, col3 = st.columns([1.3 ,0.2, 1])

with col1:
    st.write('ipsum lorem psum lorem psum lorem psum lorem psum lorem psum lorem psum lorem  \
             psum lorem  psum lorem  psum lorem  psum lorem  psum lorem ')
    
    url = 'https://www.linkedin.com/in/arvindna/'
    st.markdown(f"Feel free to reach out with questions or feedback : ")
    # st.markdown(f"###### 🔗 Linkedin: [link](%s)"% url)
    st.markdown(f"###### 🔗 Linkedin: {url}")
    
with col3:
    st.image("./img_arv.jpeg", width=300)


# st.image('./img_arv.jpeg', width = 500 )
# # st.image('./img_arv.jpeg')
# st.title("My Story")

# st.write("About Arvind ....")