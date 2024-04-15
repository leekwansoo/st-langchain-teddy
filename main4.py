import streamlit as st 
import os 
from openai import OpenAI

# API Key 설정
#open_api_key= os.getenv("OPENAI_API_KEY")
open_api_key= st.secrets["OPENAI_API_KEY"]
#print(open_api_key)
os.environ["OPENAI_API_KEY"] = open_api_key
from utils import print_messages
from utils import StreamHandler

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import ChatMessage

st.set_page_config(page_title="ChatGPT", page_icon="")
st.title("ChatGPT")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# chatting 대화기록 저장하는 store 세션
if "store" not in st.session_state:
    st.session_state["store"] = dict()
    
# 이전 대화 기록 프린트    
print_messages()

store = {}
# session ID로 세션기록을 가져오는 함수
def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    #print(session_ids)
    if session_ids not in st.session_state["store"]: 
        # 새로운 ChatMessageHistory 객체 생성하여 store에 저장함
        st.session_state["store"][session_ids] = ChatMessageHistory()
    return st.session_state["store"][session_ids] # 해당 세션 ID 에 대한 세션기록 반환해줌

if user_input := st.chat_input("Enter your message"):
    # 사용자가 입력한 내용
    st.chat_message("user").write(f'{user_input}')
    #st.session_state["messages"].append(("user", user_input)) # append as tuple
    st.session_state["messages"].append(ChatMessage(role = "user", content = user_input)) 
    
          
    # AI의 답변
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        
        # LLM을 사용하여 AI 답변 생성
        #1. llm model 생성
        llm = ChatOpenAI(streaming=True, callbacks=[stream_handler])
        
        #2. prompt 생성
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                "질문에 대하여 간결하게 답변해 주세요.",
                ),
                # 대화기록을 변수로 사용, history가 MessageHistory의 key가 됨
                MessagesPlaceholder(variable_name = "history"),
                ("human", "{question}"), # 사용자의 질문을 입력
            ]
        )
        chain = prompt | llm
        #response = chain.invoke({"question": user_input}) 
        
        chain_with_memory = (
        RunnableWithMessageHistory( # RunnableWithMessageHistory 객체 생성
            chain, # 실행할 runnable 객체
            get_session_history, # session history 가져오는 함수
            input_messages_key = "question", # 사용자 질문을 key로 입력함
            history_messages_key = "history"
            )
        )
        
        response = chain_with_memory.invoke(
            {"question": user_input},
            # 설정정보: 세션 ID: abc1234 
            config = {"configurable": {"session_id": "abc1234"}},
            
        )
        msg = response.content
        #msg = chain.invoke({"question": user_input}) # pipelining
        #st.write(msg)
        st.session_state["messages"].append(ChatMessage(role = "assistant", content = msg)) # append as tuple
