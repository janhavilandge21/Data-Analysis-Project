import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import cv2
from PIL import Image
import io
import base64
from datetime import datetime, timedelta
import random

# Set page configuration
st.set_page_config(
    page_title="Plant Disease Analysis Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .plot-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🌱 Plant Disease Analysis")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "Choose Analysis Section",
    ["📊 Dashboard Overview", "🔍 Disease Detection", "📈 Trend Analysis", "🌍 Geographic Distribution", "📋 Data Management"]
)

# Sample data generation functions
def generate_sample_data():
    """Generate sample plant disease data"""
    diseases = ['Healthy', 'Bacterial Blight', 'Fungal Rust', 'Viral Mosaic', 'Powdery Mildew']
    plants = ['Tomato', 'Potato', 'Corn', 'Wheat', 'Rice', 'Soybean']
    locations = ['North Farm', 'South Farm', 'East Field', 'West Garden', 'Central Plot']
    
    data = []
    for _ in range(1000):
        data.append({
            'date': datetime.now() - timedelta(days=random.randint(0, 365)),
            'plant_type': random.choice(plants),
            'disease_type': random.choice(diseases),
            'severity': random.randint(1, 10),
            'location': random.choice(locations),
            'temperature': random.uniform(15, 35),
            'humidity': random.uniform(30, 90),
            'rainfall': random.uniform(0, 50),
            'treatment_applied': random.choice(['Yes', 'No']),
            'recovery_rate': random.uniform(0, 100)
        })
    
    return pd.DataFrame(data)

def generate_trend_data():
    """Generate trend data for time series analysis"""
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    trend_data = []
    
    for date in dates:
        trend_data.append({
            'date': date,
            'healthy_count': random.randint(80, 120),
            'diseased_count': random.randint(10, 40),
            'temperature_avg': random.uniform(20, 30),
            'humidity_avg': random.uniform(50, 80),
            'new_cases': random.randint(0, 15)
        })
    
    return pd.DataFrame(trend_data)

# Load sample data
@st.cache_data
def load_data():
    return generate_sample_data()

@st.cache_data
def load_trend_data():
    return generate_trend_data()

