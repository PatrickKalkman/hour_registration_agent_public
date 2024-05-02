import datetime
import os
from loguru import logger


def customer_name_node(state):
    CUSTOMER1 = os.getenv("CUSTOMER1")
    CUSTOMER2 = os.getenv("CUSTOMER2")
    weekday = datetime.datetime.now().weekday()
    customer_name = CUSTOMER1 if weekday < 3 else CUSTOMER2
    logger.info(f"Customer name for today (weekday {weekday}) is {customer_name}.")
    return {"customer_name": customer_name}
