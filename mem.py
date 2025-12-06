import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Read data from CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
ben_dir = os.path.join(script_dir, 'ben')
result_dir = os.path.join(script_dir, 'result')

# Create result directory if it doesn't exist
os.makedirs(result_dir, exist_ok=True)

# Read all CSV files
bbq_df = pd.read_csv(os.path.join(ben_dir, 'BBQ.csv'))
cffq_df = pd.read_csv(os.path.join(ben_dir, 'c-FFQ-10.csv'))
ddq_df = pd.read_csv(os.path.join(ben_dir, 'DDQ.csv'))
rffq_df = pd.read_csv(os.path.join(ben_dir, 'r-FFQ-10.csv'))

# Calculate average Queue_Capacity_Bytes across all measurements
bbq_capacity = bbq_df['Queue_Capacity_Bytes'].mean()
cffq_capacity = cffq_df['Queue_Capacity_Bytes'].mean()
ddq_capacity = ddq_df['Queue_Capacity_Bytes'].mean()
rffq_capacity = rffq_df['Queue_Capacity_Bytes'].mean()

# Prepare data for bar chart
queues = ['BBQ', 'c-FFQ (b=10)', 'DDQ', 'r-FFQ (b=10)']
capacities = [bbq_capacity, cffq_capacity, ddq_capacity, rffq_capacity]
colors = ['#2E86AB', '#F18F01', '#A23B72', '#C73E1D']

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Create bars
bars = ax.bar(queues, capacities, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    label = f'{height/1024:.1f} KB' if height > 1024 else f'{height:.0f} B'
    ax.text(bar.get_x() + bar.get_width()/2., height,
            label,
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Formatting
ax.set_ylabel('Queue Capacity (Bytes)', fontsize=12, fontweight='bold')
ax.set_title('Space Complexity Comparison (Queue Capacity)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Format y-axis to show values in KB or MB
max_capacity = max(capacities)

if max_capacity > 1024 * 1024:  # If larger than 1MB
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1024/1024:.1f}M'))
elif max_capacity > 1024:  # If larger than 1KB
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1024:.1f}K'))

plt.tight_layout()
plt.savefig(os.path.join(result_dir, 'memory_comparison.png'), dpi=300, bbox_inches='tight')
plt.show()

# Print summary
print("\n" + "="*60)
print("SPACE COMPLEXITY SUMMARY (Average Queue Capacity)")
print("="*60)
for queue, capacity in zip(queues, capacities):
    print(f"{queue:20s}: {capacity:>12.0f} bytes ({capacity/1024:>8.2f} KB)")
print("="*60)
