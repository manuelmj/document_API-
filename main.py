from fastapi.responses import (RedirectResponse, 
                               PlainTextResponse)

from fastapi import (FastAPI,
                     Request)

from datetime import (datetime, 
                      timedelta)

from routes import (user_create_document,
                    cookie_session)

from validation.cookie_validation import sessions,SESSION_EXPIRE_TIME
from validation.file_validation import (pdf_file_sessionClose_delete,
                                        image_file_sessionClose_delete)

app = FastAPI()
app.include_router(cookie_session.router)
app.include_router(user_create_document.router)




@app.get("/",include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')




@app.middleware("http")
async def delete_expired_sessions(request: Request, call_next):
    # get the remote IP address of the client
    remote_ip = request.client.host

    #get session_id from cookie
    session_id = request.cookies.get("session_id")

    # if the session exists, update the expire time
    if remote_ip in sessions and session_id in sessions[remote_ip]:
        sessions[remote_ip][session_id] = datetime.now() + timedelta(seconds=SESSION_EXPIRE_TIME)

    # Eliminar cualquier sesión que haya expirado
    if remote_ip in sessions:
        expired_sessions = [session_id for session_id, expire_time in sessions[remote_ip].items() if expire_time < datetime.now()]
        for session_id in expired_sessions:
            # delete the expired session from the sessions dictionary
            response = PlainTextResponse("Session expired")
            response.delete_cookie(key="session_id")
            del sessions[remote_ip][session_id]
            await pdf_file_sessionClose_delete(session_id)
            await image_file_sessionClose_delete(session_id)

        if len(sessions[remote_ip]) == 0:
            del sessions[remote_ip]
        else:
            # if there are still sessions left, set the cookie to the first session
            response = await call_next(request)
            first_session_id = next(iter(sessions[remote_ip]))
            response.set_cookie(key="session_id", value=first_session_id, expires=30)

    else:
        # Si no hay sesión existente, simplemente llame a la función de llamada
        response = await call_next(request)

    return response

