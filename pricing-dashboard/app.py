import io

import streamlit as st
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Dynamic Pricing Strategy Optimizer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CREAM = "#F1E7D3"
ORANGE = "#E9835A"
MUSTARD = "#F2BE62"
TAUPE = "#A39A8B"
RED = "#EE5A6A"

# Large datasets: never push more than this many raw rows to the browser
MAX_TABLE_ROWS = 1000

REQUIRED_COLUMNS = [
    "date", "category", "region", "price", "discount", "units_sold",
    "units_ordered", "inventory_level", "demand", "competitor_pricing",
    "seasonality", "weather_condition"
]

PAGES = ["Dashboard", "Products", "Pricing", "Analytics", "Competitors"]


# ---------------------------------------------------
# DESIGN SYSTEM (CSS ONLY)
# ---------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #120D0C;
    --panel: #1A1412;
    --cream: #F1E7D3;
    --orange: #E9835A;
    --mustard: #F2BE62;
    --taupe: #A39A8B;
    --red: #EE5A6A;
    --line: rgba(241,231,211,0.16);
}

html, body, .stApp, .stMarkdown, button, input, select, textarea {
    font-family: "Space Grotesk", "Helvetica Neue", Arial, sans-serif !important;
}
.stApp { background: var(--bg); color: var(--cream); }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding: 1.6rem 2.6rem 4rem 2.6rem; max-width: 1360px; }

section[data-testid="stSidebar"],
div[data-testid="stSidebarCollapsedControl"],
div[data-testid="collapsedControl"] { display: none; }

/* ---------- Top bar ---------- */
.brand-tab {
    display: inline-block; background: var(--cream); color: var(--bg);
    font-weight: 700; font-size: 1.05rem; letter-spacing: -0.01em;
    padding: 0.55rem 1.4rem; border-radius: 0 0 22px 0;
    border-top-left-radius: 22px;
}
.topbar-space { height: 1.8rem; }

div[data-testid="stRadio"] div[role="radiogroup"] { gap: 8px; flex-wrap: wrap; }
div[data-testid="stRadio"] div[role="radiogroup"] > label {
    padding: 0.5rem 1.3rem; border-radius: 18px; cursor: pointer;
    background: var(--panel); border: 1px solid var(--line); color: var(--cream);
    transition: background .15s ease, color .15s ease;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child { display: none; }
div[data-testid="stRadio"] div[role="radiogroup"] > label p {
    margin: 0; font-size: 0.9rem; font-weight: 500; color: inherit;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:hover { background: var(--taupe); color: var(--bg); }
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    background: var(--red); color: var(--bg); border-color: var(--red);
}

/* ---------- Typography ---------- */
.page-title { font-size: 3rem; font-weight: 700; letter-spacing: -0.035em; line-height: 1.05; color: var(--cream); margin: 0; }
.page-sub { font-size: 1rem; color: var(--taupe); margin: 0.5rem 0 2rem 0; }
.section-title { font-size: 1.05rem; font-weight: 600; color: var(--cream); margin: 0; }
.section-sub { font-size: 0.82rem; color: var(--taupe); margin: 0.2rem 0 0.7rem 0; }
.muted { color: var(--taupe); font-size: 0.85rem; }

/* ---------- Panels ---------- */
.dashboard-card,
div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .card-marker),
div[data-testid="stVerticalBlock"]:has(> .element-container .card-marker) {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 28px;
    padding: 1.4rem 1.6rem 1.2rem 1.6rem;
    margin-bottom: 1rem;
}

/* colored instrument blocks */
.kpi-card {
    border-radius: 26px; padding: 1.1rem 1.4rem 1.3rem 1.4rem;
    margin-bottom: 1rem; color: var(--bg);
}
.c-cream { background: var(--cream); }
.c-mustard { background: var(--mustard); }
.c-orange { background: var(--orange); }
.c-taupe { background: var(--taupe); }
.c-red { background: var(--red); }

.metric-label { font-size: 0.9rem; font-weight: 500; color: var(--bg); opacity: 0.8; }
.metric-value {
    font-size: 2.3rem; font-weight: 700; letter-spacing: -0.035em;
    line-height: 1.05; margin-top: 1.1rem; color: var(--bg); word-break: break-word;
}