# Main application logic
if page == "📊 Dashboard Overview":
    st.markdown('<h1 class="main-header">Plant Disease Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    trend_df = load_trend_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Plants Analyzed",
            value=f"{len(df):,}",
            delta=f"+{random.randint(5, 20)}"
        )
    
    with col2:
        healthy_count = len(df[df['disease_type'] == 'Healthy'])
        st.metric(
            label="Healthy Plants",
            value=f"{healthy_count:,}",
            delta=f"{healthy_count/len(df)*100:.1f}%"
        )
    
    with col3:
        diseased_count = len(df[df['disease_type'] != 'Healthy'])
        st.metric(
            label="Diseased Plants",
            value=f"{diseased_count:,}",
            delta=f"{diseased_count/len(df)*100:.1f}%"
        )
    
    with col4:
        avg_severity = df[df['disease_type'] != 'Healthy']['severity'].mean()
        st.metric(
            label="Avg Disease Severity",
            value=f"{avg_severity:.1f}/10",
            delta=f"-{random.uniform(0.1, 0.5):.1f}"
        )
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Disease Distribution")
        disease_counts = df['disease_type'].value_counts()
        fig = px.pie(
            values=disease_counts.values,
            names=disease_counts.index,
            title="Distribution of Plant Diseases",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Plant Type Analysis")
        plant_disease = df.groupby(['plant_type', 'disease_type']).size().reset_index(name='count')
        fig = px.bar(
            plant_disease,
            x='plant_type',
            y='count',
            color='disease_type',
            title="Disease Cases by Plant Type",
            barmode='group'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Severity Distribution")
        fig = px.histogram(
            df[df['disease_type'] != 'Healthy'],
            x='severity',
            nbins=20,
            title="Disease Severity Distribution",
            color_discrete_sequence=['#FF6B6B']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Environmental Factors")
        fig = px.scatter(
            df,
            x='temperature',
            y='humidity',
            color='disease_type',
            size='severity',
            title="Disease vs Environmental Conditions",
            hover_data=['plant_type', 'location']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Time series trend
    st.subheader("Disease Trends Over Time")
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Disease Cases', 'Environmental Conditions'),
        vertical_spacing=0.1
    )
    
    fig.add_trace(
        go.Scatter(x=trend_df['date'], y=trend_df['diseased_count'], 
                   name='Diseased Plants', line=dict(color='red')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=trend_df['date'], y=trend_df['temperature_avg'], 
                   name='Temperature', line=dict(color='orange'), yaxis='y2'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=trend_df['date'], y=trend_df['humidity_avg'], 
                   name='Humidity', line=dict(color='blue'), yaxis='y3'),
        row=2, col=1
    )
    
    fig.update_layout(height=600, title_text="Disease Trends and Environmental Factors")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🔍 Disease Detection":
    st.markdown('<h1 class="main-header">Plant Disease Detection</h1>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a plant image for disease detection",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image of a plant leaf or stem for disease analysis"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Image Upload")
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Simulate image processing
            with st.spinner("Analyzing image..."):
                # Simulate processing time
                import time
                time.sleep(2)
                
                # Generate mock detection results
                diseases = ['Healthy', 'Bacterial Blight', 'Fungal Rust', 'Viral Mosaic', 'Powdery Mildew']
                confidence_scores = [random.uniform(0.7, 0.99) for _ in range(5)]
                total = sum(confidence_scores)
                confidence_scores = [score/total for score in confidence_scores]
                
                results = list(zip(diseases, confidence_scores))
                results.sort(key=lambda x: x[1], reverse=True)
    
    with col2:
        st.subheader("Detection Results")
        if uploaded_file is not None:
            # Display results
            for disease, confidence in results:
                color = "green" if disease == "Healthy" else "red"
                st.markdown(f"""
                <div style="padding: 10px; margin: 5px 0; border-radius: 5px; background-color: {color}20;">
                    <strong>{disease}</strong>: {confidence:.1%}
                </div>
                """, unsafe_allow_html=True)
            
            # Confidence bar chart
            fig = px.bar(
                x=[r[0] for r in results],
                y=[r[1] for r in results],
                title="Disease Detection Confidence",
                color=[r[1] for r in results],
                color_continuous_scale='RdYlGn_r'
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please upload an image to begin analysis")
    
    # Batch analysis section
    st.markdown("---")
    st.subheader("Batch Analysis")
    
    # Generate sample batch results
    sample_batch = pd.DataFrame({
        'Image_ID': [f'IMG_{i:03d}' for i in range(1, 21)],
        'Plant_Type': [random.choice(['Tomato', 'Potato', 'Corn', 'Wheat']) for _ in range(20)],
        'Detected_Disease': [random.choice(['Healthy', 'Bacterial Blight', 'Fungal Rust', 'Viral Mosaic']) for _ in range(20)],
        'Confidence': [random.uniform(0.7, 0.99) for _ in range(20)],
        'Severity': [random.randint(1, 10) for _ in range(20)]
    })
    
    st.dataframe(sample_batch, use_container_width=True)
    
    # Batch analysis visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            sample_batch,
            x='Detected_Disease',
            title="Batch Analysis Results",
            color_discrete_sequence=['#2E8B57']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            sample_batch,
            x='Confidence',
            y='Severity',
            color='Detected_Disease',
            title="Confidence vs Severity",
            size='Confidence'
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "📈 Trend Analysis":
    st.markdown('<h1 class="main-header">Disease Trend Analysis</h1>', unsafe_allow_html=True)
    
    df = load_data()
    trend_df = load_trend_data()
    
    # Time period selector
    col1, col2 = st.columns(2)
    with col1:
        time_period = st.selectbox(
            "Select Time Period",
            ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year"]
        )
    
    with col2:
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Disease Incidence", "Environmental Correlation", "Treatment Effectiveness", "Geographic Spread"]
        )
    
    # Trend analysis plots
    if analysis_type == "Disease Incidence":
        st.subheader("Disease Incidence Trends")
        
        # Monthly disease counts
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
        monthly_counts = df.groupby(['month', 'disease_type']).size().reset_index(name='count')
        monthly_counts['month'] = monthly_counts['month'].astype(str)
        
        fig = px.line(
            monthly_counts,
            x='month',
            y='count',
            color='disease_type',
            title="Monthly Disease Incidence Trends"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap of disease patterns
        st.subheader("Disease Pattern Heatmap")
        pivot_data = monthly_counts.pivot(index='month', columns='disease_type', values='count').fillna(0)
        
        fig = px.imshow(
            pivot_data,
            title="Disease Pattern Heatmap",
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Environmental Correlation":
        st.subheader("Environmental Factor Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperature vs Disease
            fig = px.scatter(
                df,
                x='temperature',
                y='severity',
                color='disease_type',
                title="Temperature vs Disease Severity",
                trendline="ols"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Humidity vs Disease
            fig = px.scatter(
                df,
                x='humidity',
                y='severity',
                color='disease_type',
                title="Humidity vs Disease Severity",
                trendline="ols"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation matrix
        st.subheader("Environmental Correlation Matrix")
        env_data = df[['temperature', 'humidity', 'rainfall', 'severity']].corr()
        
        fig = px.imshow(
            env_data,
            title="Environmental Factor Correlation",
            color_continuous_scale='RdBu',
            text_auto=True
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Treatment Effectiveness":
        st.subheader("Treatment Effectiveness Analysis")
        
        # Treatment success rate
        treatment_data = df.groupby(['disease_type', 'treatment_applied']).agg({
            'recovery_rate': 'mean',
            'severity': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                treatment_data,
                x='disease_type',
                y='recovery_rate',
                color='treatment_applied',
                title="Recovery Rate by Treatment",
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                treatment_data,
                x='disease_type',
                y='severity',
                color='treatment_applied',
                title="Severity by Treatment",
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Geographic Spread":
        st.subheader("Geographic Disease Spread")
        
        # Location-based analysis
        location_data = df.groupby(['location', 'disease_type']).size().reset_index(name='count')
        
        fig = px.treemap(
            location_data,
            path=['location', 'disease_type'],
            values='count',
            title="Disease Distribution by Location"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

elif page == "🌍 Geographic Distribution":
    st.markdown('<h1 class="main-header">Geographic Disease Distribution</h1>', unsafe_allow_html=True)
    
    df = load_data()
    
    # Mock geographic coordinates
    locations_coords = {
        'North Farm': (40.7128, -74.0060),
        'South Farm': (34.0522, -118.2437),
        'East Field': (39.9526, -75.1652),
        'West Garden': (37.7749, -122.4194),
        'Central Plot': (41.8781, -87.6298)
    }
    
    # Add coordinates to dataframe
    df['lat'] = df['location'].map(lambda x: locations_coords[x][0])
    df['lon'] = df['location'].map(lambda x: locations_coords[x][1])
    
    # Geographic visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Disease Hotspots")
        
        # Aggregate data by location
        location_summary = df.groupby(['location', 'lat', 'lon', 'disease_type']).size().reset_index(name='count')
        
        fig = px.scatter_mapbox(
            location_summary,
            lat='lat',
            lon='lon',
            size='count',
            color='disease_type',
            hover_name='location',
            hover_data=['count'],
            title="Disease Distribution Map",
            mapbox_style="open-street-map",
            zoom=3
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Location Statistics")
        
        # Location-based statistics
        location_stats = df.groupby('location').agg({
            'disease_type': lambda x: (x != 'Healthy').sum(),
            'severity': 'mean',
            'recovery_rate': 'mean'
        }).reset_index()
        location_stats.columns = ['Location', 'Diseased_Count', 'Avg_Severity', 'Avg_Recovery_Rate']
        
        fig = px.bar(
            location_stats,
            x='Location',
            y='Diseased_Count',
            title="Disease Cases by Location",
            color='Avg_Severity',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Regional analysis
    st.subheader("Regional Disease Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Disease prevalence by region
        region_disease = df.groupby(['location', 'disease_type']).size().reset_index(name='count')
        
        fig = px.sunburst(
            region_disease,
            path=['location', 'disease_type'],
            values='count',
            title="Regional Disease Distribution"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Environmental conditions by region
        region_env = df.groupby('location').agg({
            'temperature': 'mean',
            'humidity': 'mean',
            'rainfall': 'mean'
        }).reset_index()
        
        fig = px.radar(
            region_env,
            r=['temperature', 'humidity', 'rainfall'],
            theta=['temperature', 'humidity', 'rainfall'],
            color='location',
            title="Environmental Conditions by Region"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "📋 Data Management":
    st.markdown('<h1 class="main-header">Data Management</h1>', unsafe_allow_html=True)
    
    df = load_data()
    
    # Data overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    
    with col2:
        st.metric("Unique Plants", df['plant_type'].nunique())
    
    with col3:
        st.metric("Unique Diseases", df['disease_type'].nunique())
    
    # Data filters
    st.subheader("Data Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_plants = st.multiselect(
            "Filter by Plant Type",
            options=df['plant_type'].unique(),
            default=df['plant_type'].unique()
        )
    
    with col2:
        selected_diseases = st.multiselect(
            "Filter by Disease Type",
            options=df['disease_type'].unique(),
            default=df['disease_type'].unique()
        )
    
    with col3:
        severity_range = st.slider(
            "Severity Range",
            min_value=1,
            max_value=10,
            value=(1, 10)
        )
    
    # Filter data
    filtered_df = df[
        (df['plant_type'].isin(selected_plants)) &
        (df['disease_type'].isin(selected_diseases)) &
        (df['severity'].between(severity_range[0], severity_range[1]))
    ]
    
    # Display filtered data
    st.subheader("Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Data export
    st.subheader("Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export to CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"plant_disease_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export to Excel"):
            # Create Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, sheet_name='Plant Disease Data', index=False)
            
            excel_data = output.getvalue()
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=f"plant_disease_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # Data quality metrics
    st.subheader("Data Quality Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Missing data analysis
        missing_data = df.isnull().sum()
        fig = px.bar(
            x=missing_data.index,
            y=missing_data.values,
            title="Missing Data by Column",
            color_discrete_sequence=['#FF6B6B']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Data completeness
        completeness = (1 - df.isnull().sum() / len(df)) * 100
        fig = px.bar(
            x=completeness.index,
            y=completeness.values,
            title="Data Completeness (%)",
            color_discrete_sequence=['#2E8B57']
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 20px;">
        🌱 Plant Disease Analysis Dashboard | Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
) 