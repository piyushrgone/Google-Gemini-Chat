# Initial imports
import streamlit as st 
import google.generativeai as genai
import google.ai.generativelanguage as glm 
from PIL import Image
import os 
import io 

# Image to byte array
def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr=imgByteArr.getvalue()
    return imgByteArr

# Loading the enviorments 
from dotenv import load_dotenv
load_dotenv() 

# Confugiring Google AI Studio API 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])


# App Layout: 
st.set_page_config(page_title="Chat with Gemini")
st.header(":blue[Google Gemini Chat]")

gemini_text , gemini_vision = st.tabs(["Gemini Pro","Gemini Pro Vision"])

def main():
    
    clear_button = st.button("Clear Page")
    if clear_button:
        st.experimental_set_query_params()  
        
         
    with gemini_text:     
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        input=st.text_input("Input: ",key="input")
        submit=st.button(":blue[Enter]")

        if submit and input:
            response=get_gemini_response(input)
            # Add user query and response to session state chat history
            st.session_state['chat_history'].append(("You", input))
            st.subheader(":blue[Response]")
            response_container = st.container()
            with response_container:
                for chunk in response:
                    st.write(chunk.text)
                    st.session_state['chat_history'].append(("Bot", chunk.text))
        st.subheader(":blue[Chat History]")
            
        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")
        
    with gemini_vision:
        image_prompt = st.text_input("Interact with the Image", placeholder="Prompt", label_visibility="visible")
        uploaded_file = st.file_uploader("Choose and Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)

            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)
            
        if st.button("GET RESPONSE", use_container_width=True):
            model = genai.GenerativeModel("gemini-pro-vision")

            if uploaded_file is not None:
                if image_prompt != "":
                    image = Image.open(uploaded_file)

                    response = model.generate_content(
                        glm.Content(
                            parts = [
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()

                    st.write("")
                    st.write(":blue[Response]")
                    st.write("")

                    st.markdown(response.text)

                else:
                    st.write("")
                    st.header(":red[Please Provide a prompt]")

            else:
                st.write("")
                st.header(":red[Please Provide an image]")
  

if __name__ == "__main__":
    main()