.info-card { border-radius: 20px; padding: 0.8rem 1.1rem 0.95rem 1.1rem; color: var(--bg); }
.info-value { font-size: 1.35rem; font-weight: 700; letter-spacing: -0.02em; margin-top: 0.6rem; color: var(--bg); }

.status-line { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: var(--cream); }
.status-dot { width: 9px; height: 9px; border-radius: 50%; background: var(--red); }
.status-dot.off { background: var(--taupe); }
.stat-row { display: flex; justify-content: space-between; padding: 0.5rem 0;
    border-bottom: 1px solid var(--line); font-size: 0.9rem; color: var(--taupe); }
.stat-row:last-child { border-bottom: none; }
.stat-row b { color: var(--cream); font-weight: 600; }

/* ---------- Inputs ---------- */
div[data-testid="stSelectbox"] label p, div[data-testid="stTextInput"] label p {
    font-size: 0.85rem; font-weight: 500; color: var(--taupe);
}
div[data-baseweb="select"] > div, div[data-baseweb="input"] {
    background: var(--panel) !important; border: 1px solid var(--line) !important;
    border-radius: 16px !important;
}
div[data-baseweb="input"] > div { background: transparent !important; }
div[data-baseweb="select"] > div:hover, div[data-baseweb="input"]:hover { border-color: var(--taupe) !important; }
div[data-baseweb="select"] > div:focus-within, div[data-baseweb="input"]:focus-within {
    border-color: var(--orange) !important; box-shadow: none !important;
}
div[data-baseweb="select"] *, input { color: var(--cream) !important; }
input::placeholder { color: #6B6358 !important; }
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] > div {
    background: var(--panel) !important; border: 1px solid var(--line); border-radius: 16px;
}
div[data-baseweb="popover"] li:hover { background: rgba(233,131,90,0.22) !important; }

/* uploader */
div[data-testid="stFileUploaderDropzone"] {
    background: var(--bg); border: 1px dashed var(--taupe); border-radius: 20px;
}
div[data-testid="stFileUploader"] button {
    background: var(--cream); color: var(--bg); border: none; border-radius: 999px; font-weight: 600;
}
div[data-testid="stFileUploader"] button:hover { background: var(--orange); color: var(--bg); }

/* ---------- Tables ---------- */
div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 16px; overflow: hidden; }
div[data-testid="stCaptionContainer"] p { color: var(--taupe); font-size: 0.8rem; }

@media (max-width: 900px) {
    .block-container { padding: 1rem 1rem 3rem 1rem; }
    .page-title { font-size: 2.1rem; }
    .metric-value { font-size: 1.7rem; }
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# UI HELPERS (PRESENTATION ONLY)
# ---------------------------------------------------

def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="page-title">{title}</div>
        <div class="page-sub">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )


def kpi_card(column, label, value, color="cream"):
    column.markdown(
        f"""
        <div class="kpi-card c-{color}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def info_card(column, label, value, color="cream"):
    column.markdown(
        f"""
        <div class="info-card c-{color}">
            <div class="metric-label">{label}</div>
            <div class="info-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def card(title, sub=None):
    """Styled container. Use as: with card("title", "sub"): ..."""
    box = st.container()
    sub_html = f'<div class="section-sub">{sub}</div>' if sub else ""
    box.markdown(
        f"""
        <div class="card-marker"></div>
        <div class="section-title">{title}</div>
        {sub_html}
        """,
        unsafe_allow_html=True
    )
    return box


def date_range_label(frame):
    if frame is None or len(frame) == 0:
        return None
    return f"{frame['date'].min():%d %b %Y} – {frame['date'].max():%d %b %Y}"


# ---------------------------------------------------
# LOAD, CLEAN AND VALIDATE DATA
# ---------------------------------------------------

def clean_data(df):

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Convert date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    return df


# ---------------------------------------------------
# MACHINE LEARNING PRICING ENGINE
# ---------------------------------------------------

ML_FEATURES = [
    "price",
    "discount",
    "inventory_level",
    "competitor_pricing",
    "category",
    "region",
    "seasonality",
    "weather_condition",
]

CATEGORICAL_FEATURES = [
    "category",
    "region",
    "seasonality",
    "weather_condition",
]


@st.cache_resource
def train_pricing_model(data):
    """Train and cache the Random Forest demand model."""
    model_data = data[ML_FEATURES + ["units_sold"]].dropna().copy()

    X = model_data[ML_FEATURES]
    y = model_data["units_sold"]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            )
        ],
        remainder="passthrough",
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    metrics = {
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": mean_squared_error(y_test, predictions) ** 0.5,
        "r2": r2_score(y_test, predictions),
    }

    return model, metrics


