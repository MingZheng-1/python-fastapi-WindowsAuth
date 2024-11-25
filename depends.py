import fastapi
from sspi import ServerAuth
import base64
import sspicon
app = fastapi.FastAPI()
PKG_NAME = "Negotiate" #NTLM或者Negotiate

auth = ServerAuth(PKG_NAME)

async def WindowsUser(request:fastapi.Request):
    if not request.headers.get('Authorization'):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            headers={
                'WWW-Authenticate':PKG_NAME #首次返回認證協議
            }
        )
    
    token = request.headers.get("Authorization") #獲取協議握手數據
    t = base64.b64decode(token.split()[1])
    err,res = auth.authorize(t) #認證
    token = base64.b64encode(res[0].Buffer).decode('utf-8')
    if not auth.authenticated:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            headers={
                'WWW-Authenticate':"{} {}".format(PKG_NAME,token) #第二次請求返回握手數據
            }
        )
    else:
        #第三次請求（認證成功）后獲取訪問用戶名
        name = auth.credentials.QueryCredentialsAttributes(sspicon.SECPKG_CRED_ATTR_NAMES)
        auth.reset() #重設狀態，便於後續認證
        return name