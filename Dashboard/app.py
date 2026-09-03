import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

NETFLIX_RED = "#E50914"
NETFLIX_DARK = "#1a1a1a"
NETFLIX_BLACK = "#141414"
NETFLIX_GRAY = "#808080"
NETFLIX_LIGHT = "#b3b3b3"
COLOR_SEQ = [
    "#E50914", "#F5A623", "#4A90D9", "#7ED321",
    "#9B59B6", "#1ABC9C", "#E67E22", "#2ECC71",
    "#3498DB", "#E74C3C",
]

pio.templates["netflix_dark"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,26,26,0.6)",
        font=dict(color="#b3b3b3", family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#2a2a2a", zerolinecolor="#2a2a2a"),
        yaxis=dict(gridcolor="#2a2a2a", zerolinecolor="#2a2a2a"),
    )
)
pio.templates.default = "netflix_dark"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(26,26,26,0.6)",
    font=dict(color="#b3b3b3", family="Inter, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
)

st.set_page_config(
    page_title="Netflix Content Analytics",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #141414;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #1a1a1a;
    border-right: 1px solid #2a2a2a;
}
[data-testid="stSidebar"] * {
    color: #b3b3b3 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {
    color: #808080 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}
.metric-card {
    background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: #E50914;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.72rem;
    color: #808080;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.35rem;
}
.metric-delta {
    font-size: 0.78rem;
    margin-top: 0.4rem;
    font-weight: 500;
}
.metric-delta.positive { color: #2ECC71; }
.metric-delta.neutral  { color: #F5A623; }
.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #ffffff;
    margin: 0.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #E50914;
    display: inline-block;
}
.insight-box {
    background: linear-gradient(135deg, rgba(229,9,20,0.08) 0%, rgba(26,26,26,0.9) 100%);
    border: 1px solid rgba(229,9,20,0.25);
    border-left: 3px solid #E50914;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #b3b3b3;
    line-height: 1.6;
}
.insight-box strong { color: #ffffff; }
[data-baseweb="tab-list"] {
    background-color: #1a1a1a !important;
    border-bottom: 1px solid #2a2a2a;
    gap: 0;
}
[data-baseweb="tab"] {
    background-color: transparent !important;
    color: #808080 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    transition: all 0.2s;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: #ffffff !important;
    border-bottom: 2px solid #E50914 !important;
}
[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    overflow: hidden;
}
.stDataFrame { border-radius: 8px; }
div[data-testid="stMarkdownContainer"] h1 { color: #ffffff; }
.sidebar-header {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #555 !important;
    margin-bottom: 0.3rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid #2a2a2a;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_and_clean():
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir.parent / "Dataset" / "netflix_titles.csv",
        base_dir / "Dataset" / "netflix_titles.csv",
        Path("Dataset/netflix_titles.csv"),
        Path("../Dataset/netflix_titles.csv"),
    ]
    data_path = None
    for p in candidates:
        if p.exists():
            data_path = p
            break
    if data_path is None:
        raise FileNotFoundError("Could not find netflix_titles.csv in expected locations.")

    df = pd.read_csv(data_path)

    anomalies = df[df["rating"].str.contains("min", na=False)]
    for idx in anomalies.index:
        df.loc[idx, "duration"] = df.loc[idx, "rating"]
        df.loc[idx, "rating"] = np.nan

    df["director"] = df["director"].fillna("Unknown")
    df["cast"] = df["cast"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")

    df = df.dropna(subset=["date_added", "rating", "duration"])

    df["date_added"] = pd.to_datetime(df["date_added"].str.strip())
    df["year_added"] = df["date_added"].dt.year.astype(int)
    df["month_added"] = df["date_added"].dt.month
    df["month_name"] = df["date_added"].dt.strftime("%B")

    df["duration_clean"] = df["duration"].str.extract(r"(\d+)").astype(float)
    df["lag_years"] = df["year_added"] - df["release_year"]

    return df


def apply_filters(df, content_type, year_range, countries, ratings, genres):
    filtered = df.copy()
    if content_type != "All":
        filtered = filtered[filtered["type"] == content_type]
    filtered = filtered[
        (filtered["year_added"] >= year_range[0]) &
        (filtered["year_added"] <= year_range[1])
    ]
    if countries:
        mask = filtered["country"].apply(
            lambda c: any(ct.strip() in str(c) for ct in countries)
        )
        filtered = filtered[mask]
    if ratings:
        filtered = filtered[filtered["rating"].isin(ratings)]
    if genres:
        mask = filtered["listed_in"].apply(
            lambda g: any(gn.strip() in str(g) for gn in genres)
        )
        filtered = filtered[mask]
        filtered = filtered[mask]
    return filtered


def fmt_number(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(int(n))


def metric_card(label, value, delta=None, delta_type="neutral"):
    delta_html = ""
    if delta:
        delta_html = f'<div class="metric-delta {delta_type}">{delta}</div>'
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """


with st.spinner("Loading dataset..."):
    df = load_and_clean()

all_years = sorted(df["year_added"].unique())
all_ratings = sorted(df["rating"].dropna().unique())
all_genres_flat = sorted(
    set(g.strip() for gl in df["listed_in"].dropna() for g in gl.split(","))
)
all_countries_flat = sorted(
    set(c.strip()
        for cl in df[(df["country"] != "Unknown") & df["country"].notna()]["country"]
        for c in str(cl).split(",")
        if c.strip() and c.strip().lower() != "nan")
)

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1.5rem 0;">
        <span style="font-size:2rem; font-weight:900; color:#E50914; letter-spacing:-0.03em;">NETFLIX</span>
        <div style="font-size:0.65rem; color:#555; letter-spacing:0.15em; text-transform:uppercase; margin-top:0.2rem;">
            Content Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-header">Content Type</div>', unsafe_allow_html=True)
    content_type_filter = st.selectbox(
        "Content Type",
        ["All", "Movie", "TV Show"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-header" style="margin-top:1rem;">Year Range</div>', unsafe_allow_html=True)
    year_range_filter = st.slider(
        "Year Range",
        min_value=int(min(all_years)),
        max_value=int(max(all_years)),
        value=(int(min(all_years)), int(max(all_years))),
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-header" style="margin-top:1rem;">Age Rating</div>', unsafe_allow_html=True)
    rating_filter = st.multiselect(
        "Age Rating",
        options=all_ratings,
        default=[],
        placeholder="All ratings",
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-header" style="margin-top:1rem;">Country</div>', unsafe_allow_html=True)
    country_filter = st.multiselect(
        "Country",
        options=all_countries_flat,
        default=[],
        placeholder="All countries",
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-header" style="margin-top:1rem;">Genre</div>', unsafe_allow_html=True)
    genre_filter = st.multiselect(
        "Genre",
        options=all_genres_flat,
        default=[],
        placeholder="All genres",
        label_visibility="collapsed",
    )

    st.markdown("---")
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()

    st.markdown(
        '<div style="font-size:0.65rem; color:#444; text-align:center; margin-top:1rem;">'
        'Netflix Movies and TV Shows Dataset<br>via Kaggle</div>',
        unsafe_allow_html=True,
    )


df_filtered = apply_filters(
    df, content_type_filter, year_range_filter,
    country_filter, rating_filter, genre_filter
)

n_total = len(df_filtered)
n_movies = int((df_filtered["type"] == "Movie").sum())
n_tv = int((df_filtered["type"] == "TV Show").sum())
country_series = (
    df_filtered[df_filtered["country"] != "Unknown"]["country"]
    .str.split(",").explode().str.strip()
)
n_countries = int(country_series.nunique())
genre_series = df_filtered["listed_in"].str.split(",").explode().str.strip()
n_genres = int(genre_series.nunique())

st.markdown("""
<div style="padding: 0.5rem 0 1.5rem 0;">
    <span style="font-size:1.7rem; font-weight:800; color:#ffffff; letter-spacing:-0.02em;">
        Netflix Content Analytics
    </span>
    <span style="font-size:0.85rem; color:#808080; margin-left:1rem;">
        Interactive Dashboard
    </span>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(metric_card("Total Titles", fmt_number(n_total)), unsafe_allow_html=True)
with c2:
    st.markdown(metric_card("Movies", fmt_number(n_movies), f"{n_movies/n_total*100:.1f}% of library", "neutral"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_card("TV Shows", fmt_number(n_tv), f"{n_tv/n_total*100:.1f}% of library", "neutral"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_card("Countries", fmt_number(n_countries)), unsafe_allow_html=True)
with c5:
    st.markdown(metric_card("Genres", fmt_number(n_genres)), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab_overview, tab_geo, tab_time, tab_genre, tab_content, tab_people, tab_explore = st.tabs([
    "Overview",
    "Geography",
    "Time Series",
    "Genre",
    "Content Details",
    "People",
    "Data Explorer",
])


with tab_overview:
    col_left, col_right = st.columns([1, 1.8], gap="large")

    with col_left:
        st.markdown('<div class="section-title">Content Type Split</div>', unsafe_allow_html=True)
        type_counts = df_filtered["type"].value_counts()
        fig_donut = go.Figure(go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.65,
            marker=dict(colors=[NETFLIX_RED, "#4A90D9"], line=dict(color="#141414", width=2)),
            textinfo="label+percent",
            textfont=dict(size=13, color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>%{value:,} titles<br>%{percent}<extra></extra>",
        ))
        fig_donut.add_annotation(
            text=f"<b>{fmt_number(n_total)}</b><br><span style='font-size:11px;color:#808080'>Titles</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=22, color="#ffffff"),
        )
        fig_donut.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=True,
                                legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"))
        st.plotly_chart(fig_donut, use_container_width=True)

        movie_pct = n_movies / n_total * 100
        tv_pct = n_tv / n_total * 100
        st.markdown(
            f'<div class="insight-box"><strong>Key Insight:</strong> '
            f'Movies dominate at <strong>{movie_pct:.0f}%</strong> of the catalog versus '
            f'<strong>{tv_pct:.0f}%</strong> TV Shows. '
            f'Netflix positions itself as a strong movie platform while steadily growing its TV Show originals.</div>',
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown('<div class="section-title">Rating Distribution Overview</div>', unsafe_allow_html=True)
        rating_order = [
            "G", "PG", "PG-13", "R", "NC-17",
            "TV-Y", "TV-Y7", "TV-Y7-FV", "TV-G", "TV-PG", "TV-14", "TV-MA",
            "NR", "UR",
        ]
        rating_counts = df_filtered["rating"].value_counts()
        rating_counts = rating_counts.reindex(
            [r for r in rating_order if r in rating_counts.index]
        ).dropna()

        rating_by_type = (
            df_filtered.groupby(["rating", "type"]).size()
            .unstack(fill_value=0)
            .reindex([r for r in rating_order if r in rating_counts.index])
            .dropna()
        )

        fig_rating = go.Figure()
        colors_map = {"Movie": NETFLIX_RED, "TV Show": "#4A90D9"}
        for col in rating_by_type.columns:
            fig_rating.add_trace(go.Bar(
                name=col,
                x=rating_by_type.index,
                y=rating_by_type[col],
                marker_color=colors_map.get(col, "#7ED321"),
                hovertemplate=f"<b>{col}</b><br>Rating: %{{x}}<br>Titles: %{{y:,}}<extra></extra>",
            ))
        fig_rating.update_layout(
            **PLOTLY_LAYOUT, barmode="stack", height=320,
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_rating, use_container_width=True)

        top_rating = rating_counts.idxmax()
        top_pct = rating_counts.max() / rating_counts.sum() * 100
        st.markdown(
            f'<div class="insight-box"><strong>Key Insight:</strong> '
            f'<strong>{top_rating}</strong> is the dominant rating at <strong>{top_pct:.1f}%</strong> '
            f'of all content, confirming Netflix primary focus on mature adult audiences.</div>',
            unsafe_allow_html=True,
        )


with tab_geo:
    st.markdown('<div class="section-title">Geographic Content Production</div>', unsafe_allow_html=True)

    top_n_countries = st.slider("Show top N countries", 5, 30, 15, key="geo_slider")

    all_genres_geo = sorted(
        set(g.strip() for gl in df_filtered["listed_in"].dropna() for g in str(gl).split(",") if g.strip())
    )
    geo_genre = st.selectbox(
        "Filter by genre (optional)",
        ["All Genres"] + all_genres_geo,
        key="geo_genre",
    )

    df_geo = df_filtered.copy()
    if geo_genre != "All Genres":
        df_geo = df_geo[df_geo["listed_in"].str.contains(geo_genre, na=False)]

    country_counts_all = (
        df_geo[df_geo["country"] != "Unknown"]["country"]
        .str.split(",").explode().str.strip()
        .value_counts()
    )
    country_movie = (
        df_geo[(df_geo["country"] != "Unknown") & (df_geo["type"] == "Movie")]["country"]
        .str.split(",").explode().str.strip()
        .value_counts()
    )
    country_tv = (
        df_geo[(df_geo["country"] != "Unknown") & (df_geo["type"] == "TV Show")]["country"]
        .str.split(",").explode().str.strip()
        .value_counts()
    )

    top_c = country_counts_all.head(top_n_countries)
    top_m = country_movie.reindex(top_c.index).fillna(0)
    top_tv_s = country_tv.reindex(top_c.index).fillna(0)

    fig_countries = go.Figure()
    fig_countries.add_trace(go.Bar(
        name="Movie",
        y=top_c.index[::-1],
        x=top_m.values[::-1],
        orientation="h",
        marker_color=NETFLIX_RED,
        hovertemplate="<b>Movie</b><br>%{y}: %{x:,}<extra></extra>",
    ))
    fig_countries.add_trace(go.Bar(
        name="TV Show",
        y=top_c.index[::-1],
        x=top_tv_s.values[::-1],
        orientation="h",
        marker_color="#4A90D9",
        hovertemplate="<b>TV Show</b><br>%{y}: %{x:,}<extra></extra>",
    ))
    fig_countries.update_layout(
        **PLOTLY_LAYOUT,
        barmode="stack",
        height=max(400, top_n_countries * 28),
        title=f"Top {top_n_countries} Content-Producing Countries",
        xaxis_title="Number of Titles",
        legend=dict(orientation="h", y=1.05, x=0, xanchor="left"),
    )
    st.plotly_chart(fig_countries, use_container_width=True)

    col_g1, col_g2 = st.columns(2, gap="large")

    with col_g1:
        st.markdown('<div class="section-title">Country Share (%)</div>', unsafe_allow_html=True)
        top5 = country_counts_all.head(5)
        others = country_counts_all.iloc[5:].sum()
        labels = list(top5.index) + ["Others"]
        values = list(top5.values) + [others]
        fig_pie = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.4,
            marker=dict(colors=COLOR_SEQ[:6], line=dict(color="#141414", width=2)),
            textinfo="label+percent",
            textfont=dict(size=11, color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>%{value:,} titles (%{percent})<extra></extra>",
        ))
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_g2:
        st.markdown('<div class="section-title">US vs International</div>', unsafe_allow_html=True)
        df_geo_copy = df_geo.copy()
        df_geo_copy["is_us"] = df_geo_copy["country"].str.contains("United States", na=False)
        us_count = int(df_geo_copy["is_us"].sum())
        intl_count = int((~df_geo_copy["is_us"]).sum())
        fig_us = go.Figure(go.Bar(
            x=["United States", "International"],
            y=[us_count, intl_count],
            marker=dict(
                color=[NETFLIX_RED, "#4A90D9"],
                line=dict(color="#141414", width=1),
            ),
            text=[f"{us_count:,}", f"{intl_count:,}"],
            textposition="outside",
            textfont=dict(color="#ffffff"),
            hovertemplate="<b>%{x}</b><br>%{y:,} titles<extra></extra>",
        ))
        fig_us.update_layout(**PLOTLY_LAYOUT, height=320, yaxis_title="Number of Titles")
        st.plotly_chart(fig_us, use_container_width=True)

    top1 = country_counts_all.index[0]
    top1_pct = country_counts_all.iloc[0] / country_counts_all.sum() * 100
    st.markdown(
        f'<div class="insight-box"><strong>Key Insight:</strong> '
        f'<strong>{top1}</strong> leads production with <strong>{int(country_counts_all.iloc[0]):,}</strong> '
        f'titles (<strong>{top1_pct:.1f}%</strong> of geo-tagged content). '
        f'The top 5 countries account for over 70% of the catalog, '
        f'though Netflix has been actively diversifying toward international productions.</div>',
        unsafe_allow_html=True,
    )


with tab_time:
    st.markdown('<div class="section-title">Content Library Growth</div>', unsafe_allow_html=True)

    granularity = st.radio(
        "View by",
        ["Year", "Month"],
        horizontal=True,
        key="time_gran",
    )

    if granularity == "Year":
        yearly = df_filtered.groupby(["year_added", "type"]).size().unstack(fill_value=0)
        yearly["Total"] = yearly.sum(axis=1)
        yearly["YoY_Growth"] = yearly["Total"].pct_change() * 100

        fig_growth = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            subplot_titles=["Titles Added Per Year", "Year-over-Year Growth (%)"],
        )
        if "Movie" in yearly.columns:
            fig_growth.add_trace(
                go.Bar(name="Movie", x=yearly.index, y=yearly["Movie"],
                       marker_color=NETFLIX_RED,
                       hovertemplate="Movie: %{y:,}<extra></extra>"),
                row=1, col=1,
            )
        if "TV Show" in yearly.columns:
            fig_growth.add_trace(
                go.Bar(name="TV Show", x=yearly.index, y=yearly["TV Show"],
                       marker_color="#4A90D9",
                       hovertemplate="TV Show: %{y:,}<extra></extra>"),
                row=1, col=1,
            )
        fig_growth.add_trace(
            go.Scatter(name="Total", x=yearly.index, y=yearly["Total"],
                       mode="lines+markers+text",
                       line=dict(color="#F5A623", width=2),
                       marker=dict(size=7),
                       text=yearly["Total"].apply(lambda v: f"{v:,}"),
                       textposition="top center",
                       textfont=dict(size=9, color="#F5A623"),
                       hovertemplate="Total: %{y:,}<extra></extra>"),
            row=1, col=1,
        )
        growth_clean = yearly["YoY_Growth"].dropna()
        colors_bar = [NETFLIX_RED if v >= 0 else "#4A90D9" for v in growth_clean.values]
        fig_growth.add_trace(
            go.Bar(name="YoY Growth", x=growth_clean.index, y=growth_clean.values,
                   marker_color=colors_bar,
                   text=[f"{v:.0f}%" for v in growth_clean.values],
                   textposition="outside",
                   textfont=dict(size=9),
                   hovertemplate="YoY Growth: %{y:.1f}%<extra></extra>"),
            row=2, col=1,
        )
        fig_growth.update_layout(
            **PLOTLY_LAYOUT, height=600, barmode="stack",
            legend=dict(orientation="h", y=1.05, x=0, xanchor="left"),
        )
        for ann in fig_growth.layout.annotations:
            ann.font.color = "#b3b3b3"
        st.plotly_chart(fig_growth, use_container_width=True)

    else:
        MONTH_ORDER = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        monthly_total = (
            df_filtered.groupby("month_name").size()
            .reindex(MONTH_ORDER).fillna(0).astype(int)
        )
        fig_monthly = go.Figure(go.Bar(
            x=[m[:3] for m in MONTH_ORDER],
            y=monthly_total.values,
            marker=dict(
                color=monthly_total.values,
                colorscale=[[0, "#2a2a2a"], [1, NETFLIX_RED]],
                line=dict(color="#141414", width=1),
            ),
            text=monthly_total.values,
            textposition="outside",
            textfont=dict(color="#ffffff", size=10),
            hovertemplate="<b>%{x}</b><br>%{y:,} titles<extra></extra>",
        ))
        fig_monthly.update_layout(
            **PLOTLY_LAYOUT, height=380, yaxis_title="Number of Titles",
            title="Content Added by Month",
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown('<div class="section-title">Monthly Addition Heatmap</div>', unsafe_allow_html=True)
    MONTH_ORDER = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    pivot = (
        df_filtered.groupby(["year_added", "month_name"]).size()
        .unstack(fill_value=0)
        .reindex(columns=MONTH_ORDER)
    )
    fig_heat = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[m[:3] for m in MONTH_ORDER],
        y=pivot.index.tolist(),
        colorscale=[[0, "#1a1a1a"], [0.5, "#7B0000"], [1, NETFLIX_RED]],
        text=pivot.values,
        texttemplate="%{text}",
        textfont=dict(size=9, color="#ffffff"),
        hovertemplate="<b>%{y} - %{x}</b><br>%{z} titles<extra></extra>",
        colorbar=dict(
            title=dict(text="Titles", font=dict(color="#b3b3b3")),
            tickfont=dict(color="#b3b3b3"),
        ),
    ))
    fig_heat.update_layout(**PLOTLY_LAYOUT, height=380, yaxis=dict(gridcolor="#2a2a2a"))
    st.plotly_chart(fig_heat, use_container_width=True)

    if len(df_filtered) > 0:
        peak_year = df_filtered.groupby("year_added").size().idxmax()
        peak_count = df_filtered.groupby("year_added").size().max()
        st.markdown(
            f'<div class="insight-box"><strong>Key Insight:</strong> '
            f'Peak content addition was in <strong>{peak_year}</strong> with '
            f'<strong>{peak_count:,}</strong> titles added. '
            f'Netflix aggressive content expansion mirrors its global subscriber growth strategy, '
            f'with library size nearly doubling in peak years.</div>',
            unsafe_allow_html=True,
        )


with tab_genre:
    st.markdown('<div class="section-title">Genre Analysis</div>', unsafe_allow_html=True)

    col_genre_1, col_genre_2 = st.columns([2, 1], gap="large")

    with col_genre_1:
        top_n_genre = st.slider("Top N Genres", 5, 30, 15, key="genre_slider")
        genre_type_view = st.radio(
            "Split by type",
            ["All", "Movie only", "TV Show only"],
            horizontal=True,
            key="genre_type",
        )

        if genre_type_view == "Movie only":
            df_genre_view = df_filtered[df_filtered["type"] == "Movie"]
        elif genre_type_view == "TV Show only":
            df_genre_view = df_filtered[df_filtered["type"] == "TV Show"]
        else:
            df_genre_view = df_filtered

        genre_counts = (
            df_genre_view["listed_in"].str.split(",").explode().str.strip()
            .value_counts()
            .head(top_n_genre)
        )
        fig_genre_bar = go.Figure(go.Bar(
            y=genre_counts.index[::-1],
            x=genre_counts.values[::-1],
            orientation="h",
            marker=dict(
                color=genre_counts.values[::-1],
                colorscale=[[0, "#2a2a2a"], [1, NETFLIX_RED]],
                line=dict(color="#141414", width=1),
            ),
            text=genre_counts.values[::-1],
            textposition="outside",
            textfont=dict(color="#ffffff", size=10),
            hovertemplate="<b>%{y}</b><br>%{x:,} titles<extra></extra>",
        ))
        fig_genre_bar.update_layout(
            **PLOTLY_LAYOUT,
            height=max(400, top_n_genre * 28),
            xaxis_title="Number of Titles",
        )
        st.plotly_chart(fig_genre_bar, use_container_width=True)

    with col_genre_2:
        st.markdown('<div class="section-title">Genre Share</div>', unsafe_allow_html=True)
        top5_genres = (
            df_filtered["listed_in"].str.split(",").explode().str.strip()
            .value_counts()
        )
        top5_g = top5_genres.head(6)
        others_g = top5_genres.iloc[6:].sum()
        labels_g = list(top5_g.index) + ["Others"]
        vals_g = list(top5_g.values) + [others_g]
        fig_genre_pie = go.Figure(go.Pie(
            labels=labels_g, values=vals_g, hole=0.35,
            marker=dict(colors=COLOR_SEQ[:7], line=dict(color="#141414", width=2)),
            textinfo="percent",
            textfont=dict(size=11, color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>",
        ))
        fig_genre_pie.update_layout(
            **PLOTLY_LAYOUT, height=320,
            legend=dict(orientation="v", x=1, y=0.5, font=dict(size=10)),
        )
        st.plotly_chart(fig_genre_pie, use_container_width=True)

    st.markdown('<div class="section-title">Genre Trend Over Time</div>', unsafe_allow_html=True)

    top8 = (
        df_filtered["listed_in"].str.split(",").explode().str.strip()
        .value_counts().head(8).index.tolist()
    )
    selected_genres_trend = st.multiselect(
        "Select genres to display",
        options=top8,
        default=top8[:5],
        key="genre_trend_select",
    )

    if selected_genres_trend:
        rows = []
        for _, row in df_filtered.iterrows():
            for g in str(row["listed_in"]).split(","):
                g = g.strip()
                if g in selected_genres_trend:
                    rows.append({"genre": g, "year_added": row["year_added"]})

        if rows:
            gyt = pd.DataFrame(rows).groupby(["year_added", "genre"]).size().unstack(fill_value=0)
            fig_trend = go.Figure()
            for i, genre in enumerate(selected_genres_trend):
                if genre in gyt.columns:
                    fig_trend.add_trace(go.Scatter(
                        x=gyt.index, y=gyt[genre],
                        name=genre, mode="lines+markers",
                        line=dict(color=COLOR_SEQ[i % len(COLOR_SEQ)], width=2.5),
                        marker=dict(size=6),
                        hovertemplate=f"<b>{genre}</b><br>Year: %{{x}}<br>Titles: %{{y:,}}<extra></extra>",
                    ))
            fig_trend.update_layout(
                **PLOTLY_LAYOUT, height=380,
                yaxis_title="Number of Titles",
                xaxis_title="Year Added",
                legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
            )
            st.plotly_chart(fig_trend, use_container_width=True)


with tab_content:
    st.markdown('<div class="section-title">Movie Duration Analysis</div>', unsafe_allow_html=True)

    movies_f = df_filtered[(df_filtered["type"] == "Movie") & df_filtered["duration_clean"].notna()].copy()
    tv_f = df_filtered[(df_filtered["type"] == "TV Show") & df_filtered["duration_clean"].notna()].copy()

    col_d1, col_d2 = st.columns(2, gap="large")

    with col_d1:
        if not movies_f.empty:
            mean_dur = movies_f["duration_clean"].mean()
            median_dur = movies_f["duration_clean"].median()
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=movies_f["duration_clean"],
                nbinsx=40,
                marker=dict(color=NETFLIX_RED, line=dict(color="#141414", width=0.5)),
                opacity=0.85,
                name="Duration",
                hovertemplate="Duration: %{x} min<br>Count: %{y:,}<extra></extra>",
            ))
            fig_hist.add_vline(x=mean_dur, line_dash="dash", line_color="#F5A623",
                               annotation_text=f"Mean: {mean_dur:.0f}m",
                               annotation_font_color="#F5A623",
                               annotation_position="top right")
            fig_hist.add_vline(x=median_dur, line_dash="dash", line_color="#4A90D9",
                               annotation_text=f"Median: {median_dur:.0f}m",
                               annotation_font_color="#4A90D9",
                               annotation_position="top left")
            fig_hist.update_layout(
                **PLOTLY_LAYOUT, height=320,
                title="Movie Duration Distribution",
                xaxis_title="Duration (minutes)",
                yaxis_title="Number of Movies",
            )
            st.plotly_chart(fig_hist, use_container_width=True)

            col_s1, col_s2, col_s3 = st.columns(3)
            col_s1.metric("Mean", f"{mean_dur:.0f} min")
            col_s2.metric("Median", f"{median_dur:.0f} min")
            col_s3.metric("Std Dev", f"{movies_f['duration_clean'].std():.0f} min")
        else:
            st.info("No movie data available with current filters.")

    with col_d2:
        if not movies_f.empty:
            rating_order = ["G", "PG", "PG-13", "R", "NC-17", "NR", "UR"]
            movie_r = [r for r in rating_order if r in movies_f["rating"].unique()]
            movies_filtered_r = movies_f[movies_f["rating"].isin(movie_r)]

            if not movies_filtered_r.empty:
                fig_box = go.Figure()
                for i, r in enumerate(movie_r):
                    data_r = movies_filtered_r[movies_filtered_r["rating"] == r]["duration_clean"]
                    fig_box.add_trace(go.Box(
                        y=data_r, name=r,
                        marker_color=COLOR_SEQ[i % len(COLOR_SEQ)],
                        boxmean=True,
                        hovertemplate=f"<b>{r}</b><br>%{{y:.0f}} min<extra></extra>",
                    ))
                fig_box.update_layout(
                    **PLOTLY_LAYOUT, height=320,
                    title="Movie Duration by Age Rating",
                    yaxis_title="Duration (minutes)",
                    showlegend=False,
                )
                st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-title">TV Show Season Analysis</div>', unsafe_allow_html=True)

    col_tv1, col_tv2 = st.columns(2, gap="large")

    with col_tv1:
        if not tv_f.empty:
            season_counts = tv_f["duration_clean"].value_counts().sort_index()
            plot_s = season_counts[season_counts.index <= 15]
            fig_seasons = go.Figure(go.Bar(
                x=plot_s.index.astype(int),
                y=plot_s.values,
                marker=dict(
                    color=plot_s.values,
                    colorscale=[[0, "#2a2a2a"], [1, "#4A90D9"]],
                    line=dict(color="#141414", width=1),
                ),
                text=plot_s.values,
                textposition="outside",
                textfont=dict(color="#ffffff", size=9),
                hovertemplate="<b>%{x} Season(s)</b><br>%{y:,} TV Shows<extra></extra>",
            ))
            fig_seasons.update_layout(
                **PLOTLY_LAYOUT, height=320,
                title="TV Show Season Count Distribution",
                xaxis_title="Number of Seasons",
                yaxis_title="Number of TV Shows",
                xaxis=dict(tickmode="linear", dtick=1, gridcolor="#2a2a2a"),
            )
            st.plotly_chart(fig_seasons, use_container_width=True)
        else:
            st.info("No TV Show data available with current filters.")

    with col_tv2:
        if not tv_f.empty:
            cumulative = tv_f["duration_clean"].value_counts().sort_index()
            cum_pct = cumulative.cumsum() / cumulative.sum() * 100
            cum_plot = cum_pct[cum_pct.index <= 15]
            fig_cum = go.Figure()
            fig_cum.add_trace(go.Scatter(
                x=cum_plot.index.astype(int),
                y=cum_plot.values,
                mode="lines+markers",
                line=dict(color="#4A90D9", width=2.5),
                marker=dict(size=7, color="#4A90D9"),
                fill="tozeroy",
                fillcolor="rgba(74,144,217,0.1)",
                hovertemplate="<b>%{x} Season(s)</b><br>Cumulative: %{y:.1f}%<extra></extra>",
            ))
            fig_cum.add_hline(y=80, line_dash="dash", line_color=NETFLIX_RED,
                              annotation_text="80% threshold",
                              annotation_font_color=NETFLIX_RED)
            fig_cum.update_layout(
                **PLOTLY_LAYOUT, height=320,
                title="Cumulative % of TV Shows by Season Count",
                xaxis_title="Number of Seasons",
                yaxis_title="Cumulative %",
                yaxis=dict(range=[0, 105], gridcolor="#2a2a2a"),
                xaxis=dict(tickmode="linear", dtick=1, gridcolor="#2a2a2a"),
            )
            st.plotly_chart(fig_cum, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Release Lag: How Old is Netflix Content?</div>', unsafe_allow_html=True)

    lag_clean = df_filtered[(df_filtered["lag_years"] >= 0) & (df_filtered["lag_years"] <= 40)]

    if not lag_clean.empty:
        col_lag1, col_lag2 = st.columns(2, gap="large")

        with col_lag1:
            fig_lag = go.Figure()
            for ct, color in [("Movie", NETFLIX_RED), ("TV Show", "#4A90D9")]:
                subset = lag_clean[lag_clean["type"] == ct]["lag_years"]
                if not subset.empty:
                    fig_lag.add_trace(go.Histogram(
                        x=subset, name=ct, nbinsx=30, opacity=0.7,
                        marker_color=color,
                        hovertemplate=f"<b>{ct}</b><br>Lag: %{{x}} yrs<br>Count: %{{y:,}}<extra></extra>",
                    ))
            fig_lag.update_layout(
                **PLOTLY_LAYOUT, barmode="overlay", height=320,
                title="Years Between Original Release and Netflix Addition",
                xaxis_title="Years After Release",
                yaxis_title="Number of Titles",
                legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
            )
            st.plotly_chart(fig_lag, use_container_width=True)

        with col_lag2:
            fig_lag_box = go.Figure()
            for ct, color in [("Movie", NETFLIX_RED), ("TV Show", "#4A90D9")]:
                subset = lag_clean[lag_clean["type"] == ct]["lag_years"]
                if not subset.empty:
                    fig_lag_box.add_trace(go.Violin(
                        y=subset, name=ct, box_visible=True,
                        meanline_visible=True, fillcolor=color,
                        opacity=0.6, line_color="white",
                        hovertemplate=f"<b>{ct}</b><br>%{{y}} yrs<extra></extra>",
                    ))
            fig_lag_box.update_layout(
                **PLOTLY_LAYOUT, height=320,
                title="Release Lag Distribution by Content Type",
                yaxis_title="Years After Original Release",
                showlegend=False,
            )
            st.plotly_chart(fig_lag_box, use_container_width=True)

        same_year_count = int((lag_clean["lag_years"] == 0).sum())
        same_year_pct = same_year_count / len(lag_clean) * 100
        avg_lag = lag_clean["lag_years"].mean()
        st.markdown(
            f'<div class="insight-box"><strong>Key Insight:</strong> '
            f'<strong>{same_year_count:,}</strong> titles (<strong>{same_year_pct:.1f}%</strong>) '
            f'were added to Netflix in the same year as their original release. '
            f'The average lag is <strong>{avg_lag:.1f} years</strong>, indicating Netflix balances '
            f'fresh premieres with catalog acquisitions.</div>',
            unsafe_allow_html=True,
        )


with tab_people:
    st.markdown('<div class="section-title">Most Prolific Directors</div>', unsafe_allow_html=True)

    col_p1, col_p2 = st.columns([1, 1], gap="large")

    top_n_people = st.slider("Show top N", 5, 25, 15, key="people_slider")
    people_type = st.radio(
        "Content type",
        ["All", "Movie", "TV Show"],
        horizontal=True,
        key="people_type",
    )

    df_people = df_filtered.copy()
    if people_type != "All":
        df_people = df_people[df_people["type"] == people_type]

    with col_p1:
        dirs = (
            df_people[df_people["director"] != "Unknown"]["director"]
            .str.split(",").explode().str.strip()
            .value_counts().head(top_n_people)
        )
        if not dirs.empty:
            fig_dirs = go.Figure(go.Bar(
                y=dirs.index[::-1],
                x=dirs.values[::-1],
                orientation="h",
                marker=dict(
                    color=dirs.values[::-1],
                    colorscale=[[0, "#2a2a2a"], [1, "#7B2D8B"]],
                    line=dict(color="#141414", width=1),
                ),
                text=dirs.values[::-1],
                textposition="outside",
                textfont=dict(color="#ffffff", size=10),
                hovertemplate="<b>%{y}</b><br>%{x:,} titles<extra></extra>",
            ))
            fig_dirs.update_layout(
                **PLOTLY_LAYOUT,
                height=max(380, top_n_people * 28),
                title=f"Top {top_n_people} Directors",
                xaxis_title="Number of Titles",
            )
            st.plotly_chart(fig_dirs, use_container_width=True)
        else:
            st.info("No director data available.")

    with col_p2:
        cast_counts = (
            df_people[df_people["cast"] != "Unknown"]["cast"]
            .str.split(",").explode().str.strip()
            .value_counts().head(top_n_people)
        )
        if not cast_counts.empty:
            fig_cast = go.Figure(go.Bar(
                y=cast_counts.index[::-1],
                x=cast_counts.values[::-1],
                orientation="h",
                marker=dict(
                    color=cast_counts.values[::-1],
                    colorscale=[[0, "#2a2a2a"], [1, "#1ABC9C"]],
                    line=dict(color="#141414", width=1),
                ),
                text=cast_counts.values[::-1],
                textposition="outside",
                textfont=dict(color="#ffffff", size=10),
                hovertemplate="<b>%{y}</b><br>%{x:,} titles<extra></extra>",
            ))
            fig_cast.update_layout(
                **PLOTLY_LAYOUT,
                height=max(380, top_n_people * 28),
                title=f"Top {top_n_people} Cast Members",
                xaxis_title="Number of Titles",
            )
            st.plotly_chart(fig_cast, use_container_width=True)
        else:
            st.info("No cast data available.")

    if not dirs.empty and not cast_counts.empty:
        top_dir = dirs.index[0]
        top_cast_name = cast_counts.index[0]
        st.markdown(
            f'<div class="insight-box"><strong>Key Insight:</strong> '
            f'<strong>{top_dir}</strong> is the most prolific director with '
            f'<strong>{int(dirs.iloc[0])}</strong> titles, while '
            f'<strong>{top_cast_name}</strong> leads cast appearances with '
            f'<strong>{int(cast_counts.iloc[0])}</strong> titles. '
            f'Indian cinema dominates the upper ranks, reflecting Netflix strong presence in the Indian market.</div>',
            unsafe_allow_html=True,
        )


with tab_explore:
    st.markdown('<div class="section-title">Data Explorer</div>', unsafe_allow_html=True)

    col_ex1, col_ex2, col_ex3 = st.columns(3)
    with col_ex1:
        search_title = st.text_input("Search by title", placeholder="Enter title keyword...")
    with col_ex2:
        sort_col = st.selectbox(
            "Sort by",
            ["year_added", "release_year", "title", "type", "rating"],
            key="sort_col",
        )
    with col_ex3:
        sort_asc = st.radio("Order", ["Descending", "Ascending"], horizontal=True, key="sort_dir")

    df_explore = df_filtered.copy()
    if search_title:
        df_explore = df_explore[
            df_explore["title"].str.contains(search_title, case=False, na=False)
        ]

    df_explore = df_explore.sort_values(sort_col, ascending=(sort_asc == "Ascending"))

    display_cols = ["title", "type", "director", "cast", "country", "year_added",
                    "release_year", "rating", "duration", "listed_in"]
    available = [c for c in display_cols if c in df_explore.columns]

    st.markdown(
        f'<div style="font-size:0.8rem; color:#808080; margin-bottom:0.5rem;">'
        f'Showing <strong style="color:#ffffff;">{len(df_explore):,}</strong> of '
        f'<strong style="color:#ffffff;">{len(df_filtered):,}</strong> filtered records</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        df_explore[available].reset_index(drop=True),
        use_container_width=True,
        height=480,
    )

    col_dl1, col_dl2 = st.columns([1, 4])
    with col_dl1:
        csv_data = df_explore[available].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="netflix_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0;
            border-top: 1px solid #2a2a2a; margin-top: 2rem;
            font-size: 0.72rem; color: #444;">
    Netflix Content Analytics Dashboard &nbsp;|&nbsp;
    Built with Streamlit &amp; Plotly &nbsp;|&nbsp;
    Data: Netflix Movies and TV Shows (Kaggle)
</div>
""", unsafe_allow_html=True)
