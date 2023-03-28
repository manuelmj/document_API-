from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import user_create_document

app = FastAPI()
app.include_router(user_create_document.router)


@app.get("/",include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')



