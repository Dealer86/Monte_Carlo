import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class CoinGeckoMonteCarloSimulation:
    def __init__(self, coin_id: str, years_of_price_data_to_collect_starting_from_current_year: int, principal_amount: float, investment_horizon: int, num_simulations: int ):
        self.coin_id = coin_id
        self.years = years_of_price_data_to_collect_starting_from_current_year
        self.principal_amount = principal_amount
        self.investment_horizon = investment_horizon
        self.num_simulations = num_simulations

    def __fetch_price_data(self, coin_id, years):
        """
        Fetches historical cryptocurrency price data from CoinGecko API.

        Args:
            coin_id (str): The symbol or identifier of the cryptocurrency.
            years (int): The number of years of historical data to consider.

        Returns:
            list: A list of historical prices for the specified cryptocurrency.
                Returns None if there are errors during data retrieval or processing.
        """
        try:
            # Calculate the number of data points based on the interval
            num_data_points = years * 365
            
            # Fetch historical price data from the CoinGecko API
            url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={num_data_points}'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract prices from the response
                prices = [entry[1] for entry in data['prices']]
                timestamp_in_milliseconds = [e[0] for e in data["prices"]]
                timestamps = [datetime.fromtimestamp(ts / 1000) for ts in timestamp_in_milliseconds]
                # print(timestamps)
                return prices
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Error while processing data: {e}")
            return None

    def calculate_log_returns(self, prices):
        """
        Calculates logarithmic returns from a list of prices.

       
        """
        price_df = pd.Series(prices)
        log_returns = np.log(price_df / price_df.shift(1))
        return log_returns.dropna()

    def monte_carlo_simulation(self, log_returns, principal_amount, investment_horizon):
        """
        Performs Monte Carlo simulations for future value prediction of a cryptocurrency investment.
        """
        returns = []
        for _ in range(self.num_simulations):
            random_log_returns = np.random.normal(log_returns.mean(), log_returns.std(), size=investment_horizon)
            future_values = np.exp(np.cumsum(random_log_returns))
            final_value = principal_amount * future_values[-1]
            returns.append(final_value)
        return returns

    def visualize_simulation_results(self, total_average_simulations):
        """
        Visualizes the results of the Monte Carlo simulations as a histogram.

        Args:
            total_average_simulations (list): List of average future values from the simulations.
        """
        plt.figure(figsize=(10, 6))
        plt.hist(total_average_simulations, bins=20, color='blue', alpha=0.7)
        plt.title('Monte Carlo Simulation Results')
        plt.xlabel('Average Future Value')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

    def run_simulation_and_get_results(self):
        """
        Runs simulations and returns the results as a string.
        """
        prices = self.__fetch_price_data(self.coin_id, self.years)
        if prices is not None:
            log_returns = self.calculate_log_returns(prices)
            total_average_simulations = self.monte_carlo_simulation(log_returns, self.principal_amount, self.investment_horizon)

            results = []
            if total_average_simulations:
                for i, average_future_value in enumerate(total_average_simulations):
                    results.append(f"Average future values of the investment for Monte Carlo Simulation {i + 1}: \n{average_future_value:.2f}$")

                results.append(f"Total average of {self.num_simulations} Monte Carlo simulations: \n{np.mean(total_average_simulations):.2f}$")

                # self.visualize_simulation_results(total_average_simulations)
                # result = '\n'.join(results)
                
                return results

        else:
            print(f"Failed to run simulation")
            return []


if __name__ == "__main__":
    # coin_id = str(input("Enter the cryptocurrency symbol: "))
    # years = int(input("Enter the number of years of historical data to consider: "))
    # principal_amount = float(input("Enter the initial principal amount: "))
    # investment_horizon = int(input("Enter the investment horizon (in years): "))
    # num_simulations = int(input("Enter the number of Monte Carlo simulations: "))

    # run_simulation_and_print_results(coin_id, years, principal_amount, investment_horizon, num_simulations)
    # monte_carlo = CoinGeckoMonteCarloSimulation("solana", 3, 1000, 2, 10)
    # print(monte_carlo.run_simulation_and_get_results())
    pass