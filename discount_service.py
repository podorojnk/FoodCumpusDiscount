import re

STUDENT_DISCOUNT_PERCENT = 15.0
CARD_ID_PATTERN = re.compile(r"[0-9]{8}") 


class InvalidCardError(ValueError):
    """Номер студенческого билета имеет неверный формат."""


class StudentRegistryStub:
    KNOWN_CARDS = {"12345678", "20240001", "00123456"}

    def is_active(self, card_id: str) -> bool:
        return card_id in self.KNOWN_CARDS


class DiscountModule:
    def __init__(self, registry=None):
        
        self.registry = registry or StudentRegistryStub()

    @staticmethod
    def validate_card_id(card_id) -> str:
        
        if not isinstance(card_id, str):
            raise InvalidCardError(
                f"Номер билета должен быть строкой, получено: {type(card_id).__name__}"
            )
        if not card_id:
            raise InvalidCardError("Номер билета не может быть пустым")
        if len(card_id) > 32:  
            raise InvalidCardError("Номер билета слишком длинный")
        if not CARD_ID_PATTERN.fullmatch(card_id):
            raise InvalidCardError(
                "Неверный формат номера билета: ожидается ровно 8 цифр (0-9)"
            )
        return card_id

    def apply_student_discount(self, card_id) -> float:

        card_id = self.validate_card_id(card_id)
        if self.registry.is_active(card_id):
            return STUDENT_DISCOUNT_PERCENT
        return 0.0
