from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
from typing import List

class Segment(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class Rectangle(BaseModel):
    id: int
    center_x: float
    center_y: float
    width: float
    height: float
    rotation: float
    pAx: float
    pAy: float
    pBx: float
    pBy: float
    pCx: float
    pCy: float
    pDx: float
    pDy: float
    min_x: float
    max_x: float
    min_y: float
    max_y: float


app = FastAPI()

async def get_db_connection():
    return await asyncpg.connect(
        user='sfrfivyh',
        password='uT0xQahWmPQ8YD1ZOSmf7JSrDdz0dU7U',
        database='sfrfivyh',
        host='cornelius.db.elephantsql.com',
        ssl='require'
    )

@app.get("/test_db")
async def test_db():
    try:
        conn = await get_db_connection()
        rows = await conn.fetch("SELECT * FROM rectangles LIMIT 10")
        await conn.close()
        return {"data": rows}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/intersections", response_model=List[Rectangle])
async def find_intersections(segment: Segment):
    conn = await get_db_connection()

    try:
        segment_max_x = max(segment.x1, segment.x2)
        segment_min_x = min(segment.x1, segment.x2)
        segment_max_y = max(segment.y1, segment.y2)
        segment_min_y = min(segment.y1, segment.y2)
        query = f"""
        SELECT * FROM rectangles
        WHERE min_x <= {segment_max_x} AND max_x >= {segment_min_x}
          AND min_y <= {segment_max_y} AND max_y >= {segment_min_y}
        """
        rows = await conn.fetch(query)
        rectangles = [Rectangle(**dict(row)) for row in rows]
        return rectangles
    except Exception as exc:
        await conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()




