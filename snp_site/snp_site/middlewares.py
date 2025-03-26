from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
class JwtAuthMiddleware(BaseMiddleware):


    async def __call__(self,scope,receive,send):

        result=parse_qs(scope['query_string'])
        btoken=result.get(b'token')
        if(btoken):
            try:
                token=btoken[0].decode('utf-8')
                user_id=AccessToken(token)['user_id']
                scope['user_id']=user_id

            except:
                scope['user_id']=None

        else:
            scope['user_id']=None

        
        

        return await super().__call__(scope,receive,send)
    
        
    