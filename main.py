import fastapi
import fastapi.middleware
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from depends import WindowsUser

secret_key = "c3abdfd77555452cbc7cdd2c1720d909"

app = fastapi.FastAPI()

@app.get('/user')
async def user(username:str=fastapi.Depends(WindowsUser)):
    return username

if __name__ == "__main__":
    uvicorn.run(app=app,port=8999)