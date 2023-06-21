from hashlib import sha256

from src.application.common.passoword_encoder import PasswordEncoder


class HashlibPasswordEncoder(PasswordEncoder):

    def encode(self, password: str) -> str:
        bytes_ = bytes(password, encoding="utf-8")
        return sha256(bytes_).hexdigest()
    
    def verify(self, password: str, encoded_password: str) -> bool:
        return self.encode(password) == encoded_password