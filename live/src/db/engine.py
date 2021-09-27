from sqlmodel import create_engine
from live.src.config import DB_CONFIG


def get_engine():

    url = "postgresql://{user}:{passwd}@{host}:{port}/{db}".format(
        user=DB_CONFIG["db_user"],
        passwd=DB_CONFIG["db_password"],
        host=DB_CONFIG["db_host"],
        port=DB_CONFIG["db_port"],
        db=DB_CONFIG["db_name"],
    )
    engine = create_engine(url=url)

    return engine
