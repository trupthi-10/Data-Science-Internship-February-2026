from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

prompt = PromptTemplate.from_template(
    "Compare extracted skills with job description and return matching percentage:\nSkills:{skills}\nJD:{jd}"
)

def match_skills(skills, jd):
    return llm.invoke(prompt.format(skills=skills, jd=jd)).content
