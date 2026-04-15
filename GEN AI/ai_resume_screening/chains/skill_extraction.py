from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

prompt = PromptTemplate.from_template(
    "Extract skills, tools, and experience from this resume:\n{resume}"
)

def extract_skills(resume):
    return llm.invoke(prompt.format(resume=resume)).content
