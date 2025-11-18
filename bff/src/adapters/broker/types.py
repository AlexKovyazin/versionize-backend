from datetime import datetime
from decimal import Decimal
from typing import TypeAlias, Sequence

from pydantic import BaseModel

JsonDecodable: TypeAlias = bool | bytes | bytearray | float | int | str | None
SendableArray: TypeAlias = Sequence["SendableMessage"]
SendableMessage: TypeAlias = (
        JsonDecodable
        | Decimal
        | datetime
        | BaseModel
        | SendableArray
        | None
)
