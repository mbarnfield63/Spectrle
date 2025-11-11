from adjustText import adjust_text
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd

# === Load and prepare ===
df = pd.read_csv("ExoTea_Master.csv")
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df = df.dropna(subset=['Date'])

winner_cols = [c for c in df.columns if c.lower().startswith("winner")]
df = df.dropna(subset=winner_cols, how='all')

melted = df.melt(id_vars='Date', value_vars=winner_cols,
                 var_name='WinnerSlot', value_name='Name')
melted['Name'] = melted['Name'].astype(str).str.strip()
melted = melted[melted['Name'] != '']

daily_counts = melted.groupby(
    ['Date', 'Name']).size().reset_index(name='Count')
pivot = daily_counts.pivot(
    index='Date', columns='Name', values='Count').fillna(0)

# Drop unwanted columns
pivot = pivot.drop(columns=[c for c in pivot.columns
                            if pd.isna(c)
                            or str(c).strip().lower() == 'nan'
                            or str(c).strip() == ''],
                   errors='ignore')

full_range = pd.date_range(pivot.index.min(), pivot.index.max(), freq='D')
pivot = pivot.reindex(full_range, fill_value=0)
pivot.index.name = 'Date'
cumulative = pivot.cumsum()

# === Plot cumulative lines ===
plt.figure(figsize=(13, 8))
lines = {}
last_counts = {}

names = cumulative.columns
num_names = len(names)

# Choose a colormap (e.g., 'tab20', 'viridis', 'plasma', 'Set3', etc.)
cmap = cm.get_cmap('tab20', num_names)  # discrete colours

for i, name in enumerate(names):
    y_vals = cumulative[name]
    plt.plot(cumulative.index, cumulative[name],
             color=cmap(i), label=name)
    last_counts[name] = y_vals.iloc[-1]

# === Group names with the same final cumulative value ===
grouped_labels = defaultdict(list)

for name, count in last_counts.items():
    grouped_labels[count].append(name)

# === Add aggregated labels to the right ===
texts = []
x_last = cumulative.index[-1]

for count, names in grouped_labels.items():
    label = ", ".join(names)  # join multiple names
    texts.append(plt.text(x_last + pd.Timedelta(days=3),
                 count, label, fontsize=8, va='center'))

# === Adjust labels to avoid overlap ===
adjust_text(
    texts,
    only_move={'points': 'y', 'text': 'y'},
    arrowprops=dict(arrowstyle="-", color='grey', lw=0.5),
    expand_points=(1.0, 1.2),
    expand_text=(1.0, 1.2),
    force_text=(0.1, 0.1)
)

# === Formatting ===
plt.title("Dingbat Winners over Time")
plt.xlabel("Date")
plt.ylabel("Cumulative Wins")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.xlim(cumulative.index.min(), cumulative.index.max() + pd.Timedelta(days=30))
plt.legend(loc='upper left')
plt.savefig('Dingbat_Winners.png', dpi=300)
