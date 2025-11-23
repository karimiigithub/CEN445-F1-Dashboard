# 🏎️ Formula 1 Analysis & Prediction Dashboard

**Course:** CEN445 - Introduction to Data Visualization  
**Semester:** Fall 2025-2026  
**Tools:** Python, Streamlit, Plotly, Scikit-learn

## 📌 Project Overview
This project is an interactive data visualization dashboard developed to analyze historical Formula 1 World Championship data. The application allows users to explore driver performances, team statistics, race locations, and correlation between qualifying and finishing positions.

Additionally, a **K-Means Clustering (Machine Learning)** algorithm is integrated to group drivers based on their performance metrics, providing deeper insights into driver tiers.

## 📂 Dataset Details
The dataset used in this project is the **Formula 1 World Championship History 1950-2024**, obtained from Kaggle. It provides comprehensive details about races, drivers, constructors, and circuit information.

* **Source Link:** [Formula 1 World Championship History 1950-2024 (Kaggle)](https://www.kaggle.com/datasets/muhammadehsan02/formula-1-world-championship-history-1950-2024)
* **Data Size:** The dataset contains extensive historical records exceeding the assignment requirement of 2,000 rows.
* **Files Used:**
    * `Race_Results.csv`: Main transactional data (positions, points).
    * `Driver_Details.csv`: Driver names, nationalities.
    * `Team_Details.csv`: Constructor names, nationalities.
    * `Race_Schedule.csv`: Season years, rounds, dates.
    * `Track_Information.csv`: Circuit coordinates (Latitude/Longitude) for geospatial analysis.

## 📊 Visualizations & Features
The dashboard includes **9 distinct visualization techniques**, including 6 advanced types:

1.  **Geospatial Scatter Map** (Advanced): Interactive map showing global race locations.
2.  **Treemap** (Advanced): Hierarchical view of total points distributed among teams.
3.  **Sunburst Chart** (Advanced): Multi-level hierarchy (Nationality -> Team -> Driver).
4.  **K-Means Clustering Scatter** (Advanced/ML): AI-based grouping of drivers (Grid vs. Points).
5.  **Box Plot** (Advanced): Distribution of finishing positions per cluster.
6.  **Interactive Scatter Plot**: Correlation between Grid Position and Finishing Position.
7.  **Bar Chart**: Top 10 Drivers ranking.
8.  **Line Chart**: Cumulative championship points progression over the season.
9.  **Pie Chart**: Distribution of race wins among teams.

## 🛠️ Installation & Setup Instructions
To run this dashboard locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <https://github.com/karimiigithub/CEN445-F1-Dashboard>
    cd F1_Dashboard
    ```

2.  **Install required libraries:**
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```

## 👥 Team Members & Contributions
Per the assignment requirements, the workload and visualization design were distributed as follows:

### **Yiğit Çetin - 2021556020 - **
* **Role:** Project Lead, Data Engineering, Machine Learning Integration.
* **Tasks:**
    * Data Cleaning & Merging Strategy (Pandas Preprocessing).
    * Implementing **K-Means Clustering** algorithm.
    * **Visualizations Created:**
        1.  ML Scatter Plot (Clusters).
        2.  Box Plot (Cluster Distributions).
        3.  Interactive Scatter Plot (Grid vs. Finish).

### **Ozan Dural - 2021556027 - **
* **Role:** Geospatial Analysis & Driver Performance Analytics.
* **Tasks:**
    * Handling geospatial data (Latitude/Longitude) processing.
    * Designing the "Driver Analysis" tab layout.
    * **Visualizations Created:**
        1.  Geospatial Map (Global Race Locations).
        2.  Bar Chart (Top 10 Drivers).
        3.  Line Chart (Championship Progression).

### **Seymen Bugay - 2021556013 - **
* **Role:** Team Analytics & UI/UX Design.
* **Tasks:**
    * Implementing Sidebar Filters (Year & Team Selection).
    * Designing the "Team Analysis" tab and overall color theme.
    * **Visualizations Created:**
        1.  Treemap (Team Points Distribution).
        2.  Sunburst Chart (Team/Driver Hierarchy).
        3.  Pie Chart (Race Wins).

---
*This project is submitted for the partial fulfillment of the CEN445 course requirements.*


