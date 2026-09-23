import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Factory Reallocation & Shipping Optimization",
    page_icon="🏭",
    layout="wide"
)


# ============================================================
# PROJECT TITLE
# ============================================================

st.title("🏭 Factory Reallocation & Shipping Optimization")

st.markdown(
    """
    ### Supply Chain Analytics & Decision Support Dashboard

    Analysis of factory profiles, shipping performance, lead time,
    product movement, profitability, scenario analysis and
    factory reallocation opportunities.
    """
)

st.divider()


# ============================================================
# FILE NAME
# ============================================================

FILE_NAME = "Nassau candy distributor.xlsx"


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(FILE_NAME):

    st.error(
        "Excel file not found.\n\n"
        "Please keep 'Nassau candy distributor.xlsx' "
        "in the same folder as app.py."
    )

    st.stop()


# ============================================================
# LOAD EXCEL SHEET
# ============================================================

@st.cache_data
def load_sheet(sheet_name):

    """
    Load a worksheet and remove title/empty rows.
    The workbook has different header positions for different
    sheets, so each sheet is handled explicitly.
    """

    header_rows = {
        "Raw_Data": 2,
        "Data_Cleaning": 0,
        "Derived_Data": 2,
        "EDA": 0,
        "Model_Analysis": 0,
        "Clustering": 2,
        "Scenario_Analysis": 5,
        "Recommendations": 5,
        "KPI_Dashboard": 3,
        "Factory_Coordinates": 3,
        "Product_Factory_Correlation": 3,
    }

    header = header_rows.get(sheet_name, 0)

    data = pd.read_excel(
        FILE_NAME,
        sheet_name=sheet_name,
        header=header
    )

    # Remove completely empty rows
    data = data.dropna(
        axis=0,
        how="all"
    )

    # Remove completely empty columns
    data = data.dropna(
        axis=1,
        how="all"
    )

    # Clean column names
    data.columns = [
        str(column).strip()
        for column in data.columns
    ]

    return data


# ============================================================
# GET WORKBOOK SHEETS
# ============================================================

try:

    workbook = pd.ExcelFile(FILE_NAME)

    sheet_names = workbook.sheet_names

except Exception as error:

    st.error(
        f"Unable to open Excel file.\n\n{error}"
    )

    st.stop()


# ============================================================
# LOAD MAIN DATA
# ============================================================

try:

    raw_data = load_sheet("Raw_Data")

except Exception as error:

    st.error(
        f"Unable to load Raw_Data.\n\n{error}"
    )

    st.stop()


try:

    derived_data = load_sheet("Derived_Data")

except Exception:

    derived_data = raw_data.copy()


# ============================================================
# HELPER FUNCTION
# ============================================================

def make_numeric(dataframe, column):

    if column in dataframe.columns:

        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )


# ============================================================
# NUMERIC COLUMNS
# ============================================================

