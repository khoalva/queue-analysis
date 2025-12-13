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

# Group by Queue_Implementation and MPI_Size, calculate mean Dequeue_Throughput_Ops_Per_Sec
def get_dequeue_throughput_by_nodes(df, queue_name):
    queue_df = df[df['Queue_Implementation'] == queue_name].copy()
    queue_df['Nodes'] = queue_df['MPI_Size'] / 8
    grouped = queue_df.groupby('Nodes')['Dequeue_Throughput_Ops_Per_Sec'].mean()
    return grouped

bbq_dequeue = get_dequeue_throughput_by_nodes(combined_df, 'spmc_BBQ')
cffq_dequeue = get_dequeue_throughput_by_nodes(combined_df, 'spmc_c-FFQ')
dffq_dequeue = get_dequeue_throughput_by_nodes(combined_df, 'spmc_dFFQ')
rffq_dequeue = get_dequeue_throughput_by_nodes(combined_df, 'spmc_r-FFQ')
davidq_dequeue = get_dequeue_throughput_by_nodes(combined_df, 'spmc_DavidQueue')

# Get all unique nodes values
all_nodes = sorted(set(bbq_dequeue.index) | set(cffq_dequeue.index) | 
                      set(dffq_dequeue.index) | set(rffq_dequeue.index) | set(davidq_dequeue.index))

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Plot lines for each queue
ax.plot(all_nodes, [bbq_dequeue.get(n, 0) for n in all_nodes], 
        marker='o', linewidth=2, markersize=8, label='BBQ', color='#2E86AB')
ax.plot(all_nodes, [cffq_dequeue.get(n, 0) for n in all_nodes], 
        marker='s', linewidth=2, markersize=8, label='c-FFQ', color='#F18F01')
ax.plot(all_nodes, [rffq_dequeue.get(n, 0) for n in all_nodes], 
        marker='D', linewidth=2, markersize=8, label='r-FFQ', color='#C73E1D')
ax.plot(all_nodes, [dffq_dequeue.get(n, 0) for n in all_nodes], 
        marker='^', linewidth=2, markersize=8, label='dFFQ', color='#A23B72')
ax.plot(all_nodes, [davidq_dequeue.get(n, 0) for n in all_nodes], 
        marker='*', linewidth=2, markersize=10, label='DDQ', color='#6A0572')

# Formatting
ax.set_xlabel('Number of Nodes (×8 cores)', fontsize=12, fontweight='bold')
ax.set_ylabel('Dequeue Throughput (items/sec)', fontsize=12, fontweight='bold')
ax.set_title('Dequeue Throughput Comparison (Log Scale)', fontsize=14, fontweight='bold')
ax.set_yscale('log')
ax.grid(True, alpha=0.3, linestyle='--', which='both')
ax.legend(fontsize=11, loc='best')
ax.set_xticks(all_nodes)

plt.tight_layout()
plt.savefig(os.path.join(result_dir, 'dequeue_throughput_comparison.png'), dpi=300, bbox_inches='tight')
plt.show()

# Print summary
print("\n" + "="*60)
print("DEQUEUE THROUGHPUT SUMMARY")
print("="*60)
print("="*60)
for nodes in all_nodes:
    cores = int(nodes * 8)
    print(f"\n{int(nodes)} Nodes ({cores} cores):")
    print(f"  BBQ:        {bbq_dequeue.get(nodes, 0):>10.2f} items/sec")
    print(f"  c-FFQ:      {cffq_dequeue.get(nodes, 0):>10.2f} items/sec")
    print(f"  r-FFQ:      {rffq_dequeue.get(nodes, 0):>10.2f} items/sec")
    print(f"  dFFQ:       {dffq_dequeue.get(nodes, 0):>10.2f} items/sec")
    print(f"  DDQ:        {davidq_dequeue.get(nodes, 0):>10.2f} items/sec")
print("="*60)
