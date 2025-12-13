import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Read data from CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
ben_dir = os.path.join(script_dir, 'ben')
result_dir = os.path.join(script_dir, 'result')

# Create result directory if it doesn't exist
os.makedirs(result_dir, exist_ok=True)

# Read all txt files from ben directory
txt_files = glob.glob(os.path.join(ben_dir, '*.txt'))
all_data = []
for file in txt_files:
    df = pd.read_csv(file)
    all_data.append(df)

# Combine all dataframes
combined_df = pd.concat(all_data, ignore_index=True)

# Calculate average Memory_Usage_MB for each queue implementation
bbq_memory = combined_df[combined_df['Queue_Implementation'] == 'spmc_BBQ']['Memory_Usage_MB'].mean()
cffq_memory = combined_df[combined_df['Queue_Implementation'] == 'spmc_c-FFQ']['Memory_Usage_MB'].mean()
dffq_memory = combined_df[combined_df['Queue_Implementation'] == 'spmc_dFFQ']['Memory_Usage_MB'].mean()
rffq_memory = combined_df[combined_df['Queue_Implementation'] == 'spmc_r-FFQ']['Memory_Usage_MB'].mean()
davidq_memory = combined_df[combined_df['Queue_Implementation'] == 'spmc_DavidQueue']['Memory_Usage_MB'].mean()

# Prepare data for bar chart
queues = ['BBQ', 'c-FFQ', 'r-FFQ', 'dFFQ', 'DDQ ']
memories = [bbq_memory, cffq_memory, rffq_memory, dffq_memory, davidq_memory]
colors = ['#2E86AB', '#F18F01', '#C73E1D', '#A23B72', '#6A0572']

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Create bars
bars = ax.bar(queues, memories, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f} MB',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Formatting
ax.set_ylabel('Memory Usage (MB)', fontsize=12, fontweight='bold')
ax.set_title('Memory Usage Comparison', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(os.path.join(result_dir, 'memory_comparison.png'), dpi=300, bbox_inches='tight')
plt.show()

# Print summary
print("\n" + "="*60)
print("MEMORY USAGE SUMMARY")
print("="*60)
for queue, memory in zip(queues, memories):
    print(f"{queue:20s}: {memory:>10.2f} MB")
print("="*60)
