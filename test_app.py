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
        
    def test_save_plot_stock_trend(self):
        data = {
            'Close': np.random.random(100),
            '30day': np.random.random(100),
            '200day': np.random.random(100)
        }
        stockprices = pd.DataFrame(data)
        save_plot_stock_trend(var='30day', cur_title='Test Plot', stockprices=stockprices)
        self.assertTrue(os.path.exists('static/30day.png'))
        os.remove('static/30day.png')
if __name__ == '__main__':
    unittest.main()
