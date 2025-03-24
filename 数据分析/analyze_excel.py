import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# 读取Excel文件
file_path = "E:\\Desktop\\1\\数据分析\\中国人口\\分地区人口的城乡构成和出生率、死亡率、自然增长率(2022年).xlsx"
df = pd.read_excel(file_path)

# 显示前几行数据
print("数据预览:")
print(df.head())

# 显示基本信息
print("\n基本信息:")
print(df.info())

# 显示列名
print("\n列名:")
print(df.columns.tolist())

# 显示行数和列数
print(f"\n表格大小: {df.shape[0]}行 x {df.shape[1]}列")

# 地区名称映射字典，将Excel中的地区名称映射到pyecharts支持的地区名称
region_map = {
    "北京市": "北京",
    "天津市": "天津",
    "河北省": "河北",
    "山西省": "山西",
    "内蒙古自治区": "内蒙古",
    "辽宁省": "辽宁",
    "吉林省": "吉林",
    "黑龙江省": "黑龙江",
    "上海市": "上海",
    "江苏省": "江苏",
    "浙江省": "浙江",
    "安徽省": "安徽",
    "福建省": "福建",
    "江西省": "江西",
    "山东省": "山东",
    "河南省": "河南",
    "湖北省": "湖北",
    "湖南省": "湖南",
    "广东省": "广东",
    "广西壮族自治区": "广西",
    "海南省": "海南",
    "重庆市": "重庆",
    "四川省": "四川",
    "贵州省": "贵州",
    "云南省": "云南",
    "西藏自治区": "西藏",
    "陕西省": "陕西",
    "甘肃省": "甘肃",
    "青海省": "青海",
    "宁夏回族自治区": "宁夏",
    "新疆维吾尔自治区": "新疆",
    "台湾省": "台湾",
    "香港特别行政区": "香港",
    "澳门特别行政区": "澳门"
}

# 绘制地图热力图函数
def create_map(data_series, title_name, file_name):
    # 过滤掉NaN值
    filtered_data = [(region, value) for region, value in data_series if pd.notna(value)]
    
    if not filtered_data:
        print(f"警告: {title_name}的数据全部为NaN，无法创建地图")
        return
    
    # 创建地图
    map_chart = Map(init_opts=opts.InitOpts(width="1200px", height="800px", theme=ThemeType.LIGHT))
    
    # 添加数据
    map_chart.add(
        series_name=title_name,
        data_pair=filtered_data,
        maptype="china",
        is_roam=True,  # 允许缩放和平移
    )
    
    # 设置全局选项
    map_chart.set_global_opts(
        title_opts=opts.TitleOpts(title=f"2022年中国各地区{title_name}"),
        visualmap_opts=opts.VisualMapOpts(
            min_=min([x[1] for x in filtered_data]),
            max_=max([x[1] for x in filtered_data]),
            is_piecewise=False,
            range_text=["高", "低"],
        ),
        tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c}"),
    )
    
    # 保存为HTML文件
    map_chart.render(f"E:\\Desktop\\1\\数据分析\\地图可视化\\{file_name}.html")
    print(f"{title_name}地图已保存为 {file_name}.html")

# 处理数据并绘制地图
def process_and_visualize():
    # 确保目录存在
    import os
    os.makedirs("E:\\Desktop\\1\\数据分析\\地图可视化", exist_ok=True)
    
    # 打印所有列名，帮助调试
    print("Excel中的列名:", df.columns.tolist())
    
    # 打印地区列的前几个值，帮助调试
    region_col = None
    for col in df.columns:
        if '地区' in col or '省份' in col or '省市' in col or '区域' in col:
            region_col = col
            break
    
    if region_col:
        print(f"找到地区列: {region_col}")
        print("地区列的前几个值:", df[region_col].head().tolist())
    else:
        print("警告: 未找到地区列，请检查Excel文件")
        return
    
    # 标准化地区名称
    df['标准地区名'] = df[region_col].map(lambda x: region_map.get(x, x) if isinstance(x, str) else x)
    
    # 打印标准化后的地区名称
    print("标准化后的地区名称:", df['标准地区名'].tolist())
    
    # 1. 出生率地图
    birth_rate_col = None
    for col in df.columns:
        if '出生率' in col:
            birth_rate_col = col
            break
    
    if birth_rate_col:
        print(f"找到出生率列: {birth_rate_col}")
        # 确保数据是数值类型
        df[birth_rate_col] = pd.to_numeric(df[birth_rate_col], errors='coerce')
        # 创建数据对
        birth_rate_data = []
        for idx, row in df.iterrows():
            if pd.notna(row['标准地区名']) and pd.notna(row[birth_rate_col]):
                birth_rate_data.append((row['标准地区名'], row[birth_rate_col]))
        
        print(f"出生率数据对数量: {len(birth_rate_data)}")
        create_map(birth_rate_data, "出生率(‰)", "birth_rate_map")
    else:
        print("警告: 未找到出生率列")
    
    # 2. 死亡率地图
    death_rate_col = None
    for col in df.columns:
        if '死亡率' in col:
            death_rate_col = col
            break
    
    if death_rate_col:
        print(f"找到死亡率列: {death_rate_col}")
        death_rate_data = [(region, float(rate) if pd.notna(rate) else None) 
                          for region, rate in zip(df['标准地区名'], df[death_rate_col])]
        create_map(death_rate_data, "死亡率(‰)", "death_rate_map")
    else:
        print("警告: 未找到死亡率列")
    
    # 3. 自然增长率地图
    growth_rate_col = None
    for col in df.columns:
        if '自然增长率' in col:
            growth_rate_col = col
            break
    
    if growth_rate_col:
        print(f"找到自然增长率列: {growth_rate_col}")
        growth_rate_data = [(region, float(rate) if pd.notna(rate) else None) 
                           for region, rate in zip(df['标准地区名'], df[growth_rate_col])]
        create_map(growth_rate_data, "自然增长率(‰)", "growth_rate_map")
    else:
        print("警告: 未找到自然增长率列")
    
    # 4. 城镇人口比例地图
    urban_col = None
    rural_col = None
    
    for col in df.columns:
        if '城镇人口' in col:
            urban_col = col
        elif '乡村人口' in col:
            rural_col = col
    
    if urban_col and rural_col:
        print(f"找到城镇人口列: {urban_col}")
        print(f"找到乡村人口列: {rural_col}")
        
        # 计算城镇人口比例
        df['城镇人口比例'] = df.apply(
            lambda row: (float(row[urban_col]) / (float(row[urban_col]) + float(row[rural_col])) * 100) 
            if pd.notna(row[urban_col]) and pd.notna(row[rural_col]) and (float(row[urban_col]) + float(row[rural_col])) > 0 
            else None, 
            axis=1
        )
        
        urban_ratio_data = [(region, ratio) for region, ratio in zip(df['标准地区名'], df['城镇人口比例'])]
        create_map(urban_ratio_data, "城镇人口比例(%)", "urban_ratio_map")
    else:
        print("警告: 未找到城镇人口或乡村人口列")

# 执行数据处理和可视化
process_and_visualize()