for column in [
    "Sales",
    "Units",
    "Gross Profit",
    "Cost",
    "Lead Time Days",
    "Profit Margin %",
    "Cost % of Sales"
]:

    make_numeric(
        derived_data,
        column
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏭 Project Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "Executive Dashboard",
        "Data Explorer",
        "Shipping Optimization",
        "Factory Reallocation",
        "Scenario Analysis",
        "Recommendations",
        "K-Means Clustering",
        "Correlation Analysis",
        "Workbook Sheets"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("📁 Project Information")

st.sidebar.write(
    "**Dataset:** Nassau Candy Distributor"
)

st.sidebar.write(
    f"**Records:** {len(raw_data):,}"
)

st.sidebar.write(
    f"**Workbook Sheets:** {len(sheet_names)}"
)


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.header("📊 Executive Dashboard")

    st.write(
        "Management-level overview of sales, profit, shipping "
        "performance and operational efficiency."
    )

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_sales = derived_data["Sales"].sum()

    total_profit = derived_data["Gross Profit"].sum()

    total_cost = derived_data["Cost"].sum()

    total_units = derived_data["Units"].sum()

    average_lead_time = derived_data[
        "Lead Time Days"
    ].mean()

    average_margin = derived_data[
        "Profit Margin %"
    ].mean()


    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "💰 Total Sales",
            f"${total_sales:,.2f}"
        )

    with c2:

        st.metric(
            "📈 Total Gross Profit",
            f"${total_profit:,.2f}"
        )

    with c3:

        st.metric(
            "💵 Total Cost",
            f"${total_cost:,.2f}"
        )


    c4, c5, c6 = st.columns(3)

    with c4:

        st.metric(
            "📦 Total Units",
            f"{total_units:,.0f}"
        )

    with c5:

        st.metric(
            "🚚 Average Lead Time",
            f"{average_lead_time:,.2f} days"
        )

    with c6:

        st.metric(
            "📊 Average Profit Margin",
            f"{average_margin:,.2f}%"
        )


    st.divider()


    # --------------------------------------------------------
    # FINANCIAL CHART
    # --------------------------------------------------------

    st.subheader("💰 Financial Overview")

    financial_data = pd.DataFrame(
        {
            "Metric": [
                "Sales",
                "Gross Profit",
                "Cost"
            ],
            "Amount": [
                total_sales,
                total_profit,
                total_cost
            ]
        }
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(
        financial_data["Metric"],
        financial_data["Amount"]
    )

    ax.set_title(
        "Sales, Gross Profit and Cost"
    )

    ax.set_ylabel(
        "Amount ($)"
    )

    st.pyplot(fig)


    # --------------------------------------------------------
    # REGION SUMMARY
    # --------------------------------------------------------

    st.subheader("🌎 Regional Performance")

    region_summary = (
        derived_data
        .groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Gross Profit", "sum"),
            Units=("Units", "sum"),
            Average_Lead_Time=("Lead Time Days", "mean")
        )
        .reset_index()
    )

    region_summary["Average_Lead_Time"] = (
        region_summary["Average_Lead_Time"]
        .round(2)
    )

    st.dataframe(
        region_summary,
        use_container_width=True
    )


# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    st.header("🔍 Data Explorer")

    dataset = st.selectbox(
        "Select Dataset",
        [
            "Raw Data",
            "Derived Data"
        ]
    )

    if dataset == "Raw Data":

        data = raw_data

    else:

        data = derived_data


    st.subheader("Dataset Preview")

    st.dataframe(
        data.head(200),
        use_container_width=True
    )


    st.divider()


    # --------------------------------------------------------
    # DATA INFORMATION
    # --------------------------------------------------------

    st.subheader("📋 Data Information")

    info = pd.DataFrame(
        {
            "Column": data.columns,
            "Data Type": [
                str(data[column].dtype)
                for column in data.columns
            ],
            "Missing Values": [
                int(data[column].isna().sum())
                for column in data.columns
            ],
            "Unique Values": [
                int(data[column].nunique())
                for column in data.columns
            ]
        }
    )

    st.dataframe(
        info,
        use_container_width=True
    )


    st.divider()


    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    st.subheader("🔎 Filter Data")

    categorical_columns = data.select_dtypes(
        include=["object"]
    ).columns.tolist()

    if categorical_columns:

        selected_column = st.selectbox(
            "Select Column",
            categorical_columns
        )

        values = (
            data[selected_column]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_values = st.multiselect(
            "Select Values",
            sorted(values.tolist())
        )

        if selected_values:

            filtered_data = data[
                data[selected_column]
                .astype(str)
                .isin(selected_values)
            ]

        else:

            filtered_data = data

        st.write(
            f"Records displayed: **{len(filtered_data):,}**"
        )

        st.dataframe(
            filtered_data.head(500),
            use_container_width=True
        )


# ============================================================
# SHIPPING OPTIMIZATION
# ============================================================

elif page == "Shipping Optimization":

    st.header("🚚 Shipping Optimization")

    st.write(
        "Analysis of shipping modes, lead time and regional "
        "shipping performance."
    )


    # --------------------------------------------------------
    # LEAD TIME KPIs
    # --------------------------------------------------------

    min_lead = derived_data[
        "Lead Time Days"
    ].min()

    max_lead = derived_data[
        "Lead Time Days"
    ].max()

    avg_lead = derived_data[
        "Lead Time Days"
    ].mean()


    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Minimum Lead Time",
            f"{min_lead:.0f} days"
        )

    with c2:

        st.metric(
            "Average Lead Time",
            f"{avg_lead:.2f} days"
        )

    with c3:

        st.metric(
            "Maximum Lead Time",
            f"{max_lead:.0f} days"
        )


    st.divider()


    # --------------------------------------------------------
    # LEAD TIME HISTOGRAM
    # --------------------------------------------------------

    st.subheader(
        "📊 Lead Time Distribution"
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.hist(
        derived_data["Lead Time Days"].dropna(),
        bins=30
    )

    ax.set_title(
        "Distribution of Shipping Lead Time"
    )

    ax.set_xlabel(
        "Lead Time (Days)"
    )

    ax.set_ylabel(
        "Number of Orders"
    )

    st.pyplot(fig)


    # --------------------------------------------------------
    # SHIPPING MODE
    # --------------------------------------------------------

    st.subheader(
        "🚛 Shipping Mode Analysis"
    )

    ship_mode_summary = (
        derived_data
        .groupby("Ship Mode")
        .agg(
            Shipments=("Order ID", "count"),
            Average_Lead_Time=("Lead Time Days", "mean"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum")
        )
        .reset_index()
    )

    ship_mode_summary[
        "Average_Lead_Time"
    ] = ship_mode_summary[
        "Average_Lead_Time"
    ].round(2)

    st.dataframe(
        ship_mode_summary,
        use_container_width=True
    )


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(
        ship_mode_summary["Ship Mode"],
        ship_mode_summary["Shipments"]
    )

    ax.set_title(
        "Orders by Shipping Mode"
    )

    ax.set_xlabel(
        "Shipping Mode"
    )

    ax.set_ylabel(
        "Number of Orders"
    )

    plt.xticks(
        rotation=30,
        ha="right"
    )

    st.pyplot(fig)


    # --------------------------------------------------------
    # REGION LEAD TIME
    # --------------------------------------------------------

    st.subheader(
        "🌎 Regional Lead Time"
    )

    region_lead = (
        derived_data
        .groupby("Region")
        .agg(
            Shipments=("Order ID", "count"),
            Average_Lead_Time=("Lead Time Days", "mean"),
            Sales=("Sales", "sum"),
            Profit=("Gross Profit", "sum")
        )
        .reset_index()
    )

    region_lead[
        "Average_Lead_Time"
    ] = region_lead[
        "Average_Lead_Time"
    ].round(2)

    st.dataframe(
        region_lead,
        use_container_width=True
    )


# ============================================================
# FACTORY REALLOCATION
# ============================================================

elif page == "Factory Reallocation":

    st.header("🏭 Factory Reallocation Analysis")

    st.info(
        """
        Important: the source dataset does not contain a direct
        factory-assignment field. The workbook therefore uses
        Division as a simulated operational profile for the
        reallocation analysis.
        """
    )


    # --------------------------------------------------------
    # FACTORY COORDINATES
    # --------------------------------------------------------

    try:

        factories = load_sheet(
            "Factory_Coordinates"
        )

        st.subheader(
            "📍 Factory Locations"
        )

        st.dataframe(
            factories,
            use_container_width=True
        )

        if {
            "Latitude",
            "Longitude"
        }.issubset(factories.columns):

            map_data = factories[
                [
                    "Latitude",
                    "Longitude"
                ]
            ].copy()

            map_data["Latitude"] = pd.to_numeric(
                map_data["Latitude"],
                errors="coerce"
            )

            map_data["Longitude"] = pd.to_numeric(
                map_data["Longitude"],
                errors="coerce"
            )

            map_data = map_data.dropna()

            if not map_data.empty:

                st.subheader(
                    "🗺️ Factory Location Map"
                )

                st.map(
                    map_data
                )

    except Exception as error:

        st.warning(
            f"Factory coordinates unavailable: {error}"
        )


    st.divider()


    # --------------------------------------------------------
    # DIVISION ANALYSIS
    # --------------------------------------------------------

    st.subheader(
        "🏭 Operational Profile Distribution"
    )

    division_summary = (
        derived_data
        .groupby("Division")
        .agg(
            Orders=("Order ID", "count"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum"),
            Average_Lead_Time=("Lead Time Days", "mean"),
            Average_Margin=("Profit Margin %", "mean")
        )
        .reset_index()
    )

    division_summary[
        "Average_Lead_Time"
    ] = division_summary[
        "Average_Lead_Time"
    ].round(2)

    division_summary[
        "Average_Margin"
    ] = division_summary[
        "Average_Margin"
    ].round(2)

    st.dataframe(
        division_summary,
        use_container_width=True
    )


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(
        division_summary["Division"],
        division_summary["Orders"]
    )

    ax.set_title(
        "Orders by Operational Profile"
    )

    ax.set_xlabel(
        "Division"
    )

    ax.set_ylabel(
        "Orders"
    )

    st.pyplot(fig)


    # --------------------------------------------------------
    # PRODUCT-FACTORY CORRELATION
    # --------------------------------------------------------

    try:

        correlation = load_sheet(
            "Product_Factory_Correlation"
        )

        st.subheader(
            "🍬 Product–Factory Correlation"
        )

        st.dataframe(
            correlation,
            use_container_width=True
        )

    except Exception:

        pass


# ============================================================
# SCENARIO ANALYSIS
# ============================================================

elif page == "Scenario Analysis":

    st.header(
        "🔄 What-If Factory Reallocation Analysis"
    )

    st.info(
        """
        This is a proxy simulation. It compares current operational
        profiles with alternative profiles using lead-time and
        margin effects contained in the workbook.
        """
    )


    try:

        scenario = load_sheet(
            "Scenario_Analysis"
        )


        # ----------------------------------------------------
        # NUMERIC CONVERSION
        # ----------------------------------------------------

        numeric_columns = [
            "Current Lead Time",
            "Scenario Lead Time",
            "Lead Time Reduction (Days)",
            "Lead Time Reduction (%)",
            "Current Avg Profit",
            "Scenario Avg Profit",
            "Current Margin %",
            "Scenario Margin %",
            "Margin Change (pp)",
            "Recommendation Score",
            "Shipments"
        ]

        for column in numeric_columns:

            if column in scenario.columns:

                scenario[column] = pd.to_numeric(
                    scenario[column],
                    errors="coerce"
                )


        # ----------------------------------------------------
        # KPI CALCULATIONS
        # ----------------------------------------------------

        avg_reduction = scenario[
            "Lead Time Reduction (Days)"
        ].mean()

        avg_reduction_pct = scenario[
            "Lead Time Reduction (%)"
        ].mean()

        avg_margin_change = scenario[
            "Margin Change (pp)"
        ].mean()


        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Avg Lead-Time Change",
                f"{avg_reduction:.2f} days"
            )

        with c2:

            st.metric(
                "Avg Lead-Time %",
                f"{avg_reduction_pct:.2f}%"
            )

        with c3:

            st.metric(
                "Avg Margin Change",
                f"{avg_margin_change:.2f} pp"
            )


        st.divider()


        # ----------------------------------------------------
        # SCENARIO TABLE
        # ----------------------------------------------------

        st.subheader(
            "Scenario Results"
        )

        st.dataframe(
            scenario.head(200),
            use_container_width=True
        )


        # ----------------------------------------------------
        # TOP POSITIVE SCENARIOS
        # ----------------------------------------------------

        positive = scenario[
            scenario["Lead Time Reduction (Days)"] > 0
        ].copy()

        positive = positive.sort_values(
            "Recommendation Score",
            ascending=False
        )


        st.subheader(
            "📈 Scenarios With Positive Lead-Time Reduction"
        )

        st.dataframe(
            positive.head(20),
            use_container_width=True
        )


        # ----------------------------------------------------
        # CHART
        # ----------------------------------------------------

        if not positive.empty:

            chart = positive.head(15)

            labels = (
                chart["Product"].astype(str)
                + " - "
                + chart["Region"].astype(str)
            )

            fig, ax = plt.subplots(
                figsize=(12, 6)
            )

            ax.bar(
                labels,
                chart["Lead Time Reduction (Days)"]
            )

            ax.set_title(
                "Top Scenario Lead-Time Reductions"
            )

            ax.set_ylabel(
                "Lead-Time Reduction (Days)"
            )

            ax.set_xlabel(
                "Product / Region"
            )

            plt.xticks(
                rotation=70,
                ha="right"
            )

            st.pyplot(fig)


    except Exception as error:

        st.error(
            f"Unable to load scenario analysis: {error}"
        )


# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.header(
        "💡 Reallocation Recommendations"
    )

    st.write(
        """
        The following recommendations are taken from the workbook's
        proxy scenario analysis. They should be interpreted as
        analytical opportunities rather than confirmed physical
        factory relocation decisions.
        """
    )


    try:

        recommendations = load_sheet(
            "Recommendations"
        )


        # ----------------------------------------------------
        # NUMERIC COLUMNS
        # ----------------------------------------------------

        for column in [
            "Current Lead Time",
            "Scenario Lead Time",
            "Lead Time Reduction (Days)",
            "Lead Time Reduction (%)",
            "Margin Change (pp)",
            "Recommendation Score"
        ]:

            if column in recommendations.columns:

                recommendations[column] = pd.to_numeric(
                    recommendations[column],
                    errors="coerce"
                )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        low_risk = 0
        medium_risk = 0
        high_risk = 0

        if "Risk Level" in recommendations.columns:

            low_risk = (
                recommendations["Risk Level"]
                .astype(str)
                .str.lower()
                .eq("low")
                .sum()
            )

            medium_risk = (
                recommendations["Risk Level"]
                .astype(str)
                .str.lower()
                .eq("medium")
                .sum()
            )

            high_risk = (
                recommendations["Risk Level"]
                .astype(str)
                .str.lower()
                .eq("high")
                .sum()
            )


        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Low Risk",
                low_risk
            )

        with c2:

            st.metric(
                "Medium Risk",
                medium_risk
            )

        with c3:

            st.metric(
                "High Risk",
                high_risk
            )


        st.divider()


        # ----------------------------------------------------
        # RECOMMENDATION TABLE
        # ----------------------------------------------------

        st.subheader(
            "📋 Recommendation Table"
        )

        st.dataframe(
            recommendations,
            use_container_width=True
        )


        # ----------------------------------------------------
        # TOP RECOMMENDATIONS
        # ----------------------------------------------------

        if "Recommendation Score" in recommendations.columns:

            top_recommendations = (
                recommendations
                .sort_values(
                    "Recommendation Score",
                    ascending=False
                )
                .head(15)
            )

            st.subheader(
                "📊 Highest Scoring Scenarios"
            )

            st.dataframe(
                top_recommendations,
                use_container_width=True
            )


    except Exception as error:

        st.error(
            f"Unable to load recommendations: {error}"
        )


