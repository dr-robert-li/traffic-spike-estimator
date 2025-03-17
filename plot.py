import numpy as np
import matplotlib.pyplot as plt
import argparse
from matplotlib.colors import to_rgba

# Parse arguments
parser = argparse.ArgumentParser(description='Plot traffic spike magnitudes with custom traffic input')
parser.add_argument('--traffic', type=float, default=None, 
                    help='Daily traffic figure to calculate spike magnitude (users/day)')
args = parser.parse_args()

# Define model functions
def upper_bound(T):
    return 593.61 * T ** -0.2974

def median_estimate(T):
    return 430.3 * T ** -0.3857

def lower_bound(T):
    return 344.27 * T ** -0.412

# Define colors
upper_color = 'blue'
median_color = 'orange'
lower_color = 'green'

# Set up plot
plt.figure(figsize=(10, 7))

# Determine traffic range
default_min = 1e3  # 1,000 users/day
default_max = 1e8  # 100,000,000 users/day

if args.traffic is not None:
    traffic = args.traffic
    x_min = max(1, traffic * 0.5) if traffic < default_min else default_min
    x_max = traffic * 1.5 if traffic > default_max else default_max
    T_values = np.logspace(np.log10(x_min), np.log10(x_max), num=1000)
else:
    T_values = np.logspace(np.log10(default_min), np.log10(default_max), num=1000)

# Calculate spike magnitudes
upper_values = upper_bound(T_values)
median_values = median_estimate(T_values)
lower_values = lower_bound(T_values)

# Create gradient shading with fade-out effect
def create_gradient_shading(x_values, y_values, lower_y_values=None, base_color='blue', num_layers=15):
    rgba_color = to_rgba(base_color)
    bottom_boundary = np.zeros_like(y_values) + 0.1 if lower_y_values is None else lower_y_values * 1.1
    vertical_space = y_values - bottom_boundary
    
    for i in range(num_layers):
        fraction = i / num_layers
        power = 3.5
        layer_fraction = 1 - (fraction ** (1/power))
        layer_y = y_values - vertical_space * (1 - layer_fraction)
        alpha = 0.4 * np.exp(-4 * fraction)
        fill_color = (rgba_color[0], rgba_color[1], rgba_color[2], alpha)
        
        if i < num_layers - 1:
            next_fraction = (i + 1) / num_layers
            next_layer_fraction = 1 - (next_fraction ** (1/power))
            next_layer_y = y_values - vertical_space * (1 - next_layer_fraction)
            plt.fill_between(x_values, layer_y, next_layer_y, color=fill_color, edgecolor=None)
        else:
            plt.fill_between(x_values, layer_y, bottom_boundary, color=fill_color, edgecolor=None)

# Add gradient shading
create_gradient_shading(T_values, upper_values, median_values, upper_color)
create_gradient_shading(T_values, median_values, lower_values, median_color)
create_gradient_shading(T_values, lower_values, None, lower_color)

# Plot trend lines
plt.plot(T_values, upper_values, label='Upper Bound (Worst-Case Scenarios)', linewidth=2, color=upper_color)
plt.plot(T_values, median_values, label='Median Estimate Maximum', linewidth=2, color=median_color)
plt.plot(T_values, lower_values, label='Lower Bound Maximum', linewidth=2, color=lower_color)

# Mark known data points
plt.scatter([15000, 1e7, 1e8], [35, 4.4, 2.69], color=upper_color, marker='o', s=80, zorder=5, label='Upper Bound Known Data Points')
plt.scatter([1000, 3e6], [30, 1.37], color=median_color, marker='o', s=80, zorder=5, label='Median Known Data Points')
plt.scatter([1000, 1e5], [20, 3], color=lower_color, marker='o', s=80, zorder=5, label='Lower Bound Known Data Points')

# Handle user-provided traffic input
if args.traffic is not None:
    traffic = args.traffic
    upper = upper_bound(traffic)
    median = median_estimate(traffic)
    lower = lower_bound(traffic)
    
    # Add vertical line for user input
    plt.axvline(x=traffic, color='red', linestyle='--', alpha=0.7, 
                label=f'Traffic: {traffic:,.0f} users/day')
    
    # Mark intersection points
    plt.scatter([traffic], [upper], color=upper_color, marker='x', s=150, 
                linewidths=3, edgecolors='white', zorder=6,
                label=f'Upper Bound: {upper:.2f}x')
    
    plt.scatter([traffic], [median], color=median_color, marker='x', s=150, 
                linewidths=3, edgecolors='white', zorder=6,
                label=f'Median Estimate: {median:.2f}x')
    
    plt.scatter([traffic], [lower], color=lower_color, marker='x', s=150, 
                linewidths=3, edgecolors='white', zorder=6,
                label=f'Lower Bound: {lower:.2f}x')
    
    plt.title(f'Traffic Spike Magnitude Bounds (Input: {traffic:,.0f} users/day)', fontsize=14)
    
    # Adjust y-axis scale based on traffic
    if traffic > 1e7:
        max_spike = max(upper, median, lower)
        min_spike = min(upper, median, lower) * 0.8
        plt.ylim(min_spike, max_spike * 1.5)
    elif traffic > 1e6:
        max_spike = max(upper, median, lower)
        plt.ylim(0, max_spike * 2)
else:
    plt.title('Traffic Spike Magnitude Bounds (Linear Spike Scale, Logarithmic Traffic Scale)', fontsize=14)

# Configure axes
plt.xscale('log')
plt.xlabel('Mean Daily Traffic (users/day) [Log Scale]', fontsize=12)
plt.ylabel('Maximum Spike Magnitude (Multiplier)', fontsize=12)
plt.xlim(T_values[0], T_values[-1])

# Finalize plot
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.legend(loc='best', fontsize=10)
plt.tight_layout()
plt.show()