import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse

from app.api.endpoints.books import books_route
from app.api.endpoints.log_in import login_route
from app.api.endpoints.registration import registration_route
from app.common.logger import logger
from app.db.database import database

logger.info('Starting logger')
index_file = Path(Path(__file__).parent, 'app', 'indexes', 'index.html')

app = FastAPI()

app.include_router(books_route, prefix='/books')
app.include_router(login_route, prefix='/login')
app.include_router(registration_route, prefix='/registration')


@app.on_event('startup')
async def startup_database():
    await database.connect()


@app.on_event('shutdown')
async def shutdown_database():
    await database.disconnect()


@app.get('/')
def root():
    return FileResponse(index_file)


# TO DEBUG uncomment and use this
if __name__ == '__main__':
    port = os.getenv('APP_PORT', 8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
