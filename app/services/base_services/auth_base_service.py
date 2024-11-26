import abc
from app.dtos.auth import LoginReq
from app.models import User
from app.utils.access_token import Token

# Tämä on "interface" eli abstrakti parent luokka AuthServicelle.
# Tämä helpottaa täyttämään vaaditut metodit, jotta muu softa toimii oikein
# kun vaihdetaan tietokantaa ja sitä varten luodaan uusi auth service.


class AuthBaseService(abc.ABC):
    @abc.abstractmethod
    def login(self, credentials: LoginReq, token: Token):
        raise NotImplemented()

    @abc.abstractmethod
    def logout(self, user: User):
        raise NotImplemented()