import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("insunsh.csv")

# Clean data
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['decade'] = df['dated'].str.extract(r'(\d{3})\s?\-?').astype(float) * 10

# Page config
st.set_page_config(page_title="Art Collection Insights", layout="wide")

# Sidebar filters
st.sidebar.header("Filters")
# selected_century = st.sidebar.selectbox("Century", options=["All"] + sorted(df['dated'].str.contains('century').dropna().unique().tolist()))
min_price, max_price = st.sidebar.slider("Price Range", float(df['price'].min()), float(df['price'].max()), (float(df['price'].min()), float(df['price'].max())))

# Apply filters
filtered_df = df.copy()
# if selected_century != "All":
#     filtered_df = filtered_df[filtered_df['dated'].str.contains(selected_century, na=False)]
filtered_df = filtered_df[(filtered_df['price'] >= min_price) & (filtered_df['price'] <= max_price)]

# Main content
st.title("🎨 Art Collection Analysis")
st.subheader("Collection Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Artworks", len(filtered_df))
col2.metric("Average Price", f"${filtered_df['price'].mean():,.2f}")
col3.metric("Unique Artists", filtered_df['artist'].nunique())

# Visualizations
st.subheader("Artwork Distribution")
tab1, tab2, tab3, tab4 = st.tabs(["By Century", "By Medium", "Price Distribution", "Location Status"])

with tab1:
    fig = px.histogram(filtered_df, x='decade', title="Artworks by Decade")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    medium_counts = filtered_df['medium'].value_counts().head(10)
    fig = px.bar(medium_counts, title="Top 10 Mediums")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.box(filtered_df, y='price', title="Price Distribution")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    location_counts = filtered_df['location'].value_counts()
    fig = px.pie(location_counts, values=location_counts.values, names=location_counts.index, title="Artwork Location Status")
    st.plotly_chart(fig, use_container_width=True)

# Artwork explorer
st.subheader("Artwork Explorer")
search_query = st.text_input("Search artworks by title or artist")

if search_query:
    search_results = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row['title']).lower() or 
                                 search_query.lower() in str(row['artist']).lower(), axis=1)]
else:
    search_results = filtered_df

st.dataframe(
    search_results[['title', 'artist', 'dated', 'medium', 'price']],
    column_config={
        "price": st.column_config.NumberColumn(
            "Price",
            format="$%.2f",
        )
    },
    hide_index=True,
    use_container_width=True
)

# Image gallery
st.subheader("Artwork Previews")
cols = st.columns(4)
for idx, (_, row) in enumerate(search_results.iterrows()):
    if pd.notnull(row['image']):
        with cols[idx % 4]:
            st.image(row['image'], caption=row['title'], use_container_width=True)
            if idx >= 15:  # Limit to 16 images
                break