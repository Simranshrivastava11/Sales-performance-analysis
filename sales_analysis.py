import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
n = 1000

regions     = ['North', 'South', 'East', 'West']
categories  = ['Electronics', 'Furniture', 'Office Supplies', 'Clothing']
months      = pd.date_range('2023-01-01', periods=12, freq='MS')

data = {
    'Order_ID'      : [f'ORD-{1000+i}' for i in range(n)],
    'Month'         : np.random.choice(months, n),
    'Region'        : np.random.choice(regions, n, p=[0.3,0.25,0.25,0.2]),
    'Category'      : np.random.choice(categories, n, p=[0.35,0.25,0.25,0.15]),
    'Sales'         : np.random.randint(200, 5000, n),
    'Discount'      : np.round(np.random.choice([0, 0.05, 0.1, 0.2, 0.3], n), 2),
    'Units_Sold'    : np.random.randint(1, 50, n),
}

df = pd.DataFrame(data)
df['Profit'] = (df['Sales'] * (1 - df['Discount']) * 0.25).round(2)
df['Month_Name'] = df['Month'].dt.strftime('%b %Y')

df.to_csv('sales_data.csv', index=False)
print("sales_data.csv saved!")
print(df.head())

print("\nKEY INSIGHTS:")
print(f"Total Revenue    : ${df['Sales'].sum():,.0f}")
print(f"Total Profit     : ${df['Profit'].sum():,.0f}")
print(f"Avg Profit Margin: {(df['Profit'].sum()/df['Sales'].sum()*100):.1f}%")
print(f"\nRevenue by Region:\n{df.groupby('Region')['Sales'].sum().sort_values(ascending=False)}")
print(f"\nRevenue by Category:\n{df.groupby('Category')['Sales'].sum().sort_values(ascending=False)}")


fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Sales Performance Dashboard - 2023', fontsize=16, fontweight='bold')


monthly = df.groupby('Month')['Sales'].sum().reset_index()
axes[0,0].plot(monthly['Month'], monthly['Sales'], marker='o', color='steelblue', linewidth=2)
axes[0,0].set_title('Monthly Revenue Trend')
axes[0,0].set_ylabel('Revenue ($)')
axes[0,0].tick_params(axis='x', rotation=45)


region_data = df.groupby('Region')['Sales'].sum().sort_values()
axes[0,1].barh(region_data.index, region_data.values, color='coral')
axes[0,1].set_title('Revenue by Region')
axes[0,1].set_xlabel('Revenue ($)')


cat_data = df.groupby('Category')['Profit'].sum().sort_values()
axes[1,0].bar(cat_data.index, cat_data.values, color='mediumseagreen')
axes[1,0].set_title('Profit by Category')
axes[1,0].set_ylabel('Profit ($)')
axes[1,0].tick_params(axis='x', rotation=15)


axes[1,1].scatter(df['Discount'], df['Profit'], alpha=0.4, color='mediumpurple')
axes[1,1].set_title('Discount vs Profit Impact')
axes[1,1].set_xlabel('Discount Rate')
axes[1,1].set_ylabel('Profit ($)')

plt.tight_layout()
plt.savefig('sales_dashboard.png', dpi=150)
plt.show()
print("sales_dashboard.png saved!")