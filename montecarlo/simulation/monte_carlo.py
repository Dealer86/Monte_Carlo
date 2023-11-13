import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import mpld3


class CoinGeckoMonteCarloSimulation:
    def __init__(self, coin_id: str, years_of_price_data_to_collect_starting_from_current_year: int, principal_amount: float, investment_horizon: int, num_simulations: int ):
        self.coin_id = coin_id
        self.years = years_of_price_data_to_collect_starting_from_current_year
        self.principal_amount = principal_amount
        self.investment_horizon = investment_horizon
        self.num_simulations = num_simulations

    def fetch_price_data(self, coin_id, years):
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

    

    def run_simulation(self):
        """
        Runs simulations and returns the results as a string.
        """
        prices = self.fetch_price_data(self.coin_id, self.years)
        if prices is not None:
            log_returns = self.calculate_log_returns(prices)
            total_average_simulations = self.monte_carlo_simulation(log_returns, self.principal_amount, self.investment_horizon)
            return total_average_simulations
            

        else:
            print(f"Failed to run simulation")
            return []

    def get_simulations_results(self):
        results = []
        image_path = 'static/simulation/monte_carlo.png'
        if self.run_simulation():
            for i, average_future_value in enumerate(self.run_simulation()):
                results.append(f"Average future values of the investment for Monte Carlo Simulation {i + 1}: {average_future_value:.2f}$")

            results.append(f"Total average of {self.num_simulations} Monte Carlo simulations: {np.mean(self.run_simulation()):.2f}$")

            # self.visualize_simulation_results(total_average_simulations)
            # result = '\n'.join(results)
            
            return results, image_path
        else:
            print(f"Simulation failed getting results")
            return []


    def visualize_simulation(self):
        average_future_values = self.run_simulation()
        simulation_number = list(range(1, len(average_future_values) + 1))

        average_future_value_df = pd.DataFrame({
            "Simulation Number": simulation_number,
            "Average Future Value": average_future_values
        })

        # Create a figure with a single subplot
        fig, ax = plt.subplots(figsize=(14, 12))

        # Plot the bar chart
        average_future_value_df.plot.barh(y="Average Future Value", x="Simulation Number", legend=False, ax=ax)
        ax.set_xlabel('Average Future Value')
        ax.set_ylabel('Simulation Number')
        ax.grid(True)

        # Display additional information as text
        tab_info = (
            f"Cryptocurrency: {self.coin_id.capitalize()}",
            f"Years of Price Data Collected: {self.years} years",
            f"Principal amount: {self.principal_amount}$",
            f"Investment Horizon: {self.investment_horizon} days",
            f"Number of Simulations: {self.num_simulations}",
            f"Average of all Monte Carlo Simulations: {np.mean(self.run_simulation()):.2f}$"
        )

        # Add text annotations to the top of the plot
        spacing = 0.02  # Adjust this value as needed
        for i, line in enumerate(tab_info):
            ax.annotate(line, xy=(0.5, 1.02 + spacing * (i + 1)), xycoords='axes fraction',
                        ha='center', va='center', fontsize=14)
            
        # Convert the Matplotlib figure to HTML using mpld3
        graph_html = mpld3.fig_to_html(fig)
        return graph_html

        
        
        





if __name__ == "__main__":
    # coin_id = str(input("Enter the cryptocurrency symbol: "))
    # years = int(input("Enter the number of years of historical data to consider: "))
    # principal_amount = float(input("Enter the initial principal amount: "))
    # investment_horizon = int(input("Enter the investment horizon (in years): "))
    # num_simulations = int(input("Enter the number of Monte Carlo simulations: "))

    # run_simulation_and_print_results(coin_id, years, principal_amount, investment_horizon, num_simulations)
    monte_carlo = CoinGeckoMonteCarloSimulation("solana", 1, 1000, 100, 23)
    # monte_carlo.visualize_average_future_value()
    monte_carlo.visualize_simulation()
    