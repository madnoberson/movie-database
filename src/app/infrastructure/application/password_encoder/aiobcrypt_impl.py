import aiobcrypt

from app.application.common.interfaces.password_encoder import PasswordEncoder


class AiobcryptPasswordEncoder(PasswordEncoder):

    async def encode(self, plain_password: str) -> str:
        plain_password_bytes = bytes(plain_password, "utf-8")
        return str(await aiobcrypt.hashpw_with_salt(plain_password_bytes), "utf-8")

    async def verify(self, plain_password: str, encoded_password: str) -> bool:
        return await aiobcrypt.checkpw(
            password=bytes(plain_password, "utf-8"), hashed_password=bytes(encoded_password, "utf-8")
        )