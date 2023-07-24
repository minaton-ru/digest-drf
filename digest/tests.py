from django.test import TestCase


class StatusCodeTest(TestCase):
    """
    Тест на коды ответа
    """
    fixtures = ["fixture.json"]

    def test_404_status(self):
        """
        Должен вернуть код 404, потому что в загруженных фикстурах нет пользователя с id=5
        """ 
        response = self.client.get("/api/digest/", {"userid": 5, "rating": 8})
        self.assertEqual(response.status_code, 404)

    def test_200_status(self):
        """
        Должен вернуть код 200, потому что в загруженных фикстурах есть пользовател с id=2
        """ 
        response = self.client.get("/api/digest/", {"userid": 2, "rating": 8})
        self.assertEqual(response.status_code, 200)

class DigestTest(TestCase):
    """
    Тест количества полученных постов в дайджесте для загруженных фикстур
    """
    fixtures = ["fixture.json"]

    def test_first_digest(self):
        """
        Должен вернуть дайджест, в котором четыре поста
        """
        response = self.client.get("/api/digest/", {"userid": 2, "rating": 8})
        self.assertEqual(len(response.json()["posts"]), 4)
