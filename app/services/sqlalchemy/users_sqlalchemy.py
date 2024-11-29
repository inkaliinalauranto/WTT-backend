import os
from datetime import datetime, timezone
import dotenv
from app.custom_exceptions.authorization import UnauthorizedActionException
from app.custom_exceptions.notfound import NotFoundException
from app.custom_exceptions.taken import TakenException
from app.models import Team, User, Role
from app.services.base_services.users_base_service import UsersBaseService
from app.services.sqlalchemy.auth_sqlalchemy import pwd_context


dotenv.load_dotenv()

class UsersServiceSqlAlchemy(UsersBaseService):
    # Haetaan käyttäjä id:n perusteella:
    def get_by_id(self, user_id: int) -> User:
        user = (self.db.query(User).filter(User.id == user_id)).first()
        return user


    def get_all_by_team_id(self, team_id:int) -> list[User]:
        employee_role = self.db.query(Role).filter(Role.name == "employee").first()

        users_list: list[User] = self.db.query(User).filter(User.team_id == team_id, User.role_id == employee_role.id).all()
        return users_list


    def create_admin(self, admin_role: Role, admin_team: Team):
        try:
            if not admin_role:
                raise NotFoundException("Admin role not found. Create admin role using roles service")

            if not admin_team:
                raise NotFoundException("Admin team not found. Create admin team using teams service")

            self.db.add(
                User(
                    username="admin",
                    password=pwd_context.hash(os.getenv("ADMIN_PW")),
                    role_id=admin_role.id,
                    first_name="Admin",
                    last_name="user",
                    email="admin@wtt.com",
                    created_at=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8'),
                    team_id=admin_team.id
                )
            )
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e


    # Create other users
    def create(self, user: User, creator_role_id: int):
        try:
            # Luotavan käyttäjän rooli määritellään controllerissa, ja niiden olemassaolo tarkistetaan muualla

            # Käyttäjä ei voi luoda toista käyttäjää samoilla oikeuksilla.
            # Tällä estetään myös se, että admin ei yritä luoda toista adminia tätä kautta
            if creator_role_id == user.role_id:
                raise UnauthorizedActionException("Forbidden action")

            # Löytyykö team tietokannasta
            team = self.db.query(Team).filter(Team.id == user.team_id).first()
            if team is None:
                raise NotFoundException("Team not found")

            # Onko käyttäjänimi jo käytössä
            username = self.db.query(User.username).filter(User.username == user.username).first()
            if username is not None:
                raise TakenException("Username is taken")
            
            # Onko sähköposti jo rekisteröity olemassa olevalle käyttäjälle
            email = self.db.query(User.email).filter(User.email == user.email).first()
            if email is not None:
                raise TakenException("Email is already registered")

            # Häshätään salasana
            hashed_pw = pwd_context.hash(user.password)
            user.password = hashed_pw

            # Luodaan timestamp, joka on UTC 0 ja muotoiltu ja muunnettu mysqliin sopivaksi.
            user.created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')

            # Lisätään käyttäjä, joka on models.User instanssi.
            self.db.add(user)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e


    def get_user_by_access_jti(self, access_jti):
        # Haetaan user access_tokenin perusteella.
        user = self.db.query(User).filter(User.access_jti == access_jti).first()
        return user
    

    def delete_user_by_id(self, user_id: int, manager:User):
        try:
            # Haetaan id:n perusteella poistettava käyttäjä
            user = self.get_by_id(user_id)

            if user is None:
                # Jos käyttäjää ei ole, palautetaan 404
                raise NotFoundException("User not found")

            if manager.role_id == user.role_id:
                # Jos käyttäjän rooli on sama kuin poistettavan rooli (manager yrittää poistaa toisen managerin), tämä on kiellettyä.
                raise UnauthorizedActionException("Unauthorized action")
            
            # Jos käyttäjä löytyy, poistetaan se
            self.db.delete(user)
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            raise e

    # Yksinkertainen isworking setteri tietokantaan
    def set_working_status_by_id(self, user, is_working):
        try:
            user.is_working = is_working
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e


