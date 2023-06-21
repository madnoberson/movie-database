from src.application.common.passoword_encoder import PasswordEncoder


class FakePasswordEncoder(PasswordEncoder):

    def encode(self, password: str) -> str:
        return f"encoded{password}"

    def verify(
        self,
        password: str,
        encoded_password: str
    ) -> bool:
        return self.encode(password) == encoded_password