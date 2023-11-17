"""
CoinGeckoMonteCarloSimulation Module

This module defines the `CoinGeckoMonteCarloSimulation` class, which performs
Monte Carlo simulations for predicting the future value of a cryptocurrency investment.

"""
from datetime import datetime
import logging
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import mpld3

matplotlib.use("Agg")  # Use Agg backend to avoid GUI-related issues

logging.basicConfig(
    filename="finance.log",
    level=logging.DEBUG,
    format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
)


class CoinGeckoMonteCarloSimulation:
    """
    CoinGeckoMonteCarloSimulation Class

    This class performs Monte Carlo simulations for predicting the future value of
    a cryptocurrency investment based on historical price data obtained from the CoinGecko API.

    Attributes:
        coin_id (str): The symbol or identifier of the cryptocurrency.
        years (int): The number of years of historical data to consider.
        principal_amount (float): The initial principal amount of the investment.
        investment_horizon (int): The investment horizon in days.
        num_simulations (int): The number of simulations to perform.

    Methods:
        fetch_price_data(coin_id, years, return_timestamps=False):
            Fetches historical cryptocurrency price data from CoinGecko API.

        calculate_log_returns(prices) -> pd.Series:
            Calculates logarithmic returns from a list of prices.

        monte_carlo_simulation(log_returns, principal_amount, investment_horizon) -> list:
            Performs Monte Carlo simulations for future value prediction of a cryptocurrency investment.

        run_simulation() -> list:
            Runs simulations and returns the results.

        visualize_simulation() -> str:
            Visualizes Monte Carlo simulation results and additional information in HTML format.

        visualize_history_graph() -> str:
            Visualizes the historical price data graph along with additional information in HTML format.

    """

    def __init__(
        self,
        coin_id: str,
        years_of_price_data_to_collect_starting_from_current_year: int,
        principal_amount: float,
        investment_horizon: int,
        num_simulations: int,
    ):
        self.coin_id = coin_id.lower()
        self.years = years_of_price_data_to_collect_starting_from_current_year
        self.principal_amount = principal_amount
        self.investment_horizon = investment_horizon
        self.num_simulations = num_simulations

    def fetch_price_data(self, coin_id, years, return_timestamps: bool = False):
        """
        Fetches historical cryptocurrency price data from CoinGecko API.

        Args:
            coin_id (str): The symbol or identifier of the cryptocurrency.
            years (int): The number of years of historical data to consider.

        Returns:
            list: A list of historical prices for the specified cryptocurrency.
                Returns None if there are errors during data retrieval or processing.
        """
        logging.info(
            "CoinGeckoMonteCarloSimulation executing fetch_price_data command for crypto %s ...",
            self.coin_id,
        )
        try:
            # Calculate the number of data points based on the interval
            days = years * 365

            # Fetch historical price data from the CoinGecko API
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Extract prices from the response
                prices = [entry[1] for entry in data["prices"]]
                timestamp_in_milliseconds = [e[0] for e in data["prices"]]
                timestamps = [
                    datetime.fromtimestamp(ts / 1000)
                    for ts in timestamp_in_milliseconds
                ]
                if not return_timestamps:
                    logging.info(
                        "CoinGeckoMonteCarloSimulation successfully executed fetch_price_data command for crypto %s, returning prices.",
                        self.coin_id,
                    )
                    return prices
                else:
                    logging.info(
                        "CoinGeckoMonteCarloSimulation successfully executed fetch_price_data command for crypto %s, returning timestamps and prices.",
                        self.coin_id,
                    )
                    return timestamps, prices
            else:
                logging.warning(
                    "CoinGeckoMonteCarloSimulation failed to execute fetch_price_data. Status code: %s",
                    response.status_code,
                )
                return None
        except requests.Timeout:
            logging.error("Request timed out. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            logging.error("Error during API request: %s", str(e))
            return None
        except (KeyError, ValueError) as e:
            logging.error("Error while processing data: %s", str(e))
            return None

    def calculate_log_returns(self, prices) -> pd.Series:
        """
        Calculates logarithmic returns from a list of prices.

        Args:
            prices (list): List of historical prices.

        Returns:
            pd.Series: Logarithmic returns.

        """
        logging.info(
            "CoinGeckoMonteCarloSimulation executing calculate_log_returns command ..."
        )
        price_df = pd.Series(prices)
        log_returns = np.log(price_df / price_df.shift(1))
        logging.info(
            "CoinGeckoMonteCarloSimulation successfully executed calculate_log_returns command."
        )
        return log_returns.dropna()

    def monte_carlo_simulation(
        self, log_returns, principal_amount, investment_horizon
    ) -> list:
        """
        Performs Monte Carlo simulations for future value prediction of a cryptocurrency investment.

        Args:
            log_returns (pd.Series): Logarithmic returns.
            principal_amount (float): The initial principal amount of the investment.
            investment_horizon (int): The investment horizon in days.

        Returns:
            list: List of future values from Monte Carlo simulations
        """
        logging.info(
            "CoinGeckoMonteCarloSimulation executing monte_carlo_simulation command ..."
        )
        returns = []
        for _ in range(self.num_simulations):
            random_log_returns = np.random.normal(
                log_returns.mean(), log_returns.std(), size=investment_horizon
            )
            future_values = np.exp(np.cumsum(random_log_returns))
            final_value = principal_amount * future_values[-1]
            returns.append(final_value)
        logging.info(
            "CoinGeckoMonteCarloSimulation successfully executed monte_carlo_simulation command."
        )
        return returns

    def run_simulation(self) -> list:
        """
        Runs simulations and returns the results.

        Returns:
            list: List of future values from Monte Carlo simulations.
        """
        logging.info(
            "CoinGeckoMonteCarloSimulation executing run_simulation command for crypto %s...",
            self.coin_id,
        )
        prices = self.fetch_price_data(self.coin_id, self.years)
        if prices is not None:
            log_returns = self.calculate_log_returns(prices)
            total_average_simulations = self.monte_carlo_simulation(
                log_returns, self.principal_amount, self.investment_horizon
            )
            logging.info(
                "CoinGeckoMonteCarloSimulation successfully executed run_simulation command for crypto %s.",
                self.coin_id,
            )
            return total_average_simulations

        else:
            logging.warning(
                "CoinGeckoMonteCarloSimulation failed to execute run_simulation for crypto %s. Will return empty list.",
                self.coin_id,
            )
            return []

    def visualize_simulation(self) -> str:
        """
        Visualizes Monte Carlo simulation results and additional information.

        Returns:
            str: HTML representation of the simulation visualization.
        """
        logging.info(
            "CoinGeckoMonteCarloSimulation executing visualize_simulation command for crypto %s...",
            self.coin_id,
        )
        average_future_values = self.run_simulation()
        simulation_number = list(range(1, len(average_future_values) + 1))

        average_future_value_df = pd.DataFrame(
            {
                "Simulation Number": simulation_number,
                "Average Future Value": average_future_values,
            }
        )
        if len(simulation_number) >= 50:
            # Create a figure with a single subplot
            fig, ax = plt.subplots(figsize=(14, len(simulation_number) / 4))
        else:
            fig, ax = plt.subplots(figsize=(14, 12))

        # Plot the bar chart
        average_future_value_df.plot.barh(
            y="Average Future Value", x="Simulation Number", legend=False, ax=ax
        )
        ax.set_xlabel("Average Future Value")
        ax.set_ylabel("Simulation Number")
        ax.grid(True)

        below_condition = (
            average_future_value_df["Average Future Value"] >= self.principal_amount
        )
        simulations_above_principal_amount = average_future_value_df[below_condition][
            "Average Future Value"
        ].count()

        # Display additional information as text
        tab_info = (
            f"Minimum of all Monte Carlo Simulations: {average_future_value_df['Average Future Value'].min():.2f}$",
            f"Maximum of all Monte Carlo Simulations: {average_future_value_df['Average Future Value'].max():.2f}$",
            f"Average of all Monte Carlo Simulations: {np.mean(average_future_value_df['Average Future Value']):.2f}$",
            f"Simulations above principal amount: {simulations_above_principal_amount}",
            f"Years of Price Data Collected: {self.years} years",
            f"Number of Simulations: {self.num_simulations}",
            f"Investment Horizon: {self.investment_horizon} days",
            f"Principal amount: {self.principal_amount}$",
            f"Cryptocurrency: {self.coin_id.capitalize()}",
        )

        # Add text annotations to the top of the plot
        spacing = 0.014  # Adjust this value as needed
        for i, line in enumerate(tab_info):
            ax.annotate(
                line,
                xy=(0.5, 1.02 + spacing * (i + 1)),
                xycoords="axes fraction",
                ha="center",
                va="center",
                fontsize=14,
            )

        # Convert the Matplotlib figure to HTML using mpld3
        graph_html = mpld3.fig_to_html(fig)
        plt.close(fig)
        logging.info(
            "CoinGeckoMonteCarloSimulation successfully executed visualize_simulation command for crypto %s.",
            self.coin_id,
        )
        return graph_html

    def visualize_history_graph(self) -> str:
        """
        Visualizes the historical price data graph along with additional information.

        Returns:
            str: HTML representation of the history graph visualization.
        """
        logging.info(
            "CoinGeckoMonteCarloSimulation executing visualize_history_graph command for crypto %s...",
            self.coin_id,
        )
        timestamps, prices = self.fetch_price_data(
            coin_id=self.coin_id, years=self.years, return_timestamps=True
        )
        history_graph = pd.DataFrame({"Timestamps": timestamps, "Prices": prices})

        # Plotting using Matplotlib
        fig, ax = plt.subplots(figsize=(14, 11))
        ax.plot(history_graph["Timestamps"], history_graph["Prices"])
        ax.set_xlabel("Timestamps")
        ax.set_ylabel("Prices in $")
        ax.grid(True)

        min_price = history_graph["Prices"].min()
        max_price = history_graph["Prices"].max()
        average_price = history_graph["Prices"].mean()

        # Find the index of the maximum value in the 'Prices' column
        max_price_index = history_graph["Prices"].idxmax()
        min_price_index = history_graph["Prices"].idxmin()

        # Use the index to get the corresponding timestamp
        timestamp_max_price = history_graph.loc[max_price_index, "Timestamps"]
        timestamp_min_price = history_graph.loc[min_price_index, "Timestamps"]

        # Add extra information at the top of the graph
        extra_info = [
            f"Cryptocurrency: {self.coin_id.capitalize()}",
            f"Years of Price Data Collected: {self.years} years",
            f"Maximum Price and date: {max_price:.2f}$ on {timestamp_max_price}",
            f"Minimum Price and date: {min_price:.2f}$ on {timestamp_min_price}",
            f"Average price per {self.years} years: {average_price:.2f}$",
        ]

        # Set the y-coordinate for the text
        y_coord = 1.1

        # Iterate over each line of text and place it on a different row
        for line in extra_info:
            ax.text(
                0.5,
                y_coord,
                line,
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=14,
            )
            y_coord -= 0.02  # Adjust this value to control the spacing between rows

        # Convert the Matplotlib figure to HTML using mpld3
        history_html = mpld3.fig_to_html(fig)
        plt.close(fig)  # Close the Matplotlib figure to free up resources
        logging.info(
            "CoinGeckoMonteCarloSimulation successfully executed visualize_history_graph command for crypto %s.",
            self.coin_id,
        )
        return history_html


if __name__ == "__main__":
    monte_carlo = CoinGeckoMonteCarloSimulation("bitcoin", 1, 1000, 100, 5)
    monte_carlo.visualize_history_graph()
