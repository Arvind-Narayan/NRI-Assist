import streamlit as st
# from utils import hide_github_icon

st.set_page_config(page_title="About", page_icon="🇮🇳")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header("About me",divider='rainbow')

col1, col2, col3 = st.columns([1.3 ,0.2, 1])

with col1:
    with open('about_me.txt') as f:
        st.write(f.read())
    
    url = 'https://www.linkedin.com/in/arvindna/'
    st.markdown(f"So please feel free to reach out to me directly with :orange[questions] or :orange[feedback] : ")
    # st.markdown(f"###### 🔗 Linkedin: [link](%s)"% url)
    st.markdown(f"###### 🔗 Linkedin: {url}")
    
with col3:
    st.image("./img_arv.jpeg", width=300)


# st.image('./img_arv.jpeg', width = 500 )
# # st.image('./img_arv.jpeg')
# st.title("My Story")

# st.write("About Arvind ....")