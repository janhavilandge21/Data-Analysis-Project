
import streamlit as st                       
import pandas as pd                           
import numpy as np                           
import re                                  
import matplotlib.pyplot as plt               
import seaborn as sns                         
from sklearn.model_selection import train_test_split  
from sklearn.ensemble import RandomForestRegressor    
from sklearn.preprocessing import LabelEncoder       
from sklearn.metrics import mean_absolute_error, r2_score 
import plotly.express as px
                    
import warnings                               
warnings.filterwarnings("ignore")               


st.set_page_config(page_title="Data Analyst Jobs — Salary Analysis & Prediction",
                   layout="wide")             
st.title("Data Analyst Job Market Analysis & Salary Prediction")  

@st.cache_data
def load_data(file) -> pd.DataFrame:
    """Load CSV file into a DataFrame and return it."""
    return pd.read_csv(file)                    # read CSV from uploaded file

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names: strip, lower, replace spaces."""
    df = df.copy()                              
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('/', '_').str.lower()
    return df

def parse_salary_text(salary_text: str):
    """
    Parse a salary text like '$40K-$70K (Glassdoor est.)' into min, max, avg, is_hourly.
    Returns (min_annual, max_annual, avg_annual, is_hourly)
    """
    if pd.isna(salary_text):
        return (np.nan, np.nan, np.nan, False)   
    s = str(salary_text).lower()                 
    is_hourly = bool(re.search(r'per\s*hour|/hour|hourly|/hr|per\s*hr', s))  
    
    # remove parentheses and notes
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r'employer provided salary:|employer provided|glassdoor est\.?', ' ', s)
    s = s.replace(',', ' ')                      
    s = s.replace('$', '')      
                     
    # find numbers possibly with 'k'
    matches = re.findall(r'(\d+(?:\.\d+)?)(k)?', s)
    if not matches:
        return (np.nan, np.nan, np.nan, is_hourly)
    nums = []
    had_k = False
    for num_str, kflag in matches:
        val = float(num_str)
        if kflag:
            val *= 1000.0
            had_k = True
        nums.append(val)
    if len(nums) == 1:
        min_val = max_val = nums[0]
    else:
        min_val = nums[0]
        max_val = nums[1]

    if max_val is not None and max_val < 1000 and not had_k and not is_hourly:
        min_val *= 1000.0
        max_val *= 1000.0

    if is_hourly:
        min_val = min_val * 2080.0
        max_val = max_val * 2080.0
    avg_val = (min_val + max_val) / 2.0 if (not np.isnan(min_val) and not np.isnan(max_val)) else np.nan
    return (min_val, max_val, avg_val, is_hourly)

@st.cache_data
def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Perform data-cleaning, feature engineering and return processed df."""
    df = df.copy()                               
    df = clean_column_names(df)                  
    # fill rating missing values with median
    if 'rating' in df.columns:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['rating'].fillna(df['rating'].median(), inplace=True)
    # find salary-like column
    salary_col = None
    for col in df.columns:
        if 'salary' in col:
            salary_col = col
            break
    # parse salary column if found
    if salary_col is not None:
        parsed = df[salary_col].apply(parse_salary_text).apply(pd.Series)
        parsed.columns = ['min_annual', 'max_annual', 'avg_annual', 'is_hourly']
        df = pd.concat([df, parsed], axis=1)
        # make K-scale columns for convenience
        df['min_k'] = df['min_annual'] / 1000.0
        df['avg_k'] = df['avg_annual'] / 1000.0
    else:
        # create empty numeric salary columns to avoid downstream break
        df['min_annual'] = np.nan
        df['max_annual'] = np.nan
        df['avg_annual'] = np.nan
        df['min_k'] = np.nan
        df['avg_k'] = np.nan
    # simple skill flags from job description
    if 'job_description' in df.columns:
        df['has_python'] = df['job_description'].str.contains('python', case=False, na=False).astype(int)
        df['has_excel'] = df['job_description'].str.contains('excel', case=False, na=False).astype(int)
        df['tech_skills_count'] = df[['has_python', 'has_excel']].sum(axis=1)
    else:
        df['has_python'] = 0
        df['has_excel'] = 0
        df['tech_skills_count'] = 0
    # extract city, state from location if available
    if 'location' in df.columns:
        parts = df['location'].astype(str).str.split(',', n=1, expand=True)
        df['city'] = parts[0].str.strip()
        if parts.shape[1] > 1:
            df['state'] = parts[1].str.strip().str.split().str[0]
        else:
            df['state'] = np.nan
        # handle remote keywords
        remote_keywords = {'remote', 'work from home', 'wfh', 'anywhere'}
        remote_mask = df['city'].str.lower().isin(remote_keywords)
        df.loc[remote_mask, ['city','state']] = np.nan
    # tidy up size/founded columns
    if 'size' in df.columns:
        df['size'] = df['size'].astype(str)
        # label encode size for modelling later (temporary numeric mapping)
        le = LabelEncoder()
        df['size_encoded'] = le.fit_transform(df['size'].fillna('-1'))
    else:
        df['size_encoded'] = 0
    if 'founded' in df.columns:
        df['founded'] = pd.to_numeric(df['founded'], errors='coerce').fillna(0).astype(int)
    else:
        df['founded'] = 0
    # final drop/keep choices can be placed here
    return df

