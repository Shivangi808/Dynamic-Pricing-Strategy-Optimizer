# 📊 Dynamic Pricing Strategy Optimizer

An interactive **dynamic pricing and sales analytics dashboard** built with Python and Streamlit. The application helps businesses analyze sales performance, understand demand patterns, compare competitor pricing, and make data-driven pricing decisions.

## 🚀 Live Demo

**[Try the Live Dashboard](https://dynamic-pricing-strategy-optimizer-zdkugrumeu4fqwhzejplc4.streamlit.app/)**

---

## 🎯 Problem Statement

Traditional pricing strategies often rely on fixed prices and manual decisions. However, factors such as:

- Customer demand
- Product inventory
- Historical sales
- Competitor prices
- Product performance

can change continuously.

This project provides an interactive dashboard that analyzes these factors and helps identify pricing opportunities using data-driven insights.

---

## ✨ Features

### 📈 Sales Analytics
- Analyze historical sales data
- Track revenue and sales performance
- Identify demand patterns
- Visualize important business metrics

### 🏷️ Dynamic Pricing
- Analyze pricing against demand
- Compare current prices with market conditions
- Identify potential pricing opportunities
- Support data-driven pricing decisions

### 🛒 Product Analysis
- Product-level performance analysis
- Identify high-performing and low-performing products
- Compare product sales and pricing

### 🏪 Competitor Analysis
- Compare competitor prices
- Identify pricing gaps
- Analyze market positioning

### 📊 Interactive Dashboard
- Interactive Plotly visualizations
- Streamlit-based interface
- Dataset upload functionality
- Real-time analysis after uploading data

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Interactive dashboard |
| Pandas | Data manipulation |
| NumPy | Numerical computation |
| Scikit-learn | Data analysis / ML utilities |
| Plotly | Interactive visualizations |
| BeautifulSoup | Web scraping |

---

## 🔄 Workflow

```text
Sales / Market Data
        ↓
Data Upload
        ↓
Data Processing
        ↓
Sales & Demand Analysis
        ↓
Product Analysis
        ↓
Competitor Price Analysis
        ↓
Pricing Insights
        ↓
Data-Driven Pricing Decisions
```

---

## 📸 Dashboard

### Dashboard

![Dashboard](screenshots/Dashboard.png)

### Analytics

![Analytics](screenshots/Analytics.png)

### Product Analysis

![Products](screenshots/Products.png)

### Competitor Analysis

![Competitors](screenshots/Competitors.png)

---

## 📁 Project Structure

```text
Dynamic-Pricing-Strategy-Optimizer/
│
├── app.py
├── dynamic.ipynb
├── sales_data.csv
├── requirements.txt
├── README.md
│
└── screenshots/
    ├── Dashboard.png
    ├── Analytics.png
    ├── Products.png
    └── Competitors.png
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Shivangi808/Dynamic-Pricing-Strategy-Optimizer.git
```

### 2. Navigate to the project

```bash
cd Dynamic-Pricing-Strategy-Optimizer
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The dashboard will open locally at:

```text
http://localhost:8501
```

---

## ☁️ Deployment

This application can be deployed using **Streamlit Community Cloud**.

### Deployment Steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select this repository.
5. Select the `main` branch.
6. Set the main file as:

```text
app.py
```

7. Click **Deploy**.

After deployment, add the generated URL to the **Live Demo** section above.

---

## 🔮 Future Improvements

- Automated competitor price collection
- Real-time market data integration
- Demand forecasting
- ML-based price recommendation
- Inventory-aware pricing
- Automated pricing alerts
- Cloud database integration
- Authentication and business-specific dashboards

---

## 👩‍💻 Author

**Shivangi Singh**

B.Tech CSE — Artificial Intelligence & Machine Learning

Interested in **AI/ML, software engineering, data-driven systems, and intelligent applications**.

---

## ⭐ Project Goal

The goal of this project is to demonstrate how **data analytics, machine learning techniques, and interactive dashboards** can be combined to solve practical business pricing problems.
