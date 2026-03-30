from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

h = pwd.hash("123456")
print(pwd.verify("123456", h))