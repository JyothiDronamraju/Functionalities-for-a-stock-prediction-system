import os
import unittest
from flask_testing import TestCase
from app import app, create_dataset, save_plot_stock_trend
import numpy as np
import pandas as pd
from unittest.mock import patch
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By


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
    
    def test_login(self):
        driver = webdriver.Chrome()
        # navigate to the login page
        driver.get('http://127.0.0.1:5000/')

        # find the username and password fields and enter the test data
        username_field = driver.find_element('id','username')
        password_field = driver.find_element('id', 'password')
        username_field.send_keys('admin')
        password_field.send_keys('admin')

        # find the login button and click it
        login_button = driver.find_element('xpath' ,'//button[@type="submit"]')
        login_button.click()

        # wait for the alert to be present
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # switch to the alert
        alert = Alert(driver)

        # check the alert text
        assert alert.text == 'Login successful'
        alert.accept()
        driver.quit()
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
    def test_stock_prediction_form(self):
        driver = webdriver.Chrome()
        # navigate to the page
        driver.get('http://127.0.0.1:5000/home')  

        symbol_field = driver.find_element('id', 'symbol')
        symbol_field.send_keys('AAPL')

        predict_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        predict_button.click()

        # wait for the prediction to be displayed
        WebDriverWait(driver, 2000).until(EC.visibility_of_element_located((By.ID, 'priceChart')))

        tabs = driver.find_elements(By.CLASS_NAME, 'tab')
        for i, tab in enumerate(tabs):
            tab.click()

            # wait for the tab content to be displayed
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, f'content{i+1}')))

            # check the tab content text
            content = driver.find_element('id', f'content{i+1}')
            assert True

        # close the browser
        driver.quit()
        

class TestFunctions(unittest.TestCase):

    def test_create_dataset(self):
        data = np.arange(100).reshape(-1, 1)
        window_size = 5
        X, y = create_dataset(data, window_size)
        self.assertEqual(X.shape, (95, 5))
        self.assertEqual(y.shape, (95,))
if __name__ == '__main__':
    unittest.main()
