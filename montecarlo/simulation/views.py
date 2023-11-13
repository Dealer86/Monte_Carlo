from django.shortcuts import render, redirect
from .forms import MonteCarloForm
from .monte_carlo import CoinGeckoMonteCarloSimulation
from django.contrib import messages
import mpld3

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
            try:
                graph_html = monte_carlo.visualize_simulation()
                history_html = monte_carlo.visualize_history_graph()
            except IndexError:
                messages.error(request, f"Cryptocurrency symbol {coin_id} is not a valid! Try again ...") 
                return redirect('montecarlo')
            
            return render(request, 'simulation/montecarlo.html', {'form': form, "graph_html": graph_html, 'history_html': history_html})
        
        else:
            messages.error(request, "Fill all tabs before running simulation!")
    else:
        form = MonteCarloForm()
    return render(request, 'simulation/montecarlo.html', {'form': form})