def build_price_scenarios(model, latest_row):
    """Predict demand and revenue at prices around the current price."""
    current_price = float(latest_row["price"])

    candidate_prices = [
        round(current_price * 0.90, 2),
        round(current_price * 0.95, 2),
        round(current_price, 2),
        round(current_price * 1.05, 2),
        round(current_price * 1.10, 2),
    ]

    scenarios = pd.DataFrame([
        {
            "price": price,
            "discount": latest_row["discount"],
            "inventory_level": latest_row["inventory_level"],
            "competitor_pricing": latest_row["competitor_pricing"],
            "category": latest_row["category"],
            "region": latest_row["region"],
            "seasonality": latest_row["seasonality"],
            "weather_condition": latest_row["weather_condition"],
        }
        for price in candidate_prices
    ])

    scenarios["predicted_units_sold"] = model.predict(
        scenarios[ML_FEATURES]
    )
    scenarios["predicted_units_sold"] = scenarios["predicted_units_sold"].clip(lower=0)
    scenarios["expected_revenue"] = (
        scenarios["price"] * scenarios["predicted_units_sold"]
    )

    return scenarios



def missing_columns(df):
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]


@st.cache_data
def load_uploaded(file_bytes):
    return clean_data(pd.read_csv(io.BytesIO(file_bytes)))


# ---------------------------------------------------
# SESSION STATE: ACTIVE DATASET
# ---------------------------------------------------
# IMPORTANT:
# There is NO default CSV.
# The application starts with dataset = None.
# Data appears only after the user uploads a CSV.

if "dataset" not in st.session_state:
    st.session_state["dataset"] = None
    st.session_state["dataset_name"] = None
    st.session_state["dataset_key"] = None
    st.session_state["upload_error"] = None


# ---------------------------------------------------
# TOP BAR / NAVIGATION
# ---------------------------------------------------

brand_col, nav_col = st.columns([1.3, 5])

with brand_col:
    st.markdown('<div class="brand-tab">PricePilot</div>', unsafe_allow_html=True)

with nav_col:
    page = st.radio(
        "Navigation",
        PAGES,
        horizontal=True,
        key="page",
        label_visibility="collapsed"
    )

st.markdown('<div class="topbar-space"></div>', unsafe_allow_html=True)


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

