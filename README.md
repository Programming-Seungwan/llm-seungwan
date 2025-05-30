# Seungwan LLM

## 주요 개념.

1. 프롬프트가 있고, Chatting을 도와주는 클래스가 있는데 이들을 엮어서 chain으로 만든다.
2. 프롬프팅을 하고 받아온 response에는 답변이 content 필드로 와서 이를 참조하면 되는데, 가독성 좋은 글로 보기위해서는 관련 parser들을 이용할 필요가 있다. ex) output parser

## Agent란?

기존의 API나 데이터베이스 등의 리소스에 접근해서 얻어낸 데이터를 LLM에 던져주는 작업은 프로그래머가 스크립트로 짜주거나 해야했다. 이를 알아서 잘 해주는 게 바로 에이전트이다.<br/>
근데 이 에이전트 역시 내부적으로는 LLM 기술로 이루어져 있음. 현재의 AI 애플리케이션을 구현하는 데에는 다음의 세 기술의 융합체로서 이루어진다.

- LLM : Bert, GPT, claude sonnet, gemini 와 같은 트랜스포머 아키텍쳐를 기반으로 만들어진 언어 모델임
- RAG : 모델들이 사전 학습된 데이터만으로는 사용자에게 의미 있는 결과를 내놓기 어려우므로 문서를 검색하는 행위를 의미한다.
- AI Agent : 위의 설명. 문제 상황을 하위 문제로 쪼개고, 계획을 하고 알맞은 LLM 활용을 해나가는 소프트웨어.
- tool : agent(여기에서는 LLM을 말함)가 서드 파티 앱과 상호작용하기 위한 장치. tavily는 LLM이 웹 검색을 하기 위한 일종의 검색 엔진임

## Tool과 ReAct

```python
tools_for_agent = [Tool(name="Crawl Google 4 linkedin profile page", func=get_profile_url_tavily, description="useful for when you need get the Linkedin Page URL")]

```

위의 코드처럼 agent가 상황에 맞춰 사용할 함수를 적어주는 것이다. name과 description은 좀 더 LLM이 이를 효과적으로 사용할 수 있도록 context를 제공하는 것이라고 생각하면 된다.

- 추론 엔진 : 현재 본 프로젝트에서는 `hwchase17/react` 라는 추론 엔진을 사용하고 있는데 이건 그 자체로 LLM이 아니다. 오히려 랭체인 프레임워크를 사람들이 활용할 때 내부적으로 도는 LLM이 작업을 좀더 효율적으로 수행할 수 있도록 연구 결과로 알아낸 개쩌는 문자열 템플릿 리터럴 지침서 정도의 개념이다.

- agent : 일종의 LLM 프로젝트를 돌리는 **시스템 태스크 러너** 개념이라고 보면 된다. 이게 없으면 LLM은 혼자서 툴을 가지고 뭘 못한다. 랭체인 개발도 두 시기 정도로 나뉘는데, 기존에는 개발자가 chain 파이프라인을 직접 구성해주었지만, agent 개념이 나온 뒤로는 이것도 자동화할 수 있다는 것이다.

> LLM은 그래봤자 그냥 텍스트를 읽어들이고, 텍스트를 뱉어내는 로보트에 불과한 개념이다. 에이전트는 이를 활용해 LLM의 언어 능력을 "행동"으로 연계하는 시스템 소프트웨어 아키텍쳐 개념에 해당한다.

### 프로젝트 설명

1. 사용자의 스크래핑 input에 따라서 알맞은 linkedIn 유저를 찾아야 함 -> `linkedin_lookup_agent` 에이전트를 이용해서 이름에 알맞는 linkedin 주소를 tavily 엔진으로 찾는다. 이걸 반환!(이떄 agent, 추론 엔진, tool 개념 동반)
2. 반환된 linkedIn 주소를 가지고 proxyCurl API로 링크드인 데이터를 받는다. 이걸 json 양식으로 반환
3. 이걸 다시 LLM이 요약할 수 있게!

### Tavily

기존의 chrome, firefox 같은 브라우저 내부에서 사용되는 검색 엔진은 결국 사람이 보기 위한 것이므로 html, css, js를 받아오는 과정을 거친다. 하지만 LLM이 검색을 대신 해주는 것은 이런 점들이 필요 없기 때문에 그냥 JSON 포맷으로 데이터를 받아오면 된다. 따라서 이에 최적화된 tavily API를 이용하는 것이다.
