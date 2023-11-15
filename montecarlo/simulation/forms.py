from django import forms

class MonteCarloForm(forms.Form):
    coin_id = forms.CharField(max_length=50, label='Cryptocurrency')
    years = forms.IntegerField(label='Years of Historical Data')
    principal_amount = forms.FloatField(label='Initial Principal Amount')
    investment_horizon = forms.IntegerField(label='Investment Horizon (Years)')
    num_simulations = forms.IntegerField(label='Number of Monte Carlo Simulations')
