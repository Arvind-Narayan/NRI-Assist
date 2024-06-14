import streamlit as st
# from utils import hide_github_icon

st.set_page_config(page_title="About", page_icon="🇮🇳")

#hide
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True)

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