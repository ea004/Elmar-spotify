import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime
import calendar
import numpy as np

class YouTubeHistoryVisualizer:
    def __init__(self, data_file):
        self.df = pd.read_csv(data_file)
        self.df['Watch Date & Time'] = pd.to_datetime(self.df['Watch Date & Time'])
        self.results_dir = Path(__file__).parent.parent.parent / 'results'
        self.figures_dir = self.results_dir / 'figures'
        self.stats_dir = self.results_dir / 'stats'
        
        # Set custom color palette and style
        self.color_palette = sns.color_palette("husl", 15)  # Increased colors for more variety
        self.bar_colors = sns.color_palette("Set3", 15)     # Softer colors for bars
        
        # Use a built-in style instead of seaborn
        plt.style.use('bmh')  # Alternative: 'fivethirtyeight', 'ggplot', 'classic'
        sns.set_theme()  # This will set seaborn defaults without requiring the style file
        sns.set_palette(self.color_palette)

    def generate_basic_stats(self):
        """Generate basic statistics about the viewing history."""
        stats = {
            'total_videos_watched': len(self.df),
            'unique_channels': len(self.df['Channel Name'].unique()),
            'date_range': {
                'start': self.df['Watch Date & Time'].min().strftime('%Y-%m-%d'),
                'end': self.df['Watch Date & Time'].max().strftime('%Y-%m-%d')
            },
            'most_active_day': self.df.groupby(self.df['Watch Date & Time'].dt.date).size().idxmax().strftime('%Y-%m-%d'),
            'average_videos_per_day': self.df.groupby(self.df['Watch Date & Time'].dt.date).size().mean()
        }
        
        # Save stats to JSON
        with open(self.stats_dir / 'basic_stats.json', 'w') as f:
            json.dump(stats, f, indent=4)
        
        return stats

    def plot_daily_views(self):
        """Plot number of videos watched per day with rolling average."""
        daily_views = self.df.groupby(self.df['Watch Date & Time'].dt.date).size()
        
        plt.figure(figsize=(15, 8))
        plt.plot(daily_views.index, daily_views, alpha=0.3, color=self.color_palette[0], label='Daily Views')
        plt.plot(daily_views.index, daily_views.rolling(window=7).mean(), 
                color=self.color_palette[1], linewidth=2, label='7-day Moving Average')
        plt.plot(daily_views.index, daily_views.rolling(window=30).mean(), 
                color=self.color_palette[2], linewidth=2, label='30-day Moving Average')
        
        plt.title('Daily Viewing Patterns (2021-2024)', fontsize=14, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Videos Watched', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10)
        
        # Add annotations for key events
        max_day = daily_views.idxmax()
        plt.annotate(f'Peak: {daily_views.max()} videos\n{max_day}',
                    xy=(max_day, daily_views.max()),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->'))
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'daily_views.png', dpi=300, bbox_inches='tight')
        plt.close()

    def plot_top_channels(self, top_n=15):
        """Plot top N most watched channels with percentage."""
        channel_counts = self.df['Channel Name'].value_counts()
        top_channels = channel_counts.head(top_n)
        
        plt.figure(figsize=(15, 8))
        ax = plt.gca()
        bars = ax.bar(range(len(top_channels)), top_channels.values, 
                     color=self.bar_colors[:len(top_channels)])
        
        plt.title(f'Top {top_n} Most Watched Channels', fontsize=14, pad=20)
        plt.xlabel('Channel', fontsize=12)
        plt.ylabel('Number of Videos', fontsize=12)
        plt.xticks(range(len(top_channels)), top_channels.index, rotation=45, ha='right')
        
        # Add percentage labels
        total_videos = len(self.df)
        for i, v in enumerate(top_channels):
            percentage = (v / total_videos) * 100
            ax.text(i, v, f'{percentage:.1f}%', 
                   ha='center', va='bottom', fontsize=10)
        
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'top_channels.png', dpi=300, bbox_inches='tight')
        plt.close()

    def plot_hourly_distribution(self):
        """Removed as hour data is not available"""
        pass

    def plot_weekly_patterns(self):
        """Plot viewing patterns by day of week."""
        self.df['Weekday'] = self.df['Watch Date & Time'].dt.day_name()
        weekly_views = self.df['Weekday'].value_counts()
        weekly_views = weekly_views.reindex(list(calendar.day_name))
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(weekly_views)), weekly_views.values, 
                      color=self.bar_colors[:len(weekly_views)])
        
        plt.title('Viewing Patterns by Day of Week', fontsize=14, pad=20)
        plt.xlabel('Day of Week', fontsize=12)
        plt.ylabel('Number of Videos', fontsize=12)
        plt.xticks(range(len(weekly_views)), weekly_views.index, rotation=45)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom')
        
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'weekly_patterns.png', dpi=300, bbox_inches='tight')
        plt.close()

    def plot_monthly_trends(self):
        """Plot viewing trends by month."""
        monthly_views = self.df.groupby(self.df['Watch Date & Time'].dt.to_period('M')).size()
        
        plt.figure(figsize=(15, 8))
        monthly_views.plot(kind='bar')
        plt.title('Monthly Viewing Trends')
        plt.xlabel('Month')
        plt.ylabel('Number of Videos')
        plt.grid(True, axis='y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'monthly_trends.png')
        plt.close()

    def generate_channel_stats(self):
        """Generate detailed statistics about channel viewing patterns."""
        channel_stats = {
            'top_channels': self.df['Channel Name'].value_counts().head(20).to_dict(),
            'monthly_top_channels': {}
        }

        # Get top channel for each month
        for name, group in self.df.groupby(self.df['Watch Date & Time'].dt.to_period('M')):
            top_channel = group['Channel Name'].value_counts().index[0]
            channel_stats['monthly_top_channels'][str(name)] = top_channel

        with open(self.stats_dir / 'channel_stats.json', 'w') as f:
            json.dump(channel_stats, f, indent=4)

    def plot_category_distribution(self):
        """Plot category distribution with percentages."""
        category_stats = pd.read_csv(self.stats_dir / 'category_stats.csv')
        
        plt.figure(figsize=(15, 8))
        bars = plt.bar(range(len(category_stats)), category_stats['percentage'], 
                      color=self.bar_colors)
        
        plt.title('Content Category Distribution', fontsize=14, pad=20)
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Percentage of Videos (%)', fontsize=12)
        plt.xticks(range(len(category_stats)), category_stats['category'], 
                  rotation=45, ha='right')
        
        # Add percentage labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom')
        
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'category_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_monthly_heatmap(self):
        """Create monthly viewing heatmap."""
        monthly_views = self.df.groupby([
            self.df['Watch Date & Time'].dt.year,
            self.df['Watch Date & Time'].dt.month
        ]).size().unstack()
        
        plt.figure(figsize=(15, 8))
        sns.heatmap(monthly_views, cmap='YlOrRd', annot=True, fmt='g',
                   cbar_kws={'label': 'Number of Videos'})
        
        plt.title('Monthly Viewing Activity (2021-2024)', fontsize=14, pad=20)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Year', fontsize=12)
        
        # Format month labels
        plt.xticks(range(12), calendar.month_abbr[1:], rotation=0)
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'monthly_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()

    def analyze_category_correlations(self):
        """Analyze correlations between different content categories."""
        # Create category presence matrix
        category_stats = pd.read_csv(self.stats_dir / 'category_stats.csv')
        categories = category_stats['category'].tolist()
        
        # Initialize correlation matrix with zeros
        correlation_matrix = np.zeros((len(categories), len(categories)))
        
        # Calculate correlations
        for i, cat1 in enumerate(categories):
            for j, cat2 in enumerate(categories):
                # Count videos containing both categories
                videos_cat1 = self.df[self.df['Video Title'].str.contains(cat1, case=False, na=False)]
                videos_cat2 = self.df[self.df['Video Title'].str.contains(cat2, case=False, na=False)]
                both = len(set(videos_cat1.index) & set(videos_cat2.index))
                
                # Calculate Jaccard similarity
                union = len(set(videos_cat1.index) | set(videos_cat2.index))
                correlation = both / union if union > 0 else 0
                correlation_matrix[i, j] = correlation
        
        # Create DataFrame for better visualization
        correlation_df = pd.DataFrame(
            correlation_matrix,
            index=categories,
            columns=categories
        )
        
        plt.figure(figsize=(15, 12))
        mask = np.triu(np.ones_like(correlation_df), k=1)  # Mask upper triangle
        sns.heatmap(correlation_df, 
                    mask=mask,
                    annot=True, 
                    fmt='.2f', 
                    cmap='YlOrRd',
                    square=True,
                    cbar_kws={'label': 'Correlation'})
        
        plt.title('Category Correlation Heatmap', fontsize=14, pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'category_correlations.png', dpi=300, bbox_inches='tight')
        plt.close()

    def analyze_seasonal_patterns(self):
        """Analyze seasonal viewing patterns."""
        self.df['Month'] = self.df['Watch Date & Time'].dt.month
        self.df['Year'] = self.df['Watch Date & Time'].dt.year
        
        seasonal_views = self.df.groupby(['Year', 'Month']).size().unstack()
        normalized_views = seasonal_views.div(seasonal_views.sum(axis=1), axis=0)
        
        plt.figure(figsize=(15, 8))
        sns.heatmap(normalized_views, cmap='YlOrRd', annot=True, fmt='.2%')
        plt.title('Seasonal Viewing Patterns (Normalized by Year)')
        plt.xlabel('Month')
        plt.ylabel('Year')
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'seasonal_patterns.png')
        plt.close()

def main():
    project_root = Path(__file__).parent.parent.parent
    data_file = project_root / 'data' / 'processed' / 'youtube_watch_history.csv'
    
    visualizer = YouTubeHistoryVisualizer(data_file)
    
    # Generate all visualizations and stats
    visualizer.generate_basic_stats()
    visualizer.generate_channel_stats()
    visualizer.plot_daily_views()
    visualizer.plot_top_channels()
    visualizer.plot_hourly_distribution()
    visualizer.plot_weekly_patterns()
    visualizer.plot_monthly_trends()
    visualizer.plot_category_distribution()
    visualizer.create_monthly_heatmap()
    visualizer.analyze_category_correlations()
    visualizer.analyze_seasonal_patterns()

if __name__ == "__main__":
    main()
