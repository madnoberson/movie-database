class InvalidPassword(Exception):

    @property
    def message(self) -> str:
        return "Invalid password"