import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter
import matplotlib as mpl

# 设置中文黑体字体
font_path = 'C:/Windows/Fonts/simhei.ttf'  # Windows系统中黑体字体的路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 日本历史人口数据（单位：百万）
years = np.array([1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020])
population = np.array([83.2, 94.1, 104.3, 116.8, 123.5, 126.8, 128.1, 125.8])

# 年龄结构数据（2020年估计，百分比）
age_groups = ['0-14岁', '15-64岁', '65岁以上']
age_distribution_2020 = [12.6, 59.2, 28.2]  # 2020年日本人口年龄分布百分比

# 出生率和死亡率数据（每千人）
birth_rate_data = np.array([1990, 2000, 2010, 2020]), np.array([10.0, 9.4, 8.5, 7.3])
death_rate_data = np.array([1990, 2000, 2010, 2020]), np.array([6.7, 7.7, 9.5, 11.1])

# 定义人口预测模型（使用逻辑斯蒂曲线）
def logistic_model(x, a, b, c):
    return c / (1 + np.exp(-a * (x - b)))

# 拟合模型
# 使用curve_fit进行模型拟合，返回最优参数和协方差矩阵
# 使用curve_fit进行拟合，只返回参数和协方差矩阵
params, pcov = curve_fit(logistic_model, years - 1950, population, p0=[0.1, 50, 130])

# 预测未来人口
future_years = np.arange(1950, 2101, 10)
predicted_population = logistic_model(future_years - 1950, *params)

# 预测未来年龄结构变化（基于简化趋势）
# 假设老龄化趋势继续，年轻人口比例下降
young_ratio_future = np.array([12.6, 11.8, 11.0, 10.5, 10.0, 9.8, 9.5, 9.3, 9.0])
working_ratio_future = np.array([59.2, 56.0, 53.0, 50.0, 48.0, 46.0, 45.0, 44.0, 43.0])
elderly_ratio_future = np.array([28.2, 32.2, 36.0, 39.5, 42.0, 44.2, 45.5, 46.7, 48.0])
age_years = np.arange(2020, 2101, 10)

# 预测未来出生率和死亡率
future_birth_years = np.arange(1990, 2091, 10)  # 修改结束年份为2090，确保生成11个点
future_death_years = np.arange(1990, 2091, 10)  # 保持一致性

# 基于历史趋势的简化预测
birth_rate_future = np.array([10.0, 9.4, 8.5, 7.3, 6.8, 6.5, 6.3, 6.2, 6.1, 6.0, 6.0])  # 11个点
death_rate_future = np.array([6.7, 7.7, 9.5, 11.1, 12.5, 13.8, 14.5, 15.0, 15.3, 15.5, 15.6])  # 11个点

# 创建图表
plt.figure(figsize=(18, 12))

