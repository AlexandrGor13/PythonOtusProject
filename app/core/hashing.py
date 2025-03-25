import bcrypt
from passlib.context import CryptContext

if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('about', (object,), {'__version__': bcrypt.__version__})

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

if __name__ == '__main__':
    p1 = pwd_context.hash('password')
    p2 = pwd_context.hash('password')
    print(p1 == p2)
    print(pwd_context.verify('password', p1))