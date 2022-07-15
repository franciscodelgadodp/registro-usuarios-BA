from passlib.context import CryptContext


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(password: str):
    return pwd_cxt.hash(password)


def verify(user_pwd: str, candidatePwd: str):
    return pwd_cxt.verify(candidatePwd, user_pwd)
