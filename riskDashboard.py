from heatmap import RiskDashboard

# Initialize the RiskDashboard
dashboard = RiskDashboard(db_url='sqlite:///risk_dashboard.db')

# Generate the risk heatmap
fig = dashboard.generate_risk_heatmap()

# Show the heatmap
fig.show()
