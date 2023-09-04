class BaseModel:

    def update_fields(self, **kwargs) -> int:
        """
        Updates fields values passed to kwargs if value is not None
        and returns the number of updated values
        """
        updated_fields = 0
        for key, value in kwargs.items():
            if value is None:
                continue
            setattr(self, key, value)
            updated_fields += 1
        
        return updated_fields
