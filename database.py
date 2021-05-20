import aiosqlite

def column_names(tuple_desc: tuple[tuple]) -> tuple[str]:
    return tuple((tup[0] for tup in tuple_desc))

async def query_zi(zi: str):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute('''
            SELECT * FROM zi
            WHERE zi = :zi;
            ''', {'zi': zi}) as cur:
            return column_names(cur.description), await cur.fetchall()

async def query_xiaoyun(xiaoyun: str):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute('''
            SELECT * FROM v_xiaoyun
            WHERE xiaoyun = :xiaoyun;
            ''', {'xiaoyun': xiaoyun}) as cur:
            return column_names(cur.description), await cur.fetchall()

async def query_zi_from_xiaoyun(xiaoyun: str):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute('''
            SELECT * FROM zi
            WHERE xiaoyun_index IN (
                SELECT xiaoyun_index FROM v_xiaoyun
                WHERE xiaoyun = :xiaoyun
                );
            ''', {'xiaoyun': xiaoyun}) as cur:
            return column_names(cur.description), await cur.fetchall()

async def query_zi_from_xiaoyun_index(xiaoyun_index: int):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute('''
            SELECT * FROM zi
            WHERE xiaoyun_index = :xiaoyun_index;
            ''', {'xiaoyun_index': xiaoyun_index}) as cur:
            return column_names(cur.description), await cur.fetchall()

async def query_xiaoyun_from_indices(list_xiaoyun_index: list[int]):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute(f'''
            SELECT * FROM v_xiaoyun
            WHERE xiaoyun_index IN ({','.join(map(str,list_xiaoyun_index))});
            ''') as cur:
            return column_names(cur.description), await cur.fetchall()

async def query_xiaoyun_from_fanqie(fanqie: str):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute('''
            SELECT * FROM v_xiaoyun
            WHERE fanqie = :fanqie
            ''', {'fanqie': fanqie}) as cur:
            return column_names(cur.description), await cur.fetchall()

async def query_xiaoyun_from_shangzi(shangzi: str):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute('''
            SELECT * FROM v_xiaoyun
            WHERE shangzi = :shangzi
            ''', {'shangzi': shangzi}) as cur:
            return column_names(cur.description), await cur.fetchall()

async def query_xiaoyun_from_xiazi(xiazi: str):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute('''
            SELECT * FROM v_xiaoyun
            WHERE xiazi = :xiazi
            ''', {'xiazi': xiazi}) as cur:
            return column_names(cur.description), await cur.fetchall()

async def query_xiaoyun_from_initial_and_yunshe(initial: str, yunshe: str):
    async with aiosqlite.connect('kuang.db') as db:
        async with db.execute('''
            SELECT * FROM v_xiaoyun
            WHERE initial = :initial AND yunshe LIKE :yunshe
            ''', {'initial': initial, 'yunshe': yunshe}) as cur:
            return column_names(cur.description), await cur.fetchall()
