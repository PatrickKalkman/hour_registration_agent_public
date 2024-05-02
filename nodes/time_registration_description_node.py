from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

MODEL_NAME = "Llama3-8b-8192"
REGISTRATION_KEY = "registration_description"


def time_registration_description_node(state):
    GROQ_LLM = ChatGroq(model=MODEL_NAME)

    task_descriptions = state.get("task_descriptions")
    if task_descriptions is None:
        raise ValueError("Missing task descriptions in the state.")

    task_combination_prompt = PromptTemplate(
        template="""\
        system
        You are an expert at writing task descriptions for the registration of working hours in accounting.
        Multiple task descriptions are given to you, and you are asked to combine them into a cohesive description
        string. Return only the generated description using JSON with a single key called 'registration_description'.
        Do not return any other string.

        user
        TASK_DESCRIPTIONS: {task_descriptions}

        assistant""",
        input_variables=["task_descriptions"],
    )

    task_combination_generator = task_combination_prompt | GROQ_LLM | JsonOutputParser()

    description_data = task_combination_generator.invoke({"task_descriptions": task_descriptions})
    registration_description = description_data.get(REGISTRATION_KEY)
    if registration_description is None:
        raise ValueError("Failed to generate the registration description.")

    return {REGISTRATION_KEY: registration_description}
