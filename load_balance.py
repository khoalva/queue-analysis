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

# Group by MPI_Size and calculate mean Load_Balance_Score
def get_load_balance_by_nodes(df):
    # Convert MPI_Size to number of nodes (MPI_Size / 8)
    df['Nodes'] = df['MPI_Size'] / 8
    grouped = df.groupby('Nodes')['Load_Balance_Score'].mean()
    return grouped

bbq_load_balance = get_load_balance_by_nodes(bbq_df)
cffq_load_balance = get_load_balance_by_nodes(cffq_df)
ddq_load_balance = get_load_balance_by_nodes(ddq_df)
rffq_load_balance = get_load_balance_by_nodes(rffq_df)

# Get all unique nodes values
all_nodes = sorted(set(bbq_load_balance.index) | set(cffq_load_balance.index) | 
                      set(ddq_load_balance.index) | set(rffq_load_balance.index))

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Plot lines for each queue
ax.plot(all_nodes, [bbq_load_balance.get(n, 0) for n in all_nodes], 
        marker='o', linewidth=2, markersize=8, label='BBQ', color='#2E86AB')
ax.plot(all_nodes, [cffq_load_balance.get(n, 0) for n in all_nodes], 
        marker='s', linewidth=2, markersize=8, label='c-FFQ (b=10)', color='#F18F01')
ax.plot(all_nodes, [ddq_load_balance.get(n, 0) for n in all_nodes], 
        marker='^', linewidth=2, markersize=8, label='DDQ', color='#A23B72')
ax.plot(all_nodes, [rffq_load_balance.get(n, 0) for n in all_nodes], 
        marker='D', linewidth=2, markersize=8, label='r-FFQ (b=10)', color='#C73E1D')

# Formatting
ax.set_xlabel('Number of Nodes (×8 cores)', fontsize=12, fontweight='bold')
ax.set_ylabel('Load Balance Score', fontsize=12, fontweight='bold')
ax.set_title('Load Balance Comparison', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='best')
ax.set_xticks(all_nodes)
ax.set_ylim(0, 105)  # Score is typically 0-100

plt.tight_layout()
plt.savefig(os.path.join(result_dir, 'load_balance_comparison.png'), dpi=300, bbox_inches='tight')
plt.show()

# Print summary
print("\n" + "="*60)
print("LOAD BALANCE SCORE SUMMARY")
print("="*60)
print("Note: Higher score = better load balance (0-100 scale)")
print("="*60)
for nodes in all_nodes:
    cores = int(nodes * 8)
    print(f"\n{int(nodes)} Nodes ({cores} cores):")
    print(f"  BBQ:        {bbq_load_balance.get(nodes, 0):>6.1f}")
    print(f"  c-FFQ:      {cffq_load_balance.get(nodes, 0):>6.1f}")
    print(f"  DDQ:        {ddq_load_balance.get(nodes, 0):>6.1f}")
    print(f"  r-FFQ:      {rffq_load_balance.get(nodes, 0):>6.1f}")
print("="*60)
