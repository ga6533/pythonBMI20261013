import os
import shutil
import tempfile
import unittest

from app import app, bmi_guidance, init_db


class BmiAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        app.config["DATABASE"] = os.path.join(self.temp_dir, "test.db")
        with app.app_context():
            init_db()
        self.client = app.test_client()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_initial_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("了解自己的<br><em>健康狀況。</em>", page)
        self.assertIn("計算你的 BMI", page)

    def test_calculation_and_advice(self):
        response = self.client.post("/", data={"name": "王小明", "height": "170", "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertIn("王小明", page)
        self.assertIn("22.5", page)
        self.assertIn("健康體位", page)
        self.assertIn("維持均衡飲食", page)

    def test_taiwan_adult_thresholds(self):
        for bmi, category in [
            (18.4, "體重過輕"),
            (18.5, "健康體位"),
            (23.9, "健康體位"),
            (24.0, "體重過重"),
            (26.9, "體重過重"),
            (27.0, "肥胖"),
        ]:
            with self.subTest(bmi=bmi):
                self.assertEqual(bmi_guidance(bmi)["label"], category)

    def test_invalid_fields_do_not_produce_result(self):
        for height, weight in [("", "65"), ("0", "65"), ("abc", "65"), ("170", "-2"), ("inf", "65"), ("170", "nan"), ("1e-300", "65"), ("1e308", "65"), ("1", "1e308")]:
            with self.subTest(height=height, weight=weight):
                response = self.client.post("/", data={"name": "王小明", "height": height, "weight": weight})
                page = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('aria-invalid="true"', page)
                self.assertNotIn("YOUR RESULT", page)

    def test_input_is_escaped(self):
        response = self.client.post("/", data={"name": "王小明", "height": '<script>alert(1)</script>', "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertNotIn("<script>", page)
        self.assertIn("請輸入大於 0", page)

    def test_user_history(self):
        self.client.post("/", data={"name": "歷史使用者", "height": "170", "weight": "65"})
        self.client.post("/", data={"name": "歷史使用者", "height": "170", "weight": "70"})

        users_response = self.client.get("/users")
        self.assertEqual(users_response.status_code, 200)
        self.assertIn("歷史使用者", users_response.get_data(as_text=True))

        history_response = self.client.get("/users/歷史使用者")
        history_page = history_response.get_data(as_text=True)
        self.assertEqual(history_response.status_code, 200)
        self.assertIn("歷史使用者的 BMI 歷史", history_page)
        self.assertIn("22.5", history_page)
        self.assertIn("24.2", history_page)
        self.assertIn("計算時間", history_page)


if __name__ == "__main__":
    unittest.main()
