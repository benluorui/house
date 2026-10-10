import streamlit as st
import pandas as pd
import altair as alt

# 设置页面
st.set_page_config(
    page_title="California Housing Data (1990)",
    layout="wide"
)

# 缓存读取数据
@st.cache_data
def load_data():
    return pd.read_csv("housing.csv")

df = load_data()

# 1. 标题：请把 [Your Name] 换成你的名字
st.title("California Housing Data (1990) by [Your Name]")

# 2. 滑块：Minimal Median House Value
min_house_value = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000,
    step=1
)

# 3. 子标题
st.subheader("See more filters in the sidebar:")

# 4. 侧边栏多选：Choose the location type
location_types = sorted(df["ocean_proximity"].dropna().unique().tolist())
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types
)

# 5. 侧边栏单选：Choose income level
income_level = st.sidebar.radio(
    "Choose income level",
    ["Low", "Medium", "High"]
)

# 先按 Median House Value 过滤
filtered_df = df[df["median_house_value"] >= min_house_value].copy()

# 再按 ocean_proximity 过滤
filtered_df = filtered_df[
    filtered_df["ocean_proximity"].isin(selected_locations)
]

# 再按收入等级过滤
if income_level == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered_df = filtered_df[
        (filtered_df["median_income"] > 2.5) &
        (filtered_df["median_income"] < 4.5)
    ]
else:  # High
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]

# 6. 地图 + 7. 直方图
if filtered_df.empty:
    st.warning("No districts match the current filters.")
else:
    # 地图：st.map 默认识别 latitude / longitude
    st.map(filtered_df)

    # 直方图：median_house_value，30 bins
    hist = (
        alt.Chart(filtered_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "median_house_value:Q",
                bin=alt.Bin(maxbins=30),
                title="Median House Value"
            ),
            y=alt.Y("count():Q", title="Count")
        )
        .properties(title="Histogram of Median House Value")
    )
    st.altair_chart(hist, use_container_width=True)