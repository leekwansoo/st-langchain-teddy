## OPENAI_API_KEY
import os

OPENAI 의 API_KEY 를 갖고 오는 2 개의 방식이 있음
방식 1. secrets.toml 에서 가져오는 방법: 
  open_api_key = st.secrets["OPENAI_API_KEY"]
  os.environ["OPENAI_API_KEY"] = open_api_key
  secrets.toml 에 저장되어 있는 form
  OPENAI_API_KEY = "your_key"
방식2. .env file 에서 가져오는 방법
  open_api_key = os.getenv("OPENAI_API_KEY")
  os.environ["OPENAI_API_KEY"] = open_api_key
  .env 에 저장되어 있는 form
  OPENAI_API_KEY = your_key  (quotation mark 가 없음)

