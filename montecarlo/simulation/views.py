from django.shortcuts import render
from .forms import MonteCarloForm
from .monte_carlo import CoinGeckoMonteCarloSimulation
from django.contrib import messages
def montecarlo(request):
    if request.method == 'POST':
        form = MonteCarloForm(request.POST)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            coin_id = cleaned_data['coin_id']
            years = cleaned_data['years']
            principal_amount = cleaned_data['principal_amount']
            investment_horizon = cleaned_data['investment_horizon']
            num_simulations = cleaned_data['num_simulations']

            monte_carlo = CoinGeckoMonteCarloSimulation(
                coin_id, years, principal_amount, investment_horizon, num_simulations)
            results = monte_carlo.run_simulation_and_get_results()

            if not results:
                messages.error(request, f"Cryptocurrency symbol {coin_id} is not a valid! Try again ...")    
            return render(request, 'simulation/montecarlo.html', {'form': form, 'results': results})
        
        else:
            messages.error(request, "Fill all tabs in form before running simulation")
    else:
        form = MonteCarloForm()
    return render(request, 'simulation/montecarlo.html', {'form': form})