# ============================================================
# K-MEANS CLUSTERING
# ============================================================

elif page == "K-Means Clustering":

    st.header(
        "🔵 K-Means Route & Product Combination Analysis"
    )

    try:

        clustering = load_sheet(
            "Clustering"
        )


        st.subheader(
            "Cluster Dataset"
        )

        st.dataframe(
            clustering,
            use_container_width=True
        )


        if "Cluster" in clustering.columns:

            clustering["Cluster"] = pd.to_numeric(
                clustering["Cluster"],
                errors="coerce"
            )


            # ------------------------------------------------
            # CLUSTER COUNTS
            # ------------------------------------------------

            cluster_counts = (
                clustering["Cluster"]
                .value_counts()
                .sort_index()
            )

            st.subheader(
                "📊 Cluster Distribution"
            )

            cols = st.columns(
                len(cluster_counts)
            )

            for index, (cluster, count) in enumerate(
                cluster_counts.items()
            ):

                with cols[index]:

                    st.metric(
                        f"Cluster {int(cluster)}",
                        f"{count:,}"
                    )


            # ------------------------------------------------
            # CLUSTER CHART
            # ------------------------------------------------

            fig, ax = plt.subplots(
                figsize=(10, 5)
            )

            ax.bar(
                cluster_counts.index.astype(str),
                cluster_counts.values
            )

            ax.set_title(
                "K-Means Cluster Distribution"
            )

            ax.set_xlabel(
                "Cluster"
            )

            ax.set_ylabel(
                "Number of Route/Product Combinations"
            )

            st.pyplot(fig)


            # ------------------------------------------------
            # CLUSTER SUMMARY
            # ------------------------------------------------

            numeric_cluster_columns = [
                column
                for column in [
                    "Shipment_Count",
                    "Avg_Lead_Time",
                    "Avg_Sales",
                    "Avg_Units",
                    "Avg_Gross_Profit",
                    "Avg_Cost",
                    "Avg_Margin"
                ]
                if column in clustering.columns
            ]

            if numeric_cluster_columns:

                for column in numeric_cluster_columns:

                    clustering[column] = pd.to_numeric(
                        clustering[column],
                        errors="coerce"
                    )


                cluster_summary = (
                    clustering
                    .groupby("Cluster")[
                        numeric_cluster_columns
                    ]
                    .mean()
                    .round(2)
                )

                st.subheader(
                    "📋 Cluster Performance Summary"
                )

                st.dataframe(
                    cluster_summary,
                    use_container_width=True
                )


    except Exception as error:

        st.error(
            f"Unable to load clustering analysis: {error}"
        )


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

