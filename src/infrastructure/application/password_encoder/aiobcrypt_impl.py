import aiobcrypt

from src.application.common.interfaces.password_encoder import PasswordEncoder


class AiobcryptPasswordEncoder(PasswordEncoder):

    async def encode(self, plain_password: str) -> str:
        plain_password_bytes = bytes(plain_password, "utf-8")
        return str(await aiobcrypt.hashpw_with_salt(plain_password_bytes), "utf-8")

    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        plain_password_bytes = bytes(plain_password, "utf-8")
        hashed_password_bytes = bytes(hashed_password, "utf-8")

        return await aiobcrypt.checkpw(
            password=plain_password_bytes, hashed_password=hashed_password_bytes
        )