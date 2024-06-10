import unittest

class TestImageClassification(unittest.TestCase):
    def test_image_preprocessing(self):
        img_path = 'path/to/test_image.jpg'
        img_tensor = load_image(img_path)
        self.assertEqual(img_tensor.shape, (1, 150, 150, 3))

    def test_model_prediction(self):
        img_path = 'path/to/test_image.jpg'
        img_tensor = load_image(img_path)
        pred = model.predict(img_tensor)
        self.assertTrue(pred is not None)

if __name__ == '__main__':
    unittest.main()
