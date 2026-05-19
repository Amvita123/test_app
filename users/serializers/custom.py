from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class CustomSerializer(serializers.Serializer):

    def is_valid(self, raise_exception=False):
        valid = super().is_valid(raise_exception=False)

        if not valid:
            error_messages = []

            for field, messages in self.errors.items():
                if isinstance(messages, list):
                    for msg in messages:
                        if field == "non_field_errors":
                            error_messages.append(f"{msg}")
                        else:
                            if "required" in msg.lower():
                                error_messages.append(f"{field} is required")
                            else:
                                error_messages.append(f"{field} {msg}")
                else:
                    error_messages.append(f"{field} {messages}")

            message = ", ".join(error_messages)

            if raise_exception:
                raise ValidationError({
                    "success": False,
                    "message": message,
                    "data": None,
                    "error": None
                })

            self._errors = {
                "success": False,
                "message": message,
                "data": None,
                "error": None
            }

        return valid