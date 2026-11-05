
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class Settings(BaseSettings):

    default_timezone: str = Field(
        default="Asia/Kolkata",
        validation_alias="DEFAULT_TIMEZONE"
    )

    default_date_format: str = Field(
        default="%Y-%m-%d",
        validation_alias="DEFAULT_DATE_FORMAT"
    )

    default_time_format: str = Field(
        default="%H:%M:%S",
        validation_alias="DEFAULT_TIME_FORMAT"
    )

    week_starts_on: int = Field(
        default=0,
        ge=0,
        le=6,
        validation_alias="WEEK_STARTS_ON"
    )

    max_date_range_days: int = Field(
        default=366,
        ge=1,
        validation_alias="MAX_DATE_RANGE_DAYS"
    )

    max_list_days: int = Field(
        default=366,
        ge=1,
        validation_alias="MAX_LIST_DAYS"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("default_timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError(f"Invalid timezone: {value}")

        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
