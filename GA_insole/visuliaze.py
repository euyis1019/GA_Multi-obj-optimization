import pandas as pd
import plotly.express as px

# 加载数据
file_path = 'High_arch.csv'  # 确保这是正确的文件路径
data = pd.read_excel(file_path)

fig = px.scatter_3d(data, x='x坐标', y='y坐标', z='z坐标', size_max=10, opacity=0.7)
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
fig.update_traces(marker=dict(size=2))

# 确定所有坐标轴的最大范围
max_axis_range = max(data['x坐标'].max(), data['y坐标'].max(), data['z坐标'].max())

# 更新坐标轴范围
fig.update_layout(scene=dict(
    xaxis=dict(range=[-270, 270]),
    yaxis=dict(range=[-270, 270]),
    zaxis=dict(range=[-270, 270]),
    aspectmode='cube'  # 确保所有轴的比例一致
))


# 显示图表
fig.show()
