from langchain_community.tools.tavily_search import TavilySearchResults

# 실제로 agent가 호출할 tavily 기능 함수. tavily는 LLM을 위한 검색 엔진임
def get_profile_url_tavily(name: str):
  """Search for Linkedin or Twitter Profile Page."""
  search = TavilySearchResults()
  res = search.run(f"{name}")
  return res # llm을 이용하면 response를 내가 파싱할 것 없이 llm이 해줄 수 있다. 특별히 필드를 뽑는 로직을 실행할 필요가 없음