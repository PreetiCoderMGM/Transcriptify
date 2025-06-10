import datetime
import enum
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import StatementError
from logger_util import get_logger
from src import db, app
from src.encryption import encrypt_data_sys, hash_data, decrypt_data_sys
import jwt
import urllib.parse
log = get_logger(__name__)


class FountSize(enum.Enum):
    Small = "Small"
    Medium = "Medium"
    Large = "Large"


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    email_h = db.Column(db.String(200), index=True)
    first_name = db.Column(db.String(200), nullable=False, default='')
    last_name = db.Column(db.String(200), nullable=False, default='')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __init__(self, email, first_name=None, last_name=None, **kwargs):
        super(User, self).__init__(**kwargs)

        self.email = encrypt_data_sys(email)
        self.email_h = hash_data(email)
        self.created_on = datetime.datetime.now()
        self.first_name = encrypt_data_sys(first_name) if first_name else encrypt_data_sys('NA')
        self.last_name = encrypt_data_sys(last_name) if last_name else encrypt_data_sys('NA')

    def get_first_name(self):
        return decrypt_data_sys(self.first_name)

    def set_first_name(self, first_name):
        self.first_name = encrypt_data_sys(first_name)
        self.set_hash_str()

    def get_last_name(self):
        return decrypt_data_sys(self.last_name)

    def set_last_name(self, last_name):
        self.last_name = encrypt_data_sys(last_name)
        self.set_hash_str()

    def get_email(self):
        return decrypt_data_sys(self.email)

    @property
    def full_name(self):
        return '{} {}'.format(decrypt_data_sys(self.first_name), decrypt_data_sys(self.last_name))

    @staticmethod
    def get_by_email(email: str):
        attempt = 0
        while attempt < 5:
            try:
                attempt += 1
                return User.query.filter_by(email_h=hash_data(email)).first()
            except OperationalError:
                log.info(f"Due to my sql connection error get_by_email {attempt} fail. {OperationalError}")
                db.session.rollback()
            except StatementError as se:
                log.exception(se)
                db.session.rollback()
            except Exception as ex:
                log.exception(ex)
                return None
        return None

    @staticmethod
    def get_by_id(data_id: int):
        return User.query.get(data_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_auth_token(user_id, org_id, duration_days=1, minutes=0, scope_regex: str = "*"):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                # Use limit of 2 hour for token validation
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=duration_days, minutes=minutes),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
                'sub_o': org_id,
                'scope': scope_regex
            }
            token = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )

            if isinstance(token, str):
                return urllib.parse.quote(encrypt_data_sys(token))
            return urllib.parse.quote(encrypt_data_sys(token.decode("utf-8")))

        except Exception as ex:
            log.exception(ex)
            return ex

    def encode_auth_token(self, org_id, duration_days=1, minutes=0, scope_regex: str = "*"):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            return User.get_auth_token(self.id, org_id, duration_days, minutes, scope_regex)
        except Exception as ex:
            log.exception(ex)
            return ex
