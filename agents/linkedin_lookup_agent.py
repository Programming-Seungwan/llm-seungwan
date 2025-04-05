import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool # LLM이 외부 세계와 알아서 api 콜을 하고 디비를 조회하고 하는 작업을 할 수 있는 인터페이스임
from langchain.agents import (create_react_agent, AgentExecutor)
from tools.tools import get_profile_url_tavily


load_dotenv()

from langchain import hub

def lookup(name: str) -> str:
  llm = ChatOllama(
    temperature=0,
    model="gemma3:4b"
  )
  # llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
  template = """
  given the full name {name_of_person} I want your to get it me a link to their LinkedIn profile page.
  Your answer should contain only a URL
  """

  prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

  # 에이전트가 이용할 도구를 말함
  # name : 로그에 나타남, func : 사용할 함수 description : agent에게 어느 상황에 이걸 사용할지 알려주는 것
  tools_for_agent = [Tool(name="Crawl Google 4 linkedin profile page", func=get_profile_url_tavily, description="useful for when you need get the Linkedin Page URL")]

  react_prompt = hub.pull("hwchase17/react") #우리가 사용하는 추론엔진이 됨

  # 에이전트 생성
  agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True) # 실제 agent를 돌리는 런타임

  result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)}) # 기존에는 chain을 만들어서 invoke 해주었는데, 알아서 agent가 실행

  linked_profile_url = result["output"]
  return linked_profile_url

if __name__ == "__main__":
  linkedin_url = lookup("eden marco Udemy")
  print(linkedin_url)