if page == "Dashboard":

    page_header("Dynamic pricing", "Pricing intelligence overview")

    # -------------------------------
    # DATASET UPLOAD
    # -------------------------------

    with card("Dataset", "Upload your sales data (CSV files only)"):

        up_col, status_col = st.columns([3, 2])

        with up_col:
            uploaded = st.file_uploader(
                "Upload CSV",
                type=["csv"],
                label_visibility="collapsed"
            )

            if uploaded is not None:
                file_key = f"{uploaded.name}:{uploaded.size}"

                if st.session_state["dataset_key"] != file_key:
                    st.session_state["dataset_key"] = file_key

                    try:
                        new_df = load_uploaded(uploaded.getvalue())
                        missing = missing_columns(new_df)

                        if missing:
                            st.session_state["upload_error"] = (
                                "Validation failed. Missing columns: "
                                + ", ".join(missing)
                            )
                        else:
                            st.session_state["dataset"] = new_df
                            st.session_state["dataset_name"] = uploaded.name
                            st.session_state["upload_error"] = None

                    except Exception as e:
                        st.session_state["upload_error"] = (
                            f"Could not read this file: {e}"
                        )

            if st.session_state["upload_error"]:
                st.error(st.session_state["upload_error"])

        active = st.session_state["dataset"]

        with status_col:
            if active is not None:
                st.markdown(
                    f"""
                    <div class="status-line"><span class="status-dot"></span>Data loaded</div>
                    <div class="muted" style="margin: 0.2rem 0 0.6rem 0;">{st.session_state["dataset_name"]}</div>
                    <div class="stat-row"><span>Rows</span><b>{len(active):,}</b></div>
                    <div class="stat-row"><span>Columns</span><b>{len(active.columns)}</b></div>
                    <div class="stat-row"><span>Validation</span><b>Passed</b></div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="status-line"><span class="status-dot off"></span>No data</div>
                    <div class="muted" style="margin-top: 0.4rem;">Upload a CSV to begin.</div>
                    """,
                    unsafe_allow_html=True
                )

    df = st.session_state["dataset"]

    if df is None:
        st.stop()


    # -------------------------------
    # FILTERS
    # -------------------------------

    col1, col2, _spacer = st.columns([1, 1, 2])

    with col1:
        categories = ["All"] + sorted(
            df["category"].dropna().unique().tolist()
        )

        selected_category = st.selectbox(
            "Category",
            categories
        )

    with col2:
        regions = ["All"] + sorted(
            df["region"].dropna().unique().tolist()
        )

        selected_region = st.selectbox(
            "Region",
            regions
        )

    filtered_df = df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["category"] == selected_category
        ]

    if selected_region != "All":
        filtered_df = filtered_df[
            filtered_df["region"] == selected_region
        ]


    # -------------------------------
    # CALCULATE REVENUE
    # -------------------------------

    filtered_df["revenue"] = (
        filtered_df["price"] *
        filtered_df["units_sold"]
    )

    total_revenue = filtered_df["revenue"].sum()

    units_sold = filtered_df["units_sold"].sum()

    average_price = filtered_df["price"].mean()

    total_inventory = filtered_df["inventory_level"].sum()


    # -------------------------------
    # KPI CARDS
    # -------------------------------

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    kpi_card(col1, "total revenue", f"₹{total_revenue:,.0f}", "cream")
    kpi_card(col2, "units sold", f"{units_sold:,.0f}", "mustard")
    kpi_card(col3, "average price", f"₹{average_price:,.2f}", "orange")
    kpi_card(col4, "inventory", f"{total_inventory:,.0f}", "taupe")


    # -------------------------------
    # CHARTS
    # -------------------------------

    revenue_by_date = (
        filtered_df
        .groupby("date")["revenue"]
        .sum()
        .sort_index()
    )

    sales_by_date = (
        filtered_df
        .groupby("date")["units_sold"]
        .sum()
        .sort_index()
    )

    pricing_overview = pd.DataFrame(
        {
            "Price": [
                filtered_df["price"].mean(),
                filtered_df["competitor_pricing"].mean()
            ]
        },
        index=[
            "Our Price",
            "Competitor Price"
        ]
    )

    left, right = st.columns([3, 2])

    with left:
        with card("Revenue trend", date_range_label(filtered_df) or "Revenue over time"):
            st.line_chart(revenue_by_date, color=ORANGE, height=260)

    with right:
        with card("Pricing overview", "Average our price vs competitor price"):
            st.bar_chart(pricing_overview, color=MUSTARD, height=260)

    with card("Units sold", date_range_label(filtered_df) or "Units sold over time"):
        st.line_chart(sales_by_date, color=CREAM, height=220)


# ---------------------------------------------------
# All other pages use the active (uploaded) dataset
# ---------------------------------------------------

else:

    df = st.session_state["dataset"]

    if df is None:
        with card("No dataset loaded", "Go to Dashboard and upload a CSV file to use this page."):
            st.write("")
        st.stop()


# ---------------------------------------------------
# PRODUCTS
# ---------------------------------------------------