@st.cache_data
def train_model(df: pd.DataFrame):
    """Train a RandomForestRegressor on cleaned dataframe and return (model, features)."""
    
    features = []
    if 'rating' in df.columns:
        features.append('rating')
    if 'tech_skills_count' in df.columns:
        features.append('tech_skills_count')
    if 'size_encoded' in df.columns:
        features.append('size_encoded')
    if 'founded' in df.columns:
        features.append('founded')
    # ensure target exists
    if 'avg_annual' not in df.columns:
        return None, features, None, None 
    X = df[features].fillna(0)
    y = df['avg_annual'].fillna(df['avg_annual'].median())
    # simple train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # train a simple Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    # predictions + evaluation
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return model, features, mae, r2

# Sidebar: file upload & options

st.sidebar.header("Upload & Options")         
uploaded_file = st.sidebar.file_uploader("Upload CSV file (DataAnalyst.csv)", type=["csv"])  
sample_checkbox = st.sidebar.checkbox("Show sample dataset preview", value=True) 


# Main: Load and preprocess

if uploaded_file is not None:
    # show original dataset preview if requested
    raw_df = load_data(uploaded_file)         
    if sample_checkbox:
        st.subheader("Raw dataset preview")    
        st.dataframe(raw_df.head(10))         
    # preprocess and feature-engineer dataset
    with st.spinner("Preprocessing dataset..."):
        df = preprocess_dataframe(raw_df)     
    st.success("Preprocessing complete!")     
    # quick dataset summary
    st.write(f"Number of rows: {df.shape[0]}, Number of columns: {df.shape[1]}")  
    # show column list
    st.write("Columns:", df.columns.tolist())  

    
    # Exploratory Data Analysis (visuals)

    st.header("Exploratory Data Analysis (EDA)") 
    col1, col2 = st.columns(2)                  

    # Salary distribution histogram (if avg_k exists)
    if 'avg_k' in df.columns and df['avg_k'].notna().sum() > 0:
        with col1:
            st.subheader("Salary (Avg, in K) Distribution")
            fig = px.histogram(df, x='avg_k', nbins=30, title="Average Salary (K)")  
            st.plotly_chart(fig, use_container_width=True)  
    else:
        with col1:
            st.info("No parsed salary data to show distribution.")

    # Top job titles bar chart
    with col2:
        st.subheader("Top Job Titles")
        if 'job_title' in df.columns:
            top_jobs = df['job_title'].value_counts().nlargest(10)
            fig2 = px.bar(x=top_jobs.values, y=top_jobs.index, orientation='h', labels={'x':'Count','y':'Job Title'},
                          title="Top 10 Job Titles")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No job_title column found.")

    # Correlation heatmap (numeric)
    st.subheader("Numeric Correlation Matrix")
    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        corr = numeric.corr()
        fig3 = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No numeric columns found for correlation.")

    # Company ratings by industry boxplot (if industry & rating exist)
    if 'industry' in df.columns and 'rating' in df.columns:
        st.subheader("Company Ratings by Industry (Top 10 Industries)")
        top_inds = df['industry'].value_counts().nlargest(10).index
        subset = df[df['industry'].isin(top_inds)]
        fig4 = px.box(subset, x='industry', y='rating', title="Ratings by Industry")
        fig4.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig4, use_container_width=True)

    # --------------------------
    # Data Cleaning summary & missing values
    # --------------------------
    st.header("Cleaning & Missing Values")
    missing = df.isnull().sum().sort_values(ascending=False)
    st.write("Missing values per column (top 20):")
    st.dataframe(missing.head(20))

    # --------------------------
    # Model training & evaluation
    # --------------------------
    st.header("Salary Prediction Model")
    model, model_features, mae, r2 = train_model(df)  
    if model is None:
        st.info("Not enough data to train a model (missing salary target).")
    else:
        st.write("Model features used:", model_features)  
        st.write(f"Model evaluation — MAE: ${mae:,.2f}, R²: {r2:.3f}") 

        
        # Interactive prediction UI
    
        st.subheader("Predict Salary for a Hypothetical Company")
        # create UI controls for features (use reasonable defaults)
        # rating slider
        rating_input = st.slider("Company Rating (1-5)", min_value=1.0, max_value=5.0, value=float(df['rating'].median() if 'rating' in df.columns else 3.0), step=0.1)
        # size selectbox: show unique sizes in dataset if available
        if 'size' in df.columns:
            unique_sizes = df['size'].fillna('-1').unique().tolist()
            size_choice = st.selectbox("Company Size (raw)", options=unique_sizes, index=0)
            # encode chosen size using label encoder trained on df (recreate encoder)
            le = LabelEncoder()
            le.fit(df['size'].fillna('-1'))
            size_encoded = int(le.transform([size_choice])[0])
        else:
            size_encoded = 0
        # founded year
        founded_input = st.number_input("Year Founded", min_value=1800, max_value=2100, value=int(df['founded'].median() if 'founded' in df.columns else 2000))
        # skills (python & excel) checkboxes
        python_flag = st.checkbox("Job requires Python skills", value=True)
        excel_flag = st.checkbox("Job requires Excel skills", value=True)
        tech_skills_count_input = int(python_flag) + int(excel_flag)

        # prepare feature vector in same order as model_features
        feature_vector = []
        for feat in model_features:
            if feat == 'rating':
                feature_vector.append(float(rating_input))
            elif feat == 'size_encoded':
                feature_vector.append(int(size_encoded))
            elif feat == 'founded':
                feature_vector.append(int(founded_input))
            elif feat == 'tech_skills_count':
                feature_vector.append(int(tech_skills_count_input))
            else:
                # default fallback 0
                feature_vector.append(0)

        # predict on button press
        if st.button("Predict Salary"):
            pred = model.predict([feature_vector])[0]          
            st.success(f"Predicted Average Salary: ${pred:,.2f} per year")
            st.info(f"Equivalent ~ ${pred/1000:,.2f}K per year")

    # --------------------------
    # Download cleaned data & model info (optional)
    # --------------------------
    st.header("Export & Save")
    if st.button("Show cleaned dataframe head"):
        st.dataframe(df.head(20))
    # provide CSV download of cleaned dataframe
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download cleaned dataset (CSV)", data=csv, file_name='cleaned_data.csv', mime='text/csv')

else:
    # when no file uploaded, show instructions and a tiny sample example
    st.info("Upload your DataAnalyst CSV file using the left sidebar. The app will preprocess, visualize, and train a salary prediction model if salary data is available.")
    # optional: show minimal sample dataframe layout to guide user
    sample = {
        "Job Title": ["Data Analyst", "Senior Data Analyst"],
        "Salary Estimate": ["$40K-$70K (Glassdoor est.)", "$60K-$110K (Glassdoor est.)"],
        "Job Description": ["Python, Excel required", "SQL, Python, Excel required"],
        "Rating": [3.8, 4.0],
        "Company Name": ["ABC Corp", "XYZ Inc"],
        "Location": ["New York, NY", "San Francisco, CA"],
        "Size": ["51-200 employees", "1001-5000 employees"],
        "Founded": [2010, 1998]
    }
    st.dataframe(pd.DataFrame(sample))

# --------------------------
# Footer / help
# --------------------------
st.markdown("---")                            
st.write("Tips: If your dataset column names differ (e.g., 'Salary Estimate' vs 'salary_estimate'), the app attempts to auto-detect a salary-like column. Ensure job description and location columns exist for best results.")
