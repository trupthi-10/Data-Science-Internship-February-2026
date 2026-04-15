from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

prompt = PromptTemplate.from_template(
    "Explain why this candidate received score {score} based on match result: {match}"
)

def generate_explanation(score, match):
    return llm.invoke(prompt.format(score=score, match=match)).content
