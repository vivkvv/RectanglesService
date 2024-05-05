from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg
from typing import List
from shapely.geometry import LineString, Polygon, box


class Point(BaseModel):
    x: float
    y: float

class Segment(BaseModel):
    start: Point
    end: Point

class Rectangle(BaseModel):
    rectangleid: int
    centerx: float
    centery: float
    width: float
    height: float
    rotation: float
    pax: float
    pay: float
    pbx: float
    pby: float
    pcx: float
    pcy: float
    pdx: float
    pdy: float
    minx: float
    maxx: float
    miny: float
    maxy: float


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_rectangle_edges(row):
    return [
        LineString([(row['pax'], row['pay']), (row['pbx'], row['pby'])]),
        LineString([(row['pbx'], row['pby']), (row['pcx'], row['pcy'])]),
        LineString([(row['pcx'], row['pcy']), (row['pdx'], row['pdy'])]),
        LineString([(row['pdx'], row['pdy']), (row['pax'], row['pay'])])
    ]

# in real app those parameters must lay in system variables
async def get_db_connection():
    return await asyncpg.connect(
        user='sfrfivyh',
        password='uT0xQahWmPQ8YD1ZOSmf7JSrDdz0dU7U',
        database='sfrfivyh',
        host='cornelius.db.elephantsql.com',
        ssl='require'
    )

@app.post("/intersections", response_model=List[Rectangle])
async def find_intersections(segment: Segment):
    conn = await get_db_connection()

    try:
        x1, y1 = segment.start.x, segment.start.y
        x2, y2 = segment.end.x, segment.end.y

        segment_max_x = max(x1, x2)
        segment_min_x = min(x1, x2)
        segment_max_y = max(y1, y2)
        segment_min_y = min(y1, y2)

        query = """
        SELECT * FROM rectangles
        WHERE minx <= $1 AND maxx >= $2
        AND miny <= $3 AND maxy >= $4
        """
        rows = await conn.fetch(query, segment_max_x, segment_min_x, segment_max_y, segment_min_y)

        segment_line = LineString([(x1, y1), (x2, y2)])

        filtered_rectangles = []
        for row in rows:
            edges = get_rectangle_edges(row)
            if any(segment_line.intersects(edge) for edge in edges):
                filtered_rectangles.append(Rectangle(**dict(row)))

        return filtered_rectangles
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        await conn.close()

@app.get("/")
async def main():
    return {"message": "Rectangles Demo"}




