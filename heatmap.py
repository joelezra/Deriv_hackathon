import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Position, Client
import numpy as np
import requests

class RiskDashboard:
    def __init__(self, db_url='sqlite:///risk_dashboard.db'):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def generate_risk_heatmap(self):
        # Query positions data grouped by client and asset
        positions = self.session.query(
            Client.name,
            Position.asset,
            func.sum(Position.position_size * Position.price).label('total_value')
        ).join(Client).group_by(Client.name, Position.asset).all()

        # Convert to DataFrame
        df = pd.DataFrame(positions, columns=['client', 'asset', 'total_value'])
        pivot_value = df.pivot(index='client', columns='asset', values='total_value')
        
        # Create heatmap with reversed color scale
        fig = go.Figure(data=go.Heatmap(
            z=pivot_value.values,
            x=pivot_value.columns,
            y=pivot_value.index,
            colorscale='RdYlGn_r',  # Reversed color scale
            text=np.round(pivot_value.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))

        fig.update_layout(
            title='Asset Value Concentration Heatmap by Client and Asset',
            xaxis_title='Asset',
            yaxis_title='Client'
        )

        return fig

    def set_risk_alerts(self, thresholds):
        """
        Set up risk alerts based on specified thresholds
        thresholds: dict with keys 'var', 'exposure', 'loss' and corresponding values
        """
        alerts = []
        
        # Check VaR thresholds
        positions = self.session.query(
            Client.name,
            func.sum(Position.pnl).label('total_pnl'),
            func.sum(Position.position_size * Position.price).label('total_exposure')
        ).join(Client).group_by(Client.name).all()

        for position in positions:
            if position.total_exposure > thresholds['exposure']:
                alerts.append(f"ALERT: {position.name} exposure ({position.total_exposure}) exceeds threshold")
            if position.total_pnl < -thresholds['loss']:
                alerts.append(f"ALERT: {position.name} losses ({position.total_pnl}) exceed threshold")

        return alerts

    def generate_risk_report(self):
        """Generate comprehensive risk report"""
        report = {
            'total_exposure': {},
            'pnl_by_client': {},
            'risk_concentration': {}
        }

        # Calculate total exposure by asset
        exposures = self.session.query(
            Position.asset,
            func.sum(Position.position_size * Position.price).label('total_exposure')
        ).group_by(Position.asset).all()
        
        for exposure in exposures:
            report['total_exposure'][exposure.asset] = exposure.total_exposure

        # Calculate PnL by client
        pnls = self.session.query(
            Client.name,
            func.sum(Position.pnl).label('total_pnl')
        ).join(Client).group_by(Client.name).all()
        
        for pnl in pnls:
            report['pnl_by_client'][pnl.name] = pnl.total_pnl

        return report

    def fetch_and_print_closing_prices():
        # Fetch data from API endpoint
        api_url = 'http://tayar.pro:8000/get_klines/btc/1day'
        try:
            response = requests.get(api_url)
            data = response.json()

            # Extract the latest 100 data points
            latest_open = data['o'][-100:]
            latest_high = data['h'][-100:]
            latest_low = data['l'][-100:]
            # Fetch the latest 100 closing prices
            latest_close = data['c'][-100:]
            print("Latest 100 Closing Prices:")
            print(latest_close)

        except Exception as e:
            print(f"Error fetching data from API: {e}")
            return

        # Convert to a DataFrame
        closing_prices_df = pd.DataFrame(latest_close, columns=['Close']).diff().dropna()
        sorted_closing_prices_df = closing_prices_df.sort_values(by='Close', ascending=True)
        print("\nDataFrame of Latest 100 Closing Prices:")
        print(sorted_closing_prices_df)
  
    def calculate_var(self, confidence_level=0.95):
        
        # Fetch data from API endpoint
        api_url = 'http://tayar.pro:8000/get_klines/btc/1day'
        try:
            response = requests.get(api_url)
            data = response.json()

            # Extract the latest 100 data points
            latest_open = data['o'][-100:]
            latest_high = data['h'][-100:]
            latest_low = data['l'][-100:]
            # Fetch the latest 100 closing prices
            latest_close = data['c'][-100:]
            
            

        except Exception as e:
            print(f"Error fetching data from API: {e}")

        # Convert to a DataFrame
        closing_prices_df = pd.DataFrame(latest_close, columns=['Close']).diff().dropna()
        sorted_closing_prices_df = closing_prices_df.sort_values(by='Close', ascending=True)
        print("\nDataFrame of Latest 100 Closing Prices:")
        print(sorted_closing_prices_df)
        # print(closing_prices_df)

        # Calculate daily returns
        returns = closing_prices_df['Close']

        # Simulate portfolio returns
        # Assuming a single asset, the portfolio return is the same as the asset return
        portfolio_returns = returns.sort_values(ascending=True)
        # print(portfolio_returns)


        # Calculate VaR
        var = np.percentile(portfolio_returns, (1 - confidence_level) * 100)

        print(f"Value at Risk (VaR) at {confidence_level*100}% confidence level: {var}")

    def fetch_historical_prices(self):
        # Placeholder for fetching historical price data
        # Replace with actual data fetching logic
        return pd.DataFrame({
            'Asset1': np.random.normal(0, 0.01, 100),
            'Asset2': np.random.normal(0, 0.01, 100)
        })

    def get_portfolio_weights(self):
        # Placeholder for portfolio weights
        # Replace with actual logic to calculate or fetch portfolio weights
        return np.array([0.5, 0.5])

import requests
import pandas as pd

def fetch_and_print_closing_prices():
    # Fetch data from API endpoint
    api_url = 'http://tayar.pro:8000/get_klines/btc/1day'
    try:
        response = requests.get(api_url)
        data = response.json()

        # Extract the latest 100 data points
        latest_open = data['o'][-100:]
        latest_high = data['h'][-100:]
        latest_low = data['l'][-100:]
        # Fetch the latest 100 closing prices
        latest_close = data['c'][-100:]
        print("Latest 100 Closing Prices:")
        print(latest_close)

    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return

    # Convert to a DataFrame
    closing_prices_df = pd.DataFrame(latest_close, columns=['Close']).diff().dropna()
    sorted_closing_prices_df = closing_prices_df.sort_values(by='Close', ascending=True)
    print("\nDataFrame of Latest 100 Closing Prices:")
    print(sorted_closing_prices_df)

# Run the function to test
fetch_and_print_closing_prices()

# Create an instance of the class
risk_dashboard = RiskDashboard()

# Call the method
risk = risk_dashboard.calculate_var(confidence_level=0.95)
print(risk)
