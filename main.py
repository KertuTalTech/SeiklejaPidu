import streamlit as st
from langchain import PromptTemplate
#from langchain.llms import OpenAI #so vananenud rida ning asendatud allolevaga
from langchain_community.llms import OpenAI
import os

template = """
 You are a marketing copywriter with 20 years of experience. You are analyzing customer's background to write personalized service description that only this customer will receive; 
    PRODUCT input text: {content};
    CUSTOMER child´s age group (y): {agegroup};
    CUSTOMER main interest: {interest};
    TASK: Write a marketing text for service description that is tailored into this customer's child´s age group and interest. Use age group specific slang.;
    FORMAT: Present the result in the following order: (SERVICE DESCRIPTION), (BENEFITS), (OPTIONS);
    SERVICE DESCRIPTION: describe the service in 5 sentences;
    BENEFITS: describe in 3 sentences why this service is perfect considering customer´s child´s age group and interest;
    OPTIONS: Provide a story in 5 sentences, of an example options of extra activities at the party taking into account interest {interest} and child´s age {agegroup};
"""

prompt = PromptTemplate(
    input_variables=["agegroup", "interest", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personaliseeritud turundusteksti konverter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Otstarve: turundustekstide personaliseerimine igale kliendile või kliendigruppidele; väljundtekst on kohandatud kliendi a) lapse vanuserühmaga ja b) huvidega; sisendtekstiks on neutraalses vormis teenuse kirjeldus. \
    \n\n Kasutusjuhend: 1) valmista ette teenuste kirjeldused (sisendtekst). 2) määra klientide sihtrühmad lähtuvalt nende laste vanuserühma ja huvide kombinatsioonidest. 3) sisesta ükshaaval kliendi sihtrühmade lõikes eeltoodud info äpi kasutajaliideses, saada ära. \
    4) kopeeri ükshaaval sihtgruppide lõikes äpi väljundteksti kõnealuse teenuse tutvustuslehele.")

with col2:
    st.image(image='Väike Seikleja logo.jpg', caption='Cozy and stylish playroom for your little ones')

st.markdown("## Enter Your Content To Convert")

def get_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return openai_api_key
    # If OPENAI_API_KEY environment variable is not set, prompt user for input
    input_text = streamlit.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_agegroup = st.selectbox(
        'Which age group would you like your content to target?',
        ('0-1', '2-3', '4-5', '6-7'))
    
def get_interest():
    input_text = st.text_input(label="Customers main interest", key="interest_input")
    return input_text

interest_input = get_interest()

def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "children parties, playmornings, ages 0-7, personalised activities"

st.button("*GENERATE TEXT*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)

st.markdown("### Your customer tailored content:")

if content_input:
#    if not openai_api_key:
#        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
#        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(agegroup=option_agegroup, interest=interest_input, content=content_input)

    formatted_content = llm(prompt_with_content)

    st.write(formatted_content)
