import logging
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


class ApplicationSettings(BaseSettings):
    class Config:
        env_prefix = "FILE_MANIPULATOR_"

    logger_level: int = Field(logging.DEBUG)

    input_file_ext: str = Field(".rec")
    output_30r_file_ext: str = Field(".30rec")
    output_300r_file_ext: str = Field(".300rec")


@lru_cache()
def get_settings() -> ApplicationSettings:
    load_dotenv()
    return ApplicationSettings()