elif page == "Correlation Analysis":

    st.header(
        "🔗 Product, Factory & Financial Correlation"
    )


    # --------------------------------------------------------
    # PRODUCT FACTORY CORRELATION
    # --------------------------------------------------------

    try:

        correlation_data = load_sheet(
            "Product_Factory_Correlation"
        )

        st.subheader(
            "🍬 Product–Factory Mapping"
        )

        st.dataframe(
            correlation_data,
            use_container_width=True
        )

    except Exception as error:

        st.warning(
            f"Product-factory correlation unavailable: {error}"
        )


    st.divider()


    # --------------------------------------------------------
    # NUMERIC CORRELATION
    # --------------------------------------------------------

    numeric_data = derived_data.select_dtypes(
        include=np.number
    )

    if numeric_data.shape[1] >= 2:

        st.subheader(
            "📈 Numerical Correlation Matrix"
        )

        correlation_matrix = (
            numeric_data
            .corr()
            .round(2)
        )

        st.dataframe(
            correlation_matrix,
            use_container_width=True
        )


        st.subheader(
            "Scatter Plot"
        )

        x_column = st.selectbox(
            "X Variable",
            numeric_data.columns
        )

        y_column = st.selectbox(
            "Y Variable",
            numeric_data.columns
        )


        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.scatter(
            numeric_data[x_column],
            numeric_data[y_column],
            alpha=0.5
        )

        ax.set_xlabel(
            x_column
        )

        ax.set_ylabel(
            y_column
        )

        ax.set_title(
            f"{x_column} vs {y_column}"
        )

        st.pyplot(fig)


