import os

from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_CHECKPOINT_URI")

if not POSTGRES_URI:
    raise ValueError(
        "POSTGRES_CHECKPOINT_URI is not configured"
    )


def create_checkpointer():
    checkpointer = PostgresSaver.from_conn_string(
        POSTGRES_URI
    )

    checkpointer.setup()

    return checkpointer