import unittest 
import main 

#create test cases for the function 
class TestMain(unittest.TestCase):
    def Test_get_type(self):
        result = main.get_type(data=str)
        self.assertEqual(result, "STRING")