# ============================================================
# WORKBOOK SHEETS
# ============================================================

elif page == "Workbook Sheets":

    st.header(
        "📚 Workbook Sheets"
    )

    selected_sheet = st.selectbox(
        "Select Excel Sheet",
        sheet_names
    )


    try:

        if selected_sheet == "Index":

            sheet_data = pd.read_excel(
                FILE_NAME,
                sheet_name="Index"
            )

        else:

            sheet_data = load_sheet(
                selected_sheet
            )


        st.subheader(
            f"📄 {selected_sheet}"
        )


        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Rows",
                f"{len(sheet_data):,}"
            )

        with c2:

            st.metric(
                "Columns",
                f"{len(sheet_data.columns):,}"
            )

        with c3:

            st.metric(
                "Missing Values",
                f"{int(sheet_data.isna().sum().sum()):,}"
            )


        st.dataframe(
            sheet_data,
            use_container_width=True
        )


        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        csv_data = sheet_data.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            "⬇️ Download Sheet as CSV",
            data=csv_data,
            file_name=f"{selected_sheet}.csv",
            mime="text/csv"
        )


    except Exception as error:

        st.error(
            f"Unable to read the selected sheet.\n\n{error}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    ## 🏭 Factory Reallocation & Shipping Optimization

    **Dataset:** Nassau Candy Distributor

    **Technology:** Python | Pandas | NumPy | Matplotlib | Streamlit

    **Analysis Areas:** Shipping Optimization • Factory Reallocation
    • Scenario Analysis • K-Means Clustering • Recommendations
    """
)