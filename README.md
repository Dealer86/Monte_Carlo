# Monte Carlo
Monte Carlo is a simulation and uses CoinGecko API. This fintech app fetches historical cryptocurrency price data and performs Monte Carlo simulations for future value prediction of a cryptocurrency investment with logarithmic returns, generating interactive graphs.

## Video Presentation


## Deployment Instructions
### Windows:
1. Clone the git repository: `git clone https://github.com/Dealer86/Monte_Carlo.git`.
2. CD into your created directory.
3. Create a new virtual environment by running `python -m venv env/`.
4. Activate the virtual environment by running `.\env\Scripts\activate`.
5. Upgrade pip by running `python.exe -m pip install --upgrade pip`.
6. Install the required dependencies by running `pip install -r requirements.txt`.
7. CD into the montecarlo directory where manage.py module lives.
8. Run: `python manage.py runserver`
9. Check http://127.0.0.1:8000/.

## Technology Stack
### Django Web Framework
- **Django**: The core web framework for building the project.

### Backend
- **Python 3.11**: The primary programming language for the backend logic.
- **Requests**: Python library for making HTTP requests.
- **NumPy**: Library for numerical computations in Python.
- **Pandas**: Data manipulation and analysis library.
- **Matplotlib**: Plotting library for creating visualizations.
- **mpld3**: Matplotlib-based library for D3.js-inspired interactive visualizations.

### Frontend
- **HTML**: Used for structuring web pages.
- **CSS**: Applied for styling the user interface.
- **Bootstrap**: Front-end framework for creating responsive and modern UI components.

### Testing
- **Unit Tests**: Using Django's built-in testing framework.
- **Continuous Integration**: This project uses GitHub Actions for automated continuous integration.
- **GitHub Actions Status Badge** [![Django CI](https://github.com/Dealer86/Monte_Carlo/actions/workflows/django.yml/badge.svg)](https://github.com/Dealer86/Monte_Carlo/actions/workflows/django.yml)

### Third-Party Tools
- **OBS**: Used for video presentation.
- **DaVinci Resolve**: Video editing.

### License

- This project is licensed under the [MIT License](LICENSE).