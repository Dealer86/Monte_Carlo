# tests.py
from django.test import TestCase, SimpleTestCase
from datetime import datetime
from unittest.mock import patch
from django.urls import reverse
from .api.monte_carlo import CoinGeckoMonteCarloSimulation
import pandas as pd


class CoinGeckoMonteCarloSimulationTests(TestCase):
    def setUp(self):
        self.coin_gecko = CoinGeckoMonteCarloSimulation("bitcoin", 1, 1000, 100, 5)

    def test_fetch_price_data_successful_response(self):
        # Mocking a successful API response
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "prices": [
                    [timestamp, price] for timestamp, price in zip(range(10), range(10))
                ]
            }

            prices = self.coin_gecko.fetch_price_data("bitcoin", 1)

        self.assertEqual(len(prices), 10)

    def test_fetch_price_data_failed_response(self):
        # Mocking a failed API response
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 404

            coin_gecko = CoinGeckoMonteCarloSimulation(
                "Non exiting coin", 1, 1000, 100, 5
            )
            prices = coin_gecko.fetch_price_data("Non exiting coin", 1)

        self.assertIsNone(prices)

    def test_calculate_log_returns(self):
        # Test the calculate_log_returns method with sample data
        sample_prices = [100, 110, 90, 120, 80]
        expected_log_returns = [0.09531, -0.20067, 0.28768, -0.40547]

        log_returns = self.coin_gecko.calculate_log_returns(sample_prices)

        # Round to 5 decimal places for comparison
        log_returns = [round(val, 5) for val in log_returns]

        self.assertEqual(log_returns, expected_log_returns)

    def test_monte_carlo_simulation(self):
        log_returns = pd.Series([0.02, -0.01, 0.03, -0.02])
        principal_amount = 1000
        investment_horizon = 5

        simulations = self.coin_gecko.monte_carlo_simulation(
            log_returns, principal_amount, investment_horizon
        )

        self.assertEqual(len(simulations), 5)

    def test_run_simulation(self):
        # Mock the fetch_price_data method to avoid actual API calls
        with patch.object(
            CoinGeckoMonteCarloSimulation,
            "fetch_price_data",
            return_value=[100, 120, 90, 110, 80],
        ):
            simulations = self.coin_gecko.run_simulation()

        self.assertEqual(len(simulations), 5)

    def test_visualize_simulation(self):
        # Mock the run_simulation method to avoid actual simulation runs
        with patch.object(
            CoinGeckoMonteCarloSimulation,
            "run_simulation",
            return_value=[1100, 950, 1200, 1050, 900],
        ):
            visualization_html = self.coin_gecko.visualize_simulation()

        self.assertTrue(isinstance(visualization_html, str))
        self.assertIn("div", visualization_html)

    def test_visualize_history_graph(self):
        # Mock the fetch_price_data method to avoid actual API calls
        with patch.object(
            CoinGeckoMonteCarloSimulation,
            "fetch_price_data",
            return_value=([datetime(2022, 1, 1), datetime(2022, 1, 2)], [100, 120]),
        ):
            history_html = self.coin_gecko.visualize_history_graph()

        self.assertTrue(isinstance(history_html, str))
        self.assertIn("div", history_html)


class MonteCarloTests(SimpleTestCase):
    def test_url_exists_at_the_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_that_the_template_name_is_correct(self):
        response = self.client.get(reverse("montecarlo"))
        self.assertTemplateUsed(response, "simulation/montecarlo.html")

    def test_template_content(self):
        response = self.client.get(reverse("montecarlo"))
        self.assertContains(response, "<title>Crypto Monte Carlo Simulation</title>")
