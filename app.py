#%% packages
#%% packages
import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field
from enum import Enum
from pprint import pprint

from pathlib import Path
 
os.getcwd()
os.chdir(Path(__file__).resolve().parent)
print("Working directory:", Path.cwd())
 
#%% Definiere eine Enum-Klasse für die möglichen Kategorien
class EmailCategory(str, Enum):
    AUSLAND = "Ausland"
    HILFSMITTEL = "Hilfsmittel"
    KRANKENGELD = "Krankengeld"
    KRANKENHAUS = "Krankenhaus"
    SONSTIGES = "Sonstiges"
 
class ComplexityCategory(str, Enum):
    COMPLEX = "Complex"
    NONCOMPLEX ="Non-Complex"
 
class EmailSorter(BaseModel):
    category: EmailCategory = Field(
        ...,
        description="Kategorie, in die die Email einzuordnen ist."
    )
    complexity: ComplexityCategory = Field(..., description="Jede E-Mail sollte als komplex oder nicht-komplex kategorisiert werden")
 
parser = PydanticOutputParser(pydantic_object=EmailSorter)
 
#%% prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Du bearbeitest Emails und kannst sie entsprechenden Kategorien zuordnen. Die Kategorien findest du in der Formatbeschreibung. {format_instruction}"),
    ("user", "Email: {email_content}")
]).partial(format_instruction=parser.get_format_instructions())
 
 
#%% Modellinstanz erstellen
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
# model = ChatOllama(model="gemma3:4b", temperature=0)
 
#%% develop the chain
chain = prompt_template | model | parser
 
#%%
st.title("Emailklassifizierer")
user_input = st.text_area(label="Emailinhalt", placeholder="Hier können Sie Ihren Inhalt einfügen.", height=200)
 
if user_input:
    res = chain.invoke({"email_content": user_input})
    str.write("Ergebnis:")
    st.write(str(res.category))
    st.write(str(res.complexity))
 #%%
 
