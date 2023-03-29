from fastapi import HTTPException, status
from fastapi import Cookie
from fastapi import Request

#store sessions
sessions = {}
MAX_SESSIONS = 2  # max number of sessions per IP

SESSION_EXPIRE_TIME = 1800  # 30 minutes

async def session_cookie_id_validator(request:Request,session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session ID not found")
    actual_ip = request.client.host
    if actual_ip not in sessions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Session ID not found")
    if session_id not in sessions[actual_ip]:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Session ID not found")
    
    return session_id
