from typing import Literal
from database import query_xiaoyun_from_shangzi
from pydantic import BaseModel

class Xiaoyun(BaseModel):
    xiaoyun_index : int
    xiaoyun       : str
    initial       : str
    final         : str
    rhyme         : str
    fanqie        : str
    page_ref      : str
    shangzi       : str
    xiazi         : str

    tone_num      : int
    deng          : int
    hu            : str
    yunxi         : str
    yunshe        : str

class Zi(BaseModel):
    zi            : str
    xiaoyun_index : int
    zi_num        : int
    zi_def        : str

class Quick(BaseModel):
    zis           : list[Zi]
    xiaoyuns      : dict[int, Xiaoyun]
    mode          : Literal['zi', 'xiaoyun']
