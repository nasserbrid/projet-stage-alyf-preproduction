import unittest
from ..utils import create_users
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_alyf.settings')

# Initialiser Django
django.setup()

#TDD

class TestPasswordGeneration(unittest.TestCase):
    def test_generate_password(self):
        # Arrange
        user = ["youssef.omari@alyfpro.fr","Youssef","OMARI"] 

         #Act
        result = create_users.generate_password(user)
        
        #Assert
        self.assertEqual(result, "You$%!OM")

    
    def test_create_users_password(self):
        #Arrange
        user = ["nickylarson@gmail.com", "Yuyu", "HAKUSHO"]
        
        #Act
        password = create_users.generate_password(user)
        user_created = User.objects.create_user(user[2], user[0], password)
        
        #Assert
        self.assertEqual(password, "Yuy$%!HA")
        self.assertEqual(type(user_created), get_user_model())

if __name__ == "__main__":
    unittest.main()
        
    
       