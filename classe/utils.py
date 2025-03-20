import random
import string
from .models import Classe
class Utils:
    @staticmethod
    def generate_activation_code():
        """Generate a random activation code of 4 characters."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            if not Classe.objects.filter(activation_code=code).exists():
                return code
