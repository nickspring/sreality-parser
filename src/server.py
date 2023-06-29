import os

import psycopg2
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from psycopg import Error

app = FastAPI()
connection = None
cursor = None


@app.on_event("startup")
async def startup():
    global connection, cursor

    try:
        connection = psycopg2.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DATABASE"),
        )
        cursor = connection.cursor()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


@app.on_event("shutdown")
async def shutdown():
    global connection, cursor

    cursor.close()
    connection.close()


@app.get("/", response_class=HTMLResponse)
async def root():
    global connection, cursor

    response = """
     <html>
        <head>
            <title>Sreality Parser Results</title>
        </head>
        <body>
            {body}
        </body>
    </html>
    """

    cursor.execute("SELECT title, image FROM ads")
    records = cursor.fetchall()

    response = response.format(
        body="\n".join(
            [
                '<h1>{title}</h1><p><img src="{image}" /></p>'.format(
                    title=row[0],
                    image=row[1],
                )
                for row in records
            ]
        ),
    )

    return response
