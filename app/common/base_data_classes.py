from typing import Annotated

from pydantic import BeforeValidator


def strip_string(value: str) -> str:
    return value.strip()


def title_string(value: str) -> str:
    return value.strip().title()


StrippedString = Annotated[str, BeforeValidator(strip_string)]
TitledString = Annotated[str, BeforeValidator(title_string)]
