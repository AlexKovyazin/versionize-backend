from pydantic import model_validator


class BaseValidationMixin:

    @model_validator(mode="after")
    def validate_at_least_one_field(self, values):
        provided_fields = [
            field_name for field_name, field_value in values
            if field_value is not None
        ]

        if not provided_fields:
            raise ValueError("At least one field must be provided")

        return values