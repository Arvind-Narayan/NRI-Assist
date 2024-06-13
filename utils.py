import re
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
import streamlit as st
from firebase_admin import auth, exceptions, firestore
import datetime

def remove_citations(text):
    #remove citations
    pattern = r'【.*?†source】'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

async def get_access_token(client: GoogleOAuth2, redirect_url: str, code: str):
    return await client.get_access_token(code, redirect_url)

async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email

def get_logged_in_user_email(client: GoogleOAuth2, redirect_url: str):
    st.write('in get_logged_in_user_email ')
    try:
        code = st.query_params['code'] #query_params.get('code')
        st.write('code ' + code)
        if code:
            token = asyncio.run(get_access_token(client, redirect_url, code))
            st.query_params.clear() 

            if token:
                user_id, user_email = asyncio.run(get_email(client, token['access_token']))
                if user_email:
                    try:
                        user = auth.get_user_by_email(user_email)
                    except exceptions.FirebaseError:
                        user = auth.create_user(email=user_email)
                        print("user ",user.display_name)
                    st.session_state.email = user.email
                    return user.email
        return None
    except Exception as e: 
        print(e)
        st.write(e)
        pass

def update_db(collection, role, content, msg_count):
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = {"timestamp" : current_datetime,"role": role, "content": content}
    collection.update({'messages': firestore.ArrayUnion([msg])})

    if role == 'user':
        collection.update({'msg_count' : msg_count+1})