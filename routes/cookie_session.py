
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


@router.get("/", status_code=status.HTTP_201_CREATED)
async def get_session(response: Response, request: Request):
    """"
    ## Description
    This endpoint creates a session for the client and returns the session_id.
    The session_id is stored in a cookie and the session is stored in a dictionary.
    The session is deleted when the client closes the browser or when the session expires.

    ## Response
    - 201: Session created
    - 403: Max session limit exceeded
    
    ## return
    - session (dict): dictionary with the session_id and the expire time
    
    ## Arguments
    - `request (Request)`: request object

    ## Dependencies
    - None

    ## Background tasks
    - None

    ## Cookies
    - session_id: session_id cookie

    """
    session_id = str(uuid4())  
    remote_ip = request.client.host
    
    if remote_ip not in sessions:
        sessions[remote_ip] = {}
    
    if len(sessions[remote_ip]) >= MAX_SESSIONS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Max session limit exceeded.")
    
    sessions[remote_ip][session_id] = datetime.now() + timedelta(seconds=SESSION_EXPIRE_TIME)
    response.set_cookie(key="session_id", value=session_id)
    
    return {"session": sessions[remote_ip]}


@router.get("/session_id",status_code=status.HTTP_200_OK)
async def get_session_id (request:Request, session_id:str = Depends( session_cookie_id_validator)):
    """
    ## Description
    This endpoint returns the last session_id cookie.

    ## Response
    - 200: OK

    ## return
    - `session_id (str)`: session_id cookie

    ## Arguments
    - `request (Request)`: request object

    ## Dependencies
    - `session_id (str)`: session_id cookie

    """
    return {"session_id": session_id}


@router.get("/session_all",status_code=status.HTTP_200_OK)
async def get_session_all(request:Request, session_id: str = Depends( session_cookie_id_validator)):
    """
    ## Description
    This endpoint returns all the sessions for the client.

    ## Response
    - 200: OK

    ## Arguments
    - `session_id (str)`: session_id cookie
    
    ## return
    - `session (dict)`: dictionary with all the sessions for the client

    ## Arguments
    - `request (Request)`: request object

    ## Dependencies
    - `session_id (str)`: session_id cookie

    """
    actual_ip = request.client.host
    return {"session":sessions[actual_ip]}



@router.delete("/",status_code=status.HTTP_200_OK)
async def delete_session(request: Request,response : Response, session_id: str = Depends( session_cookie_id_validator)):
    """
    ## Description
    This endpoint deletes the session_id cookie and the session.

    ## Response
    - 200: OK

    ## return
    - `session_delete (str)`: session_id cookie

    ## Arguments
    - `request (Request)`: request object

    """
    actual_ip = request.client.host
    del sessions[actual_ip][session_id]
    response.delete_cookie(key="session_id")

    if len(sessions[actual_ip]) == 0:
        del sessions[actual_ip]
    else :
        first_session_id = next(iter(sessions[actual_ip]))
        response.set_cookie(key="session_id", value=first_session_id)
    
    return {"session_delete":session_id}



