import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Настройка страницы
st.set_page_config(
    page_title="YouTube Analytics Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Светлая тема с кастомным CSS
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .channel-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .section-title {
        color: #2c3e50;
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Загрузка данных
@st.cache_data
def load_data():
    return pd.read_csv('youtube_channels.csv')

df = load_data()

# Заголовок
st.markdown("<h1 style='text-align: center; color: #2c3e50;'> YOUTUBE ANALYTICS PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #7f8c8d;'>Анализ топовых YouTube каналов мира</p>", unsafe_allow_html=True)

# Боковая панель
with st.sidebar:
    st.markdown("###  Панель управления")
    
    categories = st.multiselect(
        "Категории",
        options=df['category'].unique(),
        default=df['category'].unique()
    )
    
    countries = st.multiselect(
        "Страны",
        options=df['country'].unique(),
        default=df['country'].unique()
    )
    
    st.markdown("---")
    st.markdown("###Быстрая статистика")
    st.info(f"Всего каналов: {len(df)}")
    st.info(f"Общие просмотры: {df['total_views'].sum():,}")

# Применяем фильтры
filtered_df = df[
    (df['category'].isin(categories)) & 
    (df['country'].isin(countries))
]

# Верхние метрики - ИСПРАВЛЕННАЯ ВЕРСИЯ
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_subs = filtered_df['subscribers'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h4>Средние подписчики</h4>
        <h2>{avg_subs:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_earnings = filtered_df['monthly_earnings'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h4>Средний доход</h4>
        <h2>${avg_earnings:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_engagement = filtered_df['engagement_rate'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h4>Вовлеченность</h4>
        <h2>{avg_engagement:.2%}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_videos = filtered_df['total_videos'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <h4>Всего видео</h4>
        <h2>{total_videos:,}</h2>
    </div>
    """, unsafe_allow_html=True)

# Основной контент
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("###Распределение по категориям")
    category_counts = filtered_df['category'].value_counts()
    fig_pie = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.markdown("###Топ-5 каналов по подписчикам")
    top_channels = filtered_df.nlargest(5, 'subscribers')
    
    for i, (_, channel) in enumerate(top_channels.iterrows(), 1):
        st.markdown(f"""
        <div class="channel-card">
            <h4> {channel['channel_name']}</h4>
            <p><strong>Подписчики:</strong> {channel['subscribers']:,}</p>
            <p><strong>Доход:</strong> ${channel['monthly_earnings']:,}/месяц</p>
            <p><strong>Вовлеченность:</strong> {channel['engagement_rate']:.2%}</p>
        </div>
        """, unsafe_allow_html=True)

# Дополнительные графики
st.markdown("###Средний доход по категориям")
income_data = filtered_df.groupby('category')['monthly_earnings'].mean().sort_values(ascending=True)

fig_bar = px.bar(
    x=income_data.values,
    y=income_data.index,
    orientation='h',
    color=income_data.values,
    color_continuous_scale='Blues',
    labels={'x': 'Средний доход ($)', 'y': 'Категория'}
)
st.plotly_chart(fig_bar, use_container_width=True)

# Таблица данных
st.markdown("###Все каналы")
st.dataframe(
    filtered_df[['channel_name', 'category', 'subscribers', 'monthly_earnings', 'engagement_rate']],
    use_container_width=True,
    height=400
)