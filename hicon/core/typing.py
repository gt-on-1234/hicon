from __future__ import annotations
import typing as ty

import os
import json

DecoderArgType = ty.Optional[ty.Type[json.JSONDecoder]]
EncoderArgType = ty.Type[json.JSONEncoder]

PathArgType = ty.Union[os.PathLike, str]
