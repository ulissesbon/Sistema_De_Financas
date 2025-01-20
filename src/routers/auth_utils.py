from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario
from fastapi.security import OAuth2AuthorizationCodeBearer
from src.infra.sqlalchemy.config.database import get_db
from fastapi import status, Depends, HTTPException
from src.infra.providers import token_provider
from sqlalchemy.orm import Session
from jose import JWTError


oauth2_schema = OAuth2AuthorizationCodeBearer(authorizationUrl='/auth', tokenUrl='token')

# decodificar o token, buscar usuario
def obter_usuario_logado(token: str= Depends(oauth2_schema), db: Session= Depends(get_db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'Token inválido')

    try:
        email: str= token_provider.verificar_token_acesso(token)

    except JWTError:
        raise exception
    

    if not email:
        raise exception
    

    usuario = RepositorioUsuario(db).obter_por_email(email)
    if not usuario:
        raise exception
        
    return usuario
    