# 1. 总人口预测
plt.subplot(2, 2, 1)
plt.plot(years, population, 'bo-', label='历史人口')
plt.plot(future_years, predicted_population, 'r--', label='预测人口')
plt.title('日本人口预测 (1950-2100)', fontproperties=font_prop, fontsize=14)
plt.xlabel('年份', fontproperties=font_prop, fontsize=12)
plt.ylabel('人口 (百万)', fontproperties=font_prop, fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(prop=font_prop)

# 2. 年龄结构变化
plt.subplot(2, 2, 2)
plt.stackplot(age_years, young_ratio_future, working_ratio_future, elderly_ratio_future, 
              labels=['0-14岁', '15-64岁', '65岁以上'],
              colors=['#3498db', '#2ecc71', '#e74c3c'], alpha=0.8)
plt.title('日本人口年龄结构预测 (2020-2100)', fontproperties=font_prop, fontsize=14)
plt.xlabel('年份', fontproperties=font_prop, fontsize=12)
plt.ylabel('人口比例 (%)', fontproperties=font_prop, fontsize=12)
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(prop=font_prop, loc='upper right')

# 3. 出生率和死亡率变化
plt.subplot(2, 2, 3)
plt.plot(future_birth_years, birth_rate_future, 'g-o', label='出生率')
plt.plot(future_death_years, death_rate_future, 'm-o', label='死亡率')
plt.axvline(x=2020, color='gray', linestyle='--', alpha=0.7)
plt.title('日本出生率与死亡率预测 (1990-2100)', fontproperties=font_prop, fontsize=14)
plt.xlabel('年份', fontproperties=font_prop, fontsize=12)
plt.ylabel('每千人比率', fontproperties=font_prop, fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(prop=font_prop)

# 4. 人口金字塔 (2020年与2050年对比)
plt.subplot(2, 2, 4)

# 2020年简化人口金字塔数据
age_categories = ['0-14', '15-29', '30-44', '45-59', '60-74', '75+']
male_2020 = [7.5, 8.0, 9.5, 10.0, 9.0, 6.0]
female_2020 = [7.0, 7.5, 9.0, 10.0, 10.0, 7.5]

# 2050年预测人口金字塔数据
male_2050 = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
female_2050 = [4.5, 5.5, 6.5, 7.5, 9.5, 12.0]

y_pos = np.arange(len(age_categories))
bar_width = 0.35

# 绘制2050年预测
plt.barh(y_pos + bar_width/2, male_2050, bar_width, color='lightblue', alpha=0.8, label='2050年男性')
plt.barh(y_pos + bar_width/2, [-x for x in female_2050], bar_width, color='lightpink', alpha=0.8, label='2050年女性')

# 绘制2020年实际
plt.barh(y_pos - bar_width/2, male_2020, bar_width, color='blue', alpha=0.5, label='2020年男性')
plt.barh(y_pos - bar_width/2, [-x for x in female_2020], bar_width, color='red', alpha=0.5, label='2020年女性')

plt.yticks(y_pos, age_categories)
plt.title('日本人口金字塔对比 (2020 vs 2050)', fontproperties=font_prop, fontsize=14)
plt.xlabel('人口百分比 (%)', fontproperties=font_prop, fontsize=12)
plt.ylabel('年龄组', fontproperties=font_prop, fontsize=12)

# 自定义x轴标签，去掉负号
def millions_formatter(x, pos):
    return f'{abs(x):.1f}'

plt.gca().xaxis.set_major_formatter(FuncFormatter(millions_formatter))
plt.legend(prop=font_prop, loc='lower right')
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.suptitle('日本人口变化趋势分析与预测', fontproperties=font_prop, fontsize=18, y=0.98)
plt.subplots_adjust(top=0.9)

# 保存图表
plt.savefig('e:/Desktop/1/日本人口预测.png', dpi=300, bbox_inches='tight')

# 显示图表
plt.show()

# 输出关键数据点
print("日本人口预测关键数据点:")
for i, year in enumerate(future_years):
    if year % 20 == 0 and year >= 2020:
        print(f"{year}年: {predicted_population[i]:.1f}百万")

print("\n年龄结构变化:")
for i, year in enumerate(age_years):
    if year % 20 == 0:
        print(f"{year}年: 0-14岁: {young_ratio_future[i]:.1f}%, 15-64岁: {working_ratio_future[i]:.1f}%, 65岁以上: {elderly_ratio_future[i]:.1f}%")


# 使用指数平滑模型预测出生率和死亡率
def exponential_smoothing(data, alpha=0.3, horizon=7):
    result = [data[0]]  # 初始化结果列表
    # 计算历史数据的平滑值
    for n in range(1, len(data)):
        result.append(alpha * data[n] + (1 - alpha) * result[n-1])
    # 预测未来值
    last = result[-1]
    for _ in range(horizon):
        # 使用衰减因子对趋势进行调整
        decay = 0.95  # 衰减率
        trend = (result[-1] - result[-2]) * decay
        last = last + trend
        result.append(last)
    return np.array(result)

# 历史数据
birth_rates = np.array([10.0, 9.4, 8.5, 7.3])  # 1990-2020的数据
death_rates = np.array([6.7, 7.7, 9.5, 11.1])  # 1990-2020的数据

# 使用指数平滑预测
birth_rate_future = exponential_smoothing(birth_rates, alpha=0.3, horizon=7)
death_rate_future = exponential_smoothing(death_rates, alpha=0.3, horizon=7)

# 确保预测值在合理范围内
birth_rate_future = np.clip(birth_rate_future, 4.0, 10.0)  # 限制出生率范围
death_rate_future = np.clip(death_rate_future, 6.0, 18.0)  # 限制死亡率范围