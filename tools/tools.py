from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
  """Search for Linkedin or Twitter Profile Page."""
  search = TavilySearchResults()
  res = search.run(f"{name}")
  return res # llm을 이용하면 response를 내가 파싱할 것 없이 llm이 해줄 수 있다.