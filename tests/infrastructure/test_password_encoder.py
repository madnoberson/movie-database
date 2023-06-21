from src.infrastructure.password_encoder import (
    HashlibPasswordEncoder
)


class TestPasswordEncoder:

    def test_verify_should_return_true_when_password_is_corect(self):
        encoder = HashlibPasswordEncoder()

        password = "secretpassword"
        encoded_password = encoder.encode(password)

        assert encoder.verify(password, encoded_password)
    
    def test_verify_should_return_false_when_password_is_incorrect(self):
        encoder = HashlibPasswordEncoder()

        wrong_password = "wrongsecretpassword"
        encoded_password = encoder.encode("secretpassword")

        assert not encoder.verify(wrong_password, encoded_password)