if page == "Products":

    page_header("Products", "Product-level information")

    search_col, _spacer = st.columns([1, 2])

    with search_col:
        search = st.text_input(
            "Search products",
            placeholder="Search category"
        )

    products_df = df.copy()

    if search:

        products_df = products_df[
            products_df["category"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    with card("Product records", "Sales, pricing and inventory"):
        st.dataframe(
            products_df[
                [
                    "date",
                    "category",
                    "region",
                    "price",
                    "discount",
                    "units_sold",
                    "units_ordered",
                    "inventory_level",
                    "demand"
                ]
            ].head(MAX_TABLE_ROWS),
            use_container_width=True
        )
        st.caption(
            f"Showing {min(len(products_df), MAX_TABLE_ROWS):,} of "
            f"{len(products_df):,} matching rows"
        )

    inventory_by_category = (
        products_df
        .groupby("category")["inventory_level"]
        .sum()
        .sort_values(ascending=False)
    )

    with card("Inventory by category", "Total inventory level per category"):
        st.bar_chart(inventory_by_category, color=ORANGE, height=260)


# ---------------------------------------------------
# PRICING
# ---------------------------------------------------

elif page == "Pricing":

    page_header("Pricing", "ML-powered price recommendation")

    sel_col, _spacer = st.columns([1, 2])

    with sel_col:
        selected_category = st.selectbox(
            "Select product category",
            sorted(df["category"].dropna().unique())
        )

    st.write("")

    category_df = df[df["category"] == selected_category]

    if len(category_df) > 0:
        latest_row = (
            category_df
            .sort_values("date")
            .iloc[-1]
        )

        # Train the same Random Forest approach used in dynamic.ipynb.
        try:
            model, metrics = train_pricing_model(df)
            scenarios = build_price_scenarios(model, latest_row)
            best_row = scenarios.loc[
                scenarios["expected_revenue"].idxmax()
            ]

            recommended_price = float(best_row["price"])
            predicted_demand = float(best_row["predicted_units_sold"])
            expected_revenue = float(best_row["expected_revenue"])

            current_price = float(latest_row["price"])
            price_change = recommended_price - current_price
            price_change_pct = (
                price_change / current_price * 100
                if current_price != 0 else 0
            )

            # -------------------------------
            # ML PRICING KPIs
            # -------------------------------
            col1, col2, col3, col4 = st.columns(4)

            kpi_card(col1, "current price", f"₹{current_price:,.2f}", "cream")
            kpi_card(col2, "recommended price", f"₹{recommended_price:,.2f}", "mustard")
            kpi_card(col3, "predicted units", f"{predicted_demand:,.0f}", "orange")
            kpi_card(col4, "expected revenue", f"₹{expected_revenue:,.0f}", "taupe")

            # -------------------------------
            # RECOMMENDATION
            # -------------------------------
            with card(
                "ML price recommendation",
                "Random Forest demand prediction + expected revenue optimization"
            ):
                if price_change > 0:
                    st.write(
                        f"The model suggests **increasing the price by ₹{price_change:,.2f} "
                        f"({price_change_pct:+.1f}%)** for this category."
                    )
                elif price_change < 0:
                    st.write(
                        f"The model suggests **decreasing the price by ₹{abs(price_change):,.2f} "
                        f"({price_change_pct:+.1f}%)** for this category."
                    )
                else:
                    st.write("The model suggests keeping the current price.")

                st.caption(
                    "The recommendation tests five prices from -10% to +10% around the latest price "
                    "and selects the one with the highest predicted revenue. It is a prototype "
                    "decision-support output, not a guaranteed future outcome."
                )

            # -------------------------------
            # PRICE SCENARIOS
            # -------------------------------
            with card(
                "Candidate price analysis",
                "Predicted demand and revenue at different prices"
            ):
                chart_data = scenarios.set_index("price")[
                    ["predicted_units_sold", "expected_revenue"]
                ]
                st.line_chart(chart_data, height=280)

            display_scenarios = scenarios.rename(
                columns={
                    "price": "Candidate Price",
                    "predicted_units_sold": "Predicted Units Sold",
                    "expected_revenue": "Expected Revenue",
                }
            )[[
                "Candidate Price",
                "Predicted Units Sold",
                "Expected Revenue",
            ]].copy()

            with card(
                "Pricing scenarios",
                "ML prediction for each candidate price"
            ):
                st.dataframe(
                    display_scenarios.style.format({
                        "Candidate Price": "₹{:,.2f}",
                        "Predicted Units Sold": "{:,.1f}",
                        "Expected Revenue": "₹{:,.2f}",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )

            # -------------------------------
            # MODEL PERFORMANCE
            # -------------------------------
            with card(
                "Model performance",
                "Evaluation on the held-out 20% test set"
            ):
                m1, m2, m3 = st.columns(3)
                info_card(m1, "MAE", f"{metrics['mae']:.2f}", "cream")
                info_card(m2, "RMSE", f"{metrics['rmse']:.2f}", "mustard")
                info_card(m3, "R²", f"{metrics['r2']:.3f}", "orange")

        except Exception as e:
            st.error(f"ML pricing engine could not run: {e}")

        # -------------------------------
        # CURRENT MARKET SIGNALS
        # -------------------------------
        with card("Pricing signals", "Conditions behind the latest record"):
            s1, s2, s3, s4 = st.columns(4)

            info_card(s1, "competitor price", f"₹{latest_row['competitor_pricing']:,.2f}", "cream")
            info_card(s2, "inventory", f"{latest_row['inventory_level']:,.0f}", "mustard")
            info_card(s3, "discount", f"{latest_row['discount']}%", "orange")
            info_card(s4, "demand", f"{latest_row['demand']}", "taupe")


# ---------------------------------------------------
# ANALYTICS
# ---------------------------------------------------

elif page == "Analytics":

    page_header("Analytics", "Business performance &amp; trends")


    # Work on a copy so the active dataset keeps its original columns
    df = df.copy()

    # Revenue

    df["revenue"] = (
        df["price"] *
        df["units_sold"]
    )


    # -------------------------------
    # KPI
    # -------------------------------

    col1, col2, col3 = st.columns(3)


    total_revenue = df["revenue"].sum()

    total_sales = df["units_sold"].sum()

    avg_discount = df["discount"].mean()


    kpi_card(col1, "total revenue", f"₹{total_revenue:,.0f}", "cream")
    kpi_card(col2, "total units sold", f"{total_sales:,.0f}", "mustard")
    kpi_card(col3, "average discount", f"{avg_discount:.2f}%", "orange")


    # -------------------------------
    # TRENDS
    # -------------------------------

    revenue_trend = (
        df.groupby("date")["revenue"]
        .sum()
        .sort_index()
    )

    demand_trend = (
        df.groupby("date")["units_sold"]
        .sum()
        .sort_index()
    )

    category_sales = (
        df.groupby("category")["units_sold"]
        .sum()
        .sort_values(ascending=False)
    )

    left, right = st.columns(2)

    with left:
        with card("Revenue trend", "Revenue over time"):
            st.line_chart(revenue_trend, color=ORANGE, height=240)

    with right:
        with card("Demand trend", "Units sold over time"):
            st.line_chart(demand_trend, color=MUSTARD, height=240)

    with card("Category performance", "Units sold per category"):
        st.bar_chart(category_sales, color=ORANGE, height=260)


# ---------------------------------------------------
# COMPETITORS
# ---------------------------------------------------

elif page == "Competitors":

    page_header("Competitors", "Market price comparison")


    competitor_df = df.copy()


    # Calculate price difference

    competitor_df["price_difference"] = (
        competitor_df["price"]
        -
        competitor_df["competitor_pricing"]
    )


    # -------------------------------
    # SUMMARY CARDS (from existing averages)
    # -------------------------------

    our_avg = df["price"].mean()
    comp_avg = df["competitor_pricing"].mean()
    avg_diff = our_avg - comp_avg

    col1, col2, col3 = st.columns(3)

    kpi_card(col1, "our average price", f"₹{our_avg:,.2f}", "cream")
    kpi_card(col2, "competitor average price", f"₹{comp_avg:,.2f}", "taupe")
    kpi_card(col3, "price gap", f"₹{avg_diff:,.2f}", "red" if avg_diff < 0 else "mustard")


    # -------------------------------
    # CATEGORY PRICE COMPARISON (summary table, not raw rows)
    # -------------------------------

    category_summary = (
        df.groupby("category")[["price", "competitor_pricing"]]
        .mean()
    )
    category_summary["price_difference"] = (
        category_summary["price"]
        -
        category_summary["competitor_pricing"]
    )
    category_summary = category_summary.round(2)

    with card("Category price comparison", "Average price per category"):
        st.dataframe(
            category_summary,
            use_container_width=True
        )


    # -------------------------------
    # AVERAGE PRICE COMPARISON
    # -------------------------------

    price_comparison = pd.DataFrame(
        {
            "Price": [
                df["price"].mean(),
                df["competitor_pricing"].mean()
            ]
        },
        index=[
            "Our Average Price",
            "Competitor Average Price"
        ]
    )


    # -------------------------------
    # PRICE GAP BY CATEGORY
    # -------------------------------

    category_gap = (
        df.groupby("category")
        .apply(
            lambda x:
            x["price"].mean()
            -
            x["competitor_pricing"].mean(),
            include_groups=False
        )
        .sort_values()
    )

    left, right = st.columns(2)

    with left:
        with card("Average price comparison", "Our average vs competitor average"):
            st.bar_chart(price_comparison, color=MUSTARD, height=240)

    with right:
        with card("Price gap by category", "Average price difference per category"):
            st.bar_chart(category_gap, color=ORANGE, height=240)