import random
import string
class Utils:
    @staticmethod
    def generate_activation_code():
        """Generate a random activation code of 4 characters."""
        return ''.join(random.choices(string.ascii_uppercase, k=4))
