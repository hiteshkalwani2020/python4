import plotly.express as px

def plot_trends(trend_df, top_n=5):
    # Get the top N hashtags overall
    top_hashtags = (
        trend_df.groupby('hashtags')['count'].sum()
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )
    filtered = trend_df[trend_df['hashtags'].isin(top_hashtags)]
    fig = px.line(
        filtered,
        x='datetime',
        y='count',
        color='hashtags',
        markers=True,
        title=f"Top {top_n} Trending Hashtags Over Time"
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Count")
    return fig
