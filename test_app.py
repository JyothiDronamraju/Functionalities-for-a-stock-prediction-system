import os
import unittest
from flask_testing import TestCase
from app import app, create_dataset, save_plot_stock_trend
import numpy as np
import pandas as pd
from unittest.mock import patch
from datetime import datetime, timedelta

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_predict_stock_get(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Symbol', response.data)

    @patch('app.yf.download')
    @patch('app.yf.Ticker')
    def test_predict_stock_post(self, mock_ticker, mock_download):
        mock_download.return_value = self._generate_mock_stock_data()
        mock_ticker.return_value.news = []

        response = self.client.post('/home', data={'symbol': 'AAPL'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AAPL', response.data)
    def _generate_mock_stock_data(self):
        dates = pd.date_range(start=datetime.now() - timedelta(days=1000), end=datetime.now())
        data = np.random.random(size=(len(dates), 5))
        return pd.DataFrame(data, columns=['Open', 'High', 'Low', 'Close', 'Volume'], index=dates)

class TestFunctions(unittest.TestCase):

    def test_create_dataset(self):
        data = np.arange(100).reshape(-1, 1)
        window_size = 5
        X, y = create_dataset(data, window_size)
        self.assertEqual(X.shape, (95, 5))
        self.assertEqual(y.shape, (95,))

    def test_create_dataset_window_size_1(self):
        # Test with window size 1
        data = np.arange(100).reshape(-1, 1)
        window_size = 1
        X, y = create_dataset(data, window_size)
        self.assertEqual(X.shape, (99, 1))
        self.assertEqual(y.shape, (99,))

    
    

    def test_create_dataset_negative_window_size(self):
        # Test with negative window size
        data = np.arange(100).reshape(-1, 1)
        window_size = -5
        with self.assertRaises(ValueError):
            X, y = create_dataset(data, window_size)

    def test_create_dataset_non_numeric_data(self):
        # Test with non-numeric data
        data = ['a', 'b', 'c']
        window_size = 2
        with self.assertRaises(TypeError):
            X, y = create_dataset(data, window_size)

    def test_create_dataset_non_numeric_window_size(self):
        # Test with non-numeric window size
        data = np.arange(100).reshape(-1, 1)
        window_size = 'abc'
        with self.assertRaises(TypeError):
            X, y = create_dataset(data, window_size)

    

if __name__ == '__main__':
    unittest.main()
