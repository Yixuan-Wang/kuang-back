import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import database as db
from models import Quick, Xiaoyun, Zi

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_xiaoyuns(column_names, result):
    list_xiaoyuns = [Xiaoyun.parse_obj(zip(column_names, xiaoyun)) for xiaoyun in result]
    xiaoyuns = {xiaoyun.xiaoyun_index: xiaoyun for xiaoyun in list_xiaoyuns}
    return xiaoyuns

def generate_zis(column_names, result):
    return [Zi.parse_obj(zip(column_names, zi)) for zi in result]

@app.get("/quick/{s}", response_model=Quick)
async def quick(s: str):
    if len(s) == 1:
        column_names, result = await db.query_zi(zi=s)
        zis = generate_zis(column_names, result)
        column_names, result = await db.query_xiaoyun_from_indices(tuple({zi.xiaoyun_index for zi in zis}))
        xiaoyuns = generate_xiaoyuns(column_names, result)
        return Quick(zis=zis, xiaoyuns=xiaoyuns, mode='zi')
    elif len(s) == 2:
        if s.startswith('-'):
            aw_zi, aw_xy = await asyncio.gather(db.query_zi_from_xiaoyun(xiaoyun=s[1]), db.query_xiaoyun(xiaoyun=s[1]))
            return Quick(zis=generate_zis(*aw_zi), xiaoyuns=generate_xiaoyuns(*aw_xy), mode='zi')
        elif s.endswith('~'):
            column_names, result = await db.query_xiaoyun_from_shangzi(shangzi=s[0])
            xiaoyuns = generate_xiaoyuns(column_names, result)
            return Quick(zis=[], xiaoyuns=xiaoyuns, mode='xiaoyun')
        elif s.startswith('~'):
            column_names, result = await db.query_xiaoyun_from_xiazi(xiazi=s[1])
            xiaoyuns = generate_xiaoyuns(column_names, result)
            return Quick(zis=[], xiaoyuns=xiaoyuns, mode='xiaoyun')
        else:
            column_names, result = await db.query_xiaoyun_from_fanqie(fanqie=s)
            xiaoyuns = generate_xiaoyuns(column_names, result)
            return Quick(zis=[], xiaoyuns=xiaoyuns, mode='xiaoyun')
    elif len(s) == 3:
        if s[1] == '+':
            column_names, result = await db.query_xiaoyun_from_initial_and_yunshe(initial=s[0], yunshe=s[2])
            xiaoyuns = generate_xiaoyuns(column_names, result)
            return Quick(zis=[], xiaoyuns=xiaoyuns, mode='xiaoyun')
        else: return Quick(zis=[], xiaoyuns=[], mode='zi')
    else: return Quick(zis=[], xiaoyuns=[], mode='zi')

app.mount("/", StaticFiles(directory="public", html=True), name="public")
