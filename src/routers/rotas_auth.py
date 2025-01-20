from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario
from src.schemas.schemas import LoginSucess, UsuarioSchema, UsuarioSimples, LoginData
from src.infra.sqlalchemy.config.database import get_db, criar_db
from fastapi import APIRouter, status, Depends, HTTPException
from src.infra.providers import hash_provider, token_provider
from src.routers.auth_utils import obter_usuario_logado
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth")


# AUTENTICAÇÃO DE USUÁRIO

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model= UsuarioSimples)
def criar_usuario(usuario: UsuarioSchema, db: Session= Depends(get_db)):
    # verificação se já existe
    usuario_localizado = RepositorioUsuario(db).obter_por_email(usuario.email)

    if usuario_localizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuário já existente')

    # criando o usuario
    usuario.senha = hash_provider.gerar_hash(usuario.senha)

    usuario_criado = RepositorioUsuario(db).criar(usuario)
    return usuario_criado


@router.post('/token', status_code=status.HTTP_202_ACCEPTED, response_model=LoginSucess)
def login(login_data: LoginData, db: Session= Depends(get_db)):
    senha = login_data.senha
    email = login_data.email

    usuario = RepositorioUsuario(db).obter_por_email(email)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email ou senha incorretos')

    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)
    if not senha_valida:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email ou senha incorretos')

    # Gerar KWT
    token = token_provider.criar_token_acesso({'sub': usuario.email})

    usuario_simples = UsuarioSimples(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email
    )
    return LoginSucess(usuario_login=usuario_simples, acess_token=token)


@router.get('/me', response_model= UsuarioSimples)
def me(usuario: UsuarioSchema= Depends(obter_usuario_logado)):
    return usuario