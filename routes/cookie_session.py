
from fastapi import APIRouter

from fastapi import (HTTPException, 
                     status,
                     Response,
                     Request) 

from fastapi import (Depends,
                      Cookie)

from validation.cookie_validation import  session_cookie_id_validator
from validation.cookie_validation import(sessions,
                                         MAX_SESSIONS,
                                         SESSION_EXPIRE_TIME)
from uuid import uuid4
from datetime import datetime, timedelta

router = APIRouter(
    prefix= "/session",
    tags=["session"]
)


@router.get("/")
async def read_session(response: Response, request: Request):
    session_id = str(uuid4())  
    remote_ip = request.client.host
    
    if remote_ip not in sessions:
        sessions[remote_ip] = {}
    
    if len(sessions[remote_ip]) >= MAX_SESSIONS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Max session limit exceeded.")
    
    sessions[remote_ip][session_id] = datetime.now() + timedelta(seconds=SESSION_EXPIRE_TIME)
    response.set_cookie(key="session_id", value=session_id)
    
    return {"session_id": session_id,
            "session": sessions,
            "remote_ip": remote_ip}


@router.get("/session_id")
async def get_session_id (request:Request, session_id:str = Depends( session_cookie_id_validator)):
    return {"session_id": session_id}


@router.get("/session_all")
async def get_session_all(request:Request, session_id: str = Depends( session_cookie_id_validator)):
    actual_ip = request.client.host
    return {"session":sessions[actual_ip]}



@router.delete("/")
async def delete_session(request: Request,response : Response, session_id: str = Depends( session_cookie_id_validator)):
        
    actual_ip = request.client.host
    del sessions[actual_ip][session_id]
    response.delete_cookie(key="session_id")

    if len(sessions[actual_ip]) == 0:
        del sessions[actual_ip]
    else :
        first_session_id = next(iter(sessions[actual_ip]))
        response.set_cookie(key="session_id", value=first_session_id)
    
    return {"session_delete":session_id}



