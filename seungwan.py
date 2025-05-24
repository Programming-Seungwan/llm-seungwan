from langchain_core.prompts import PromptTemplate # 프롬프트를 사용할 수 있게 함
from langchain_openai import ChatOpenAI # 채팅을 할 수 있게 함
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def seungwan_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name = name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile=linkedin_username)

    summary_template = """
    given the linkedin information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
"""

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    # 온도는 모델이 얼마나 창의적일지를 의미. 0은 창의적이지 않음
    # llm = ChatOllama(temperature=0, model="gemma3:4b")
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data})

    print(res)



if __name__ == '__main__':
    load_dotenv()
    print("Hello langchain")

    seungwan_with(name='seungwan kim lawandgood')
