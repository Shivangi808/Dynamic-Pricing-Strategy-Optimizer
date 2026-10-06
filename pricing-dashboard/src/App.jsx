import { useState } from "react";
import "./App.css";

const products = [
  {
    name: "Premium Basmati Rice",
    sku: "SKU-1024",
    current: 145,
    recommended: 159,
    demand: "High",
    inventory: 32,
    competitor: 158,
  },
  {
    name: "Organic Wheat Flour",
    sku: "SKU-2041",
    current: 68,
    recommended: 65,
    demand: "Medium",
    inventory: 124,
    competitor: 67,
  },
  {
    name: "Cold Pressed Oil",
    sku: "SKU-3102",
    current: 210,
    recommended: 225,
    demand: "High",
    inventory: 45,
    competitor: 221,
  },
  {
    name: "Green Tea Pack",
    sku: "SKU-4120",
    current: 180,
    recommended: 180,
    demand: "Low",
    inventory: 210,
    competitor: 182,
  },
  {
    name: "Organic Honey",
    sku: "SKU-5102",
    current: 320,
    recommended: 335,
    demand: "High",
    inventory: 28,
    competitor: 330,
  },
];

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [timeRange, setTimeRange] = useState("Last 30 days");
  const [showNotification, setShowNotification] = useState(false);

  const handleOptimize = (product) => {
    setShowNotification(
      `${product.name}: recommended price is ₹${product.recommended}`
    );

    setTimeout(() => {
      setShowNotification(false);
    }, 3000);
  };

  return (
    <div className="app">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-logo">P</div>

          <div>
            <h2>PricePilot</h2>
            <span>Pricing Intelligence</span>
          </div>
        </div>

        <div className="nav-section">
          <p className="nav-title">MAIN MENU</p>

          {[
            ["Dashboard", "▦"],
            ["Products", "□"],
            ["Pricing", "₹"],
            ["Analytics", "⌁"],
            ["Competitors", "◎"],
          ].map(([name, icon]) => (
            <button
              key={name}
              className={`nav-item ${
                activePage === name ? "active" : ""
              }`}
              onClick={() => setActivePage(name)}
            >
              <span>{icon}</span>
              {name}
            </button>
          ))}
        </div>

        <div className="nav-section second">
          <p className="nav-title">SYSTEM</p>

          <button
            className={`nav-item ${
              activePage === "Settings" ? "active" : ""
            }`}
            onClick={() => setActivePage("Settings")}
          >
            <span>⚙</span>
            Settings
          </button>
        </div>

        <div className="system-status">
          <div className="status-indicator"></div>

          <div>
            <strong>Pricing Engine</strong>
            <span>System operational</span>
          </div>
        </div>

      </aside>

      {/* MAIN */}
      <main className="main">

        {/* HEADER */}
        <header className="topbar">

          <div>
            <p className="breadcrumb">
              BUSINESS ANALYTICS / {activePage.toUpperCase()}
            </p>

            <h1>
              {activePage === "Dashboard"
                ? "Dynamic Pricing Dashboard"
                : activePage}
            </h1>

            <p className="page-description">
              Monitor demand, inventory and competitor pricing.
            </p>
          </div>

          <div className="top-actions">

            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="range-select"
            >
              <option>Last 7 days</option>
              <option>Last 30 days</option>
              <option>Last 90 days</option>
            </select>

            <button className="notification-button">♢</button>

            <div className="profile">
              SS
            </div>

          </div>

        </header>

        {/* KPI CARDS */}
        <section className="stats-grid">

          <div className="stat-card">
            <div className="stat-header">
              <span>Total Revenue</span>
              <div className="stat-icon green">₹</div>
            </div>

            <h2>₹2,84,620</h2>

            <div className="stat-growth">
              <span>↑ 12.8%</span>
              <small>vs previous period</small>
            </div>
          </div>


          <div className="stat-card">
            <div className="stat-header">
              <span>Units Sold</span>
              <div className="stat-icon blue">▦</div>
            </div>

            <h2>3,842</h2>

            <div className="stat-growth">
              <span>↑ 15.2%</span>
              <small>vs previous period</small>
            </div>
          </div>


          <div className="stat-card">
            <div className="stat-header">
              <span>Average Price</span>
              <div className="stat-icon purple">₹</div>
            </div>

            <h2>₹742</h2>

            <div className="stat-growth">
              <span>↑ 8.4%</span>
              <small>vs previous period</small>
            </div>
          </div>


          <div className="stat-card">
            <div className="stat-header">
              <span>Optimizations</span>
              <div className="stat-icon orange">✦</div>
            </div>

            <h2>247</h2>

            <div className="stat-growth">
              <span>↑ 21.5%</span>
              <small>this month</small>
            </div>
          </div>

        </section>


        {/* ANALYTICS AREA */}
        <section className="analytics-grid">

          {/* REVENUE CHART */}
          <div className="panel revenue-panel">

            <div className="panel-header">

              <div>
                <h3>Revenue Performance</h3>
                <p>Revenue generated over time</p>
              </div>

              <button className="outline-button">
                View report →
              </button>

            </div>

            <div className="chart-wrapper">

              <div className="chart-y-axis">
                <span>30K</span>
                <span>20K</span>
                <span>10K</span>
                <span>0</span>
              </div>

              <div className="chart">

                <div className="horizontal-line line-1"></div>
                <div className="horizontal-line line-2"></div>
                <div className="horizontal-line line-3"></div>
                <div className="horizontal-line line-4"></div>

                <svg
                  className="revenue-svg"
                  viewBox="0 0 700 240"
                  preserveAspectRatio="none"
                >
                  <defs>
                    <linearGradient
                      id="areaGradient"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop
                        offset="0%"
                        stopOpacity="0.18"
                      />

                      <stop
                        offset="100%"
                        stopOpacity="0"
                      />
                    </linearGradient>
                  </defs>

                  <polygon
                    points="
                    0,190
                    50,175
                    100,182
                    150,145
                    200,155
                    250,125
                    300,140
                    350,95
                    400,110
                    450,80
                    500,92
                    550,58
                    600,65
                    650,35
                    700,45
                    700,240
                    0,240
                    "
                    fill="url(#areaGradient)"
                  />

                  <polyline
                    points="
                    0,190
                    50,175
                    100,182
                    150,145
                    200,155
                    250,125
                    300,140
                    350,95
                    400,110
                    450,80
                    500,92
                    550,58
                    600,65
                    650,35
                    700,45
                    "
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>

                <div className="chart-x-axis">
                  <span>Sep 1</span>
                  <span>Sep 8</span>
                  <span>Sep 15</span>
                  <span>Sep 22</span>
                  <span>Sep 29</span>
                </div>

              </div>

            </div>

          </div>


          {/* AI RECOMMENDATION */}
          <div className="panel recommendation-panel">

            <div className="ai-title">

              <div className="ai-symbol">
                ✦
              </div>

              <div>
                <h3>AI Price Recommendation</h3>
                <p>Pricing engine insight</p>
              </div>

            </div>

            <div className="recommend-product">
              <span>TOP OPPORTUNITY</span>
              <h2>Premium Basmati Rice</h2>
              <p>SKU-1024</p>
            </div>

            <div className="price-row">

              <div>
                <span>Current price</span>
                <strong>₹145</strong>
              </div>

              <div className="price-arrow">
                →
              </div>

              <div>
                <span>Recommended</span>
                <strong className="recommended">
                  ₹159
                </strong>
              </div>

            </div>

            <div className="recommendation-reason">

              <div className="reason-label">
                WHY THIS PRICE?
              </div>

              <p>
                Demand has increased by <strong>18%</strong> while
                competitor prices are between <strong>₹158–₹162</strong>.
              </p>

            </div>

            <button
              className="primary-button"
              onClick={() =>
                handleOptimize(products[0])
              }
            >
              Apply Recommendation
            </button>

          </div>

        </section>


        {/* PRODUCT TABLE */}
        <section className="panel product-panel">

          <div className="panel-header">

            <div>
              <h3>Product Pricing Overview</h3>
              <p>
                AI-generated recommendations based on current market data
              </p>
            </div>

            <button className="outline-button">
              Export data ↓
            </button>

          </div>


          <div className="table-container">

            <table>

              <thead>
                <tr>
                  <th>PRODUCT</th>
                  <th>CURRENT PRICE</th>
                  <th>RECOMMENDED</th>
                  <th>DEMAND</th>
                  <th>INVENTORY</th>
                  <th>COMPETITOR</th>
                  <th></th>
                </tr>
              </thead>

              <tbody>

                {products.map((product) => (

                  <tr key={product.sku}>

                    <td>
                      <div className="product-cell">
                        <div className="product-avatar">
                          {product.name.charAt(0)}
                        </div>

                        <div>
                          <strong>{product.name}</strong>
                          <small>{product.sku}</small>
                        </div>
                      </div>
                    </td>

                    <td>
                      ₹{product.current}
                    </td>

                    <td>

                      <span
                        className={
                          product.recommended > product.current
                            ? "price-up"
                            : product.recommended < product.current
                            ? "price-down"
                            : "price-same"
                        }
                      >
                        ₹{product.recommended}

                        {product.recommended > product.current && " ↑"}

                        {product.recommended < product.current && " ↓"}
                      </span>

                    </td>

                    <td>
                      <span
                        className={`demand ${product.demand.toLowerCase()}`}
                      >
                        {product.demand}
                      </span>
                    </td>

                    <td>
                      {product.inventory} units
                    </td>

                    <td>
                      ₹{product.competitor}
                    </td>

                    <td>

                      <button
                        className="optimize-button"
                        onClick={() =>
                          handleOptimize(product)
                        }
                      >
                        Optimize
                      </button>

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        </section>


        {/* DATA PIPELINE */}
        <section className="pipeline">

          <div>
            <span className="pipeline-label">
              DATA PIPELINE
            </span>

            <h3>
              Pricing decisions powered by real-time data
            </h3>
          </div>

          <div className="pipeline-steps">

            <div>
              <span>01</span>
              <strong>Data Collection</strong>
              <small>Sales · Inventory · Competitors</small>
            </div>

            <b>→</b>

            <div>
              <span>02</span>
              <strong>Data Processing</strong>
              <small>Cleaning · Features · Trends</small>
            </div>

            <b>→</b>

            <div>
              <span>03</span>
              <strong>Price Optimization</strong>
              <small>ML model · Recommendation</small>
            </div>

          </div>

        </section>

      </main>


      {/* NOTIFICATION */}
      {showNotification && (
        <div className="toast">
          <span>✓</span>
          {showNotification}
        </div>
      )}

    </div>
  );
}

export default App;