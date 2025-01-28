# Seungwan LLM

## 주요 개념.
1. 프롬프트가 있고, Chatting을 도와주는 클래스가 있는데 이들을 엮어서 chain으로 만든다.
2. 프롬프팅을 하고 받아온 response에는 답변이 content 필드로 와서 이를 참조하면 되는데, 가독성 좋은 글로 보기위해서는 관련 parser들을 이용할 필요가 있다. ex) output parser