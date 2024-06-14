import openai
import streamlit as st
import streamlit_pills as stp
import firebase_admin
from firebase_admin import auth, exceptions, credentials, initialize_app, firestore
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
from utils import get_logged_in_user_email, remove_citations, update_db
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock 

st.set_page_config(page_title="NRI-Assist", page_icon="🇮🇳")

#Hide header
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize Firebase app
fb_creds = dict(st.secrets["firebase"]['creds'])
cred = credentials.Certificate(fb_creds)

try:
    firebase_admin.get_app()
except ValueError as e:
    initialize_app(cred)

# Initialize Google OAuth2 client
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
redirect_url = "https://nri-assist.streamlit.app/"  # redirect after google login

goa_client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)


#Open AI client
openai_api_key = st.secrets["openai_api_key"]
oai_client = openai.OpenAI(api_key=openai_api_key)
assis_id = st.secrets["assis_id"] #OAI Assistant ID

#Firestore db 
if 'db' not in st.session_state:
        st.session_state.db = ''

db=firestore.client()
st.session_state.db=db

# Get user info
if 'email' not in st.session_state:
    st.session_state['email'] = ''

try:
    if st.session_state.email:
        user_info = db.collection('users').document(st.session_state.email).get()
        if user_info.exists:
            user_info = user_info.to_dict()
        else :
            user_info = {'messages': [], 'msg_count': 1}
            doc_ref = db.collection('users').document(st.session_state.email)
            doc_ref.set(user_info)
except Exception as e:
    print(e)


def show_login_button():
    authorization_url = asyncio.run(goa_client.get_authorization_url(
        redirect_url,
        scope=["email", "profile"],
        extras_params={"access_type": "offline"},
    ))
    st.link_button("Login", authorization_url)

    get_logged_in_user_email(goa_client, redirect_url)


with st.sidebar:
    if not st.session_state.email:
        get_logged_in_user_email(goa_client, redirect_url)
        if not st.session_state.email:
            show_login_button()

    if st.session_state.email:
        # st.write(st.session_state.email)
        if st.button("Logout", type="primary", key="logout_non_required"):
            print('button if statement ')
            st.session_state.email = ''
            st.rerun()

        st.write('⚠️ The AI model may sometimes generate incorrect information; please verify independently.')
    
    



st.header("NRI Assist 🇺🇸 🇮🇳", divider = 'rainbow') 
st.markdown("I am Arvind's **:orange[AI agent]**.\
         Feel free to ask me questions about returning to India.✨ ")


#thread session state
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = oai_client.beta.threads.create().id

#message session srae
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# pills config
suggestions_list = ["Why did you move to India?", "How to evaluate moving to India?", "How to transfer money to India?"]
suggestions_icons = ["🍀", "🎈", "🌈"]
# pills_index = None

# Create the pill component
selected = stp.pills("Quick Questions:", suggestions_list, suggestions_icons, index=None)

# Show existing messages if any...
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = ''

# Handle selection
if selected:
    prompt = selected

# Handle selection
chat_in = st.chat_input()
if chat_in:
    prompt = chat_in

# input from the user
if prompt:

    if not st.session_state.email:
        st.info("Please login to continue.")
        st.stop()

    if user_info['msg_count'] >= 8:
        st.info("Sorry we have reached the token limit. Please reach out to Arvind directly!")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt}) # add to state
    user_collection = db.collection('users').document(st.session_state.email)
    update_db(collection = user_collection, role = 'user', content = prompt, msg_count = user_info['msg_count'])


    # Display the user's query
    with st.chat_message("user"):
        st.markdown(prompt)

    # add the user's message to the existing thread
    oai_client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id, 
        role="user", 
        content=prompt
        )
    
    try:
        with st.spinner("Generating response..."): 
    # Stream the assistant's reply
            with st.chat_message("assistant"):
                stream = oai_client.beta.threads.runs.create(
                    thread_id=st.session_state.thread_id,
                    assistant_id=assis_id,
                    stream=True
                    )
                
                # Empty container to display the assistant's reply
                assistant_reply_box = st.empty()
                
                # A blank string to store the assistant's reply
                assistant_reply = ""

                # Iterate through the stream 
                for event in stream:
                    # Here, we only consider if there's a delta text
                    if isinstance(event, ThreadMessageDelta):
                        if isinstance(event.data.delta.content[0], TextDeltaBlock):
                            # empty the container
                            assistant_reply_box.empty()
                            # add the new text
                            partial_reply = event.data.delta.content[0].text.value
                            assistant_reply += remove_citations(partial_reply)
                            # display the new text
                            assistant_reply_box.markdown(assistant_reply)
                
                if not assistant_reply:
                    st.info("Sorry we have reached the token limit. Please reach out to Arvind directly!")
                    st.stop()

                # Once the stream is over, update chat history
                st.session_state.messages.append({"role": "assistant",
                                                    "content": assistant_reply})
                
                update_db(collection = user_collection, role = 'assistant', content = assistant_reply, 
                        msg_count = user_info['msg_count'])
    except:
        st.info("Sorry we have reached the token limit. Please reach out to Arvind directly!")
        st.stop()
