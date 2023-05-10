import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

#   You're working as a professional business man who is doing business with Korean and you're communicating with your Korean business partner via email in Korean language.
#     - Provide your output to Korean language

template = """
 
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the tone, email:
    TONE: {tone}
    EMAIL: {email}
        
    YOUR RESPONSE in the same language as in the input email:
"""

prompt = PromptTemplate(
    input_variables=["tone", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("Globalize Text")

#col1, col2 = st.columns(2)

#with col1:
st.markdown("The application is to improve your email skills by converting your emails into a more professional format. \n\n This tool \
                is powered by [OpenAI](https://openai.com) and modified by Oscar Gu.\n")
st.markdown("该应用旨在通过将您的电子邮件转换为\n 更专业的格式和内容来提升您的电子邮件技巧。\n该工具由OpenAI-GPT模型提供技术支持，并由Oscar Gu进行了模型微调。[韩语版]")

#with col2:
#    st.image(image='TweetScreenshot.png', width=400, caption='https://twitter.com/DannyRichman/status/1598254671591723008')

st.markdown("## Enter Your Email To Convert")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2, col3 = st.columns(3)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like?',
        ('Formal', 'Informal'))
    
#with col2:
#    option_dialect = st.selectbox(
#        'Which English Dialect would you like?',
#        ('American', 'British'))
    
# with col3:
#    option_lang = st.selectbox(
#        'Which Language would you like?',
#        ('EN', 'CN'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Email:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)

    st.markdown("### 韩语版本:")
    llm = load_LLM(openai_api_key=openai_api_key)
    llm.temperature = 0
    korean_lang_content = llm("translate the below content into Korean language. Just provide the translated result and don't provide me any additional content. \n" + formatted_email)
    st.write(korean_lang_content)
