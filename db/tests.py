import unittest
import requests
import pymongo



"""
class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
"""

myclient = pymongo.MongoClient("mongodb://admin:admin@172.17.0.1:27017")
mydb = myclient["smpp"]

users_col = mydb["users"]

test_user = {
        "system_id": 111111,
        "password": "qwerty",
        "tag": "test_user",
        "api_key": "test"
}


class TestAPIMethods(unittest.TestCase):
    def test_add_user(self):
        users_col.delete_one(test_user)

        new_user = requests.post("127.0.0.1:5000/new_user",
                                 params={
                                     "system_id": test_user["system_id"],
                                     "password": test_user["password"],
                                     "tag": test_user["tag"],
                                     "api_key": test_user["api_key"]
                                     })
        self.assertEqual(new_user.status_code, 200)

        


if __name__ == '__main__':
    unittest.main()
