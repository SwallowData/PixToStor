# !/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests

from dotenv import find_dotenv,load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
api_key = 'sk-you_key'
api_base = 'you_url'
def look(i):
    print(type(i))
    print(i)
def img2text(url):
    #loade ai model
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": "Bearer you_hf_key"}
    #you proxies if you have proxies
    proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}
    with open(url, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data, proxies=proxies)
    return response.json()[0]['generated_text']
def generate_story(scenario,topic):
    m_word = {'科技':'technology','生活':'life','创意':'originality'}
    topic = m_word[topic]
    print(topic)
    template = """
    you are a story teller;
    you can generate a short story based on a simple narrative, the story should be no more than 200 words;
    you generate a short story topic is {topic}
    you answered in Chinese;
    CONTEXT:{scenario}
    STORY:
    """
    prompt = PromptTemplate(template = template,input_variables = ['scenario','topic'])
    story_llm = prompt | ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=1,
        base_url=api_base,
        api_key=api_key,
        openai_proxy='http://localhost:7890'
    )
    print("story_llm:",story_llm)
    story = story_llm.invoke(input={'scenario':scenario,'topic':topic})
    print("story:",story)
    return story.content
def translation(body):
    prompt = PromptTemplate(template='''Please convert the following characters to Chinese;
                                        Only output Chinese 
                                        CONTEXT:{body}
                                        '''
                            , input_variables=['body'])
    story_llm = prompt | ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=1,
        base_url=api_base,
        api_key=api_key,
        openai_proxy='http://localhost:7890'
    )
    story = story_llm.invoke(input={'body':body})
    print("story:",story)
    return story.content
def run():
    st.set_page_config(page_title='图片想象',page_icon='🤗')
    st.header('把图片变成故事')
    uploaded_file = st.file_uploader('选择图片...',type='jpg')
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open(uploaded_file.name,'wb') as file:
            file.write(bytes_data)
        st.image(uploaded_file,caption='加载图片中...',
                 use_column_width=True
                 )
        scenario = translation(img2text(uploaded_file.name))
        topic = st.selectbox(
            label='请输入您的主题',
            options=('科技', '生活', '创意'),
            index=2,
            format_func=str,
        )
        with st.expander('场景'):
            st.write(scenario)
        # scenario = 'chain hiphop'
        story = generate_story(scenario,topic = topic )
        with st.expander('故事'):
            st.write(story)
if __name__ == '__main__':
    run()