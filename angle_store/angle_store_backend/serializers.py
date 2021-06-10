from datetime import datetime
import re
from rest_framework import serializers

from angle_store_backend.models import Product

NAME_FIRST_LETTER_REGEX = r"^[0-9a-zA-Z]$"
NAME_REMAINING_LETTERS_REGEX = r"^([0-9a-zA-Z]|\ |-)+$"

DATE_FORMAT = '%m/%d/%Y'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "price", "start_date"]

    # Validators
    def validate_name(self, value: str):
        # pkey constraint takes care of uniqueness, just need to check formatting
        if len(value) < 4 or len(value) > 10:
            raise serializers.ValidationError(
                f"Name should be between 4 and 10 characters long. Current name is {len(value)} characters long."
            )

        if not re.match(NAME_FIRST_LETTER_REGEX, value[0]):
            raise serializers.ValidationError(
                f"First letter of name should be digit or letter. Current first letter is {value[0]}."
            )

        if not re.match(NAME_REMAINING_LETTERS_REGEX, value[1:]):
            raise serializers.ValidationError(
                f"2nd letter of name onwards should be digit/letter/space/hyphen. Current name is {value}."
            )

        return value

    def validate_price(self, value: int):
        if value < 0:
            raise serializers.ValidationError(f"Price should not be negative. Provided price: {value}")
        return value

    def validate_start_date(self, value: str):
        try:
            start_date = datetime.strptime(value, DATE_FORMAT).date()
            today = datetime.now().date()

            if start_date < today:
                raise serializers.ValidationError(
                    f"Provided start_date should be after current date. start_date: {str(start_date)},\
                        today: {str(today)}"
                )

            return value
        except Exception as e:
            # Catch formatting + misc errors
            raise serializers.ValidationError(e)
