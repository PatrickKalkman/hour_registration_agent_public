import os
from typing import List
from todoist_api_python.api import TodoistAPI
from loguru import logger


def task_fetcher_node(state):
    api = initialize_todoist_api()
    print(state)
    customer_name = state["customer_name"]
    logger.info(f"Fetching tasks for customer {customer_name}...")
    project_id = get_project_id(api, customer_name)
    done_section_id = get_done_section(api, project_id)
    tasks = get_sections_tasks(api, done_section_id)
    task_descriptions = [task.content for task in tasks]
    return {"task_descriptions": task_descriptions}


def initialize_todoist_api():
    api_token = os.getenv('TODOIST_API_KEY')
    if not api_token:
        logger.error("TODOIST_API_KEY is not set.")
        raise ValueError("API token for Todoist is not set in environment variables.")
    return TodoistAPI(api_token)


def get_project_id(api, project_name: str) -> str:
    logger.info("Getting projects for project ID...")
    projects = api.get_projects()
    for project in projects:
        if project_name.lower() in project.name.lower():
            return project.id
    raise ValueError("Project ID not found.")


def get_done_section(api, project_id: str) -> str:
    logger.info(f"Getting sections for done section from project with ID {project_id}")
    sections = api.get_sections(project_id=project_id)
    for section in sections:
        if "done" in section.name.lower():
            return section.id
    raise ValueError("Done section not found.")


def get_sections_tasks(api, section_id: str) -> List[str]:
    logger.info(f"Getting tasks for section with ID {section_id}")
    tasks = api.get_tasks(section_id=section_id)
    return [task for task in tasks if task.section_id == section_id]
