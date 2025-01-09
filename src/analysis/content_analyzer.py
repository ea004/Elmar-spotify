from collections import defaultdict
import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
import seaborn as sns
import calendar
import numpy as np

class ContentAnalyzer:
    def __init__(self):
        # Content type patterns and their categories
        self.content_patterns = {
            'Educational': {
                'patterns': [
                    r'how to|tutorial|learn|guide|explained|basics|introduction to|what is|why do|course|lesson',
                    r'tips|tricks|advice|basics|fundamentals|beginners|advanced|masterclass|workshop',
                    r'math|physics|chemistry|biology|programming|coding|algorithm'
                ],
                'keywords': ['tutorial', 'guide', 'learn', 'course', 'education', 'lecture', 'lesson']
            },
            'Gaming': {
                'patterns': [
                    r'gameplay|playthrough|walkthrough|stream|gaming|gamer|play|plays',
                    r'pubg|mobile legends|clash|fortnite|minecraft|gta|fifa|valorant|cs:?go',
                    r'game\s+review|game\s+guide|gaming\s+moments|highlights|tournament',
                    r'#gaming|#game|#gamer|#mobilegaming|#pubgmobile|#bgmi'
                ],
                'keywords': ['game', 'gaming', 'play', 'stream', 'pubg', 'fifa']
            },
            'Entertainment': {
                'patterns': [
                    r'funny|fails|compilation|moments|highlights|best of|montage',
                    r'reaction|reacting|prank|challenge|fun|entertainment|show',
                    r'vlog|daily|life|behind the scenes|bloopers|outtakes'
                ],
                'keywords': ['fun', 'entertainment', 'show', 'vlog']
            },
            'Music': {
                'patterns': [
                    r'official music video|lyrics|audio|live performance|concert|cover|remix|soundtrack',
                    r'instrumental|acoustic|official video|music|song|album|track',
                    r'epic music|orchestral|theme|ost|score|background music'
                ],
                'keywords': ['music', 'song', 'audio', 'sound', 'track']
            },
            'Sports': {
                'patterns': [
                    r'highlights|match|game|tournament|championship|league|vs\.?|versus',
                    r'goals|scores|plays|sports|competition|final|semi-final|quarter-final',
                    r'football|soccer|basketball|tennis|boxing|ufc|mma|wrestling'
                ],
                'keywords': ['sport', 'game', 'match', 'tournament', 'championship']
            },
            'Reviews': {
                'patterns': [
                    r'review|unboxing|first look|hands-on|comparison|vs\.?|versus',
                    r'test|testing|benchmark|analysis|overview|impression',
                    r'worth it\?|should you|better than'
                ],
                'keywords': ['review', 'comparison', 'test', 'analysis']
            },
            'News': {
                'patterns': [
                    r'news|update|latest|breaking|report|coverage|analysis',
                    r'announcement|revealed|exclusive|insider|leak',
                    r'what happened|why|explained|investigation'
                ],
                'keywords': ['news', 'update', 'report', 'coverage']
            },
            'Rankings': {
                'patterns': [
                    r'top\s*\d+|best\s*\d+|\d+\s*best|greatest|worst|ranking',
                    r'compared|versus|vs\.?|comparison|list of|ultimate|definitive',
                    r'most|best|worst|ranked|tier list'
                ],
                'keywords': ['top', 'best', 'ranking', 'list']
            },
            'Shorts': {
                'patterns': [
                    r'#shorts|short video|quick|brief|snippet',
                    r'#short|#tiktok|#reels'
                ],
                'keywords': ['short', 'quick', 'brief']
            },
            'Documentary': {
                'patterns': [
                    r'documentary|history|investigation|story of|behind the scenes',
                    r'exploring|discovery|journey|documentary series',
                    r'real story|true story|what really happened'
                ],
                'keywords': ['documentary', 'history', 'investigation']
            },
            'Tech': {
                'patterns': [
                    r'tech|technology|software|hardware|programming|coding|development',
                    r'computer|digital|online|internet|web|app|application',
                    r'smartphone|gadget|device|review|setup|build'
                ],
                'keywords': ['tech', 'technology', 'software', 'programming']
            },
            'Movies & TV': {
                'patterns': [
                    r'trailer|teaser|preview|episode|season|series',
                    r'movie|film|tv show|television|netflix|amazon prime|disney\+',
                    r'#series|#movie|#film|#tv|#netflix'
                ],
                'keywords': ['movie', 'film', 'tv', 'series', 'show']
            },
            'Russian Content': {
                'patterns': [
                    r'[а-яА-ЯёЁ]',  # Cyrillic characters
                    r'#\w*[а-яА-ЯёЁ]\w*'  # Hashtags with Cyrillic
                ],
                'keywords': []
            }
        }

    def categorize_video(self, title):
        """Categorize a video based on its title."""
        categories = []
        title_lower = title.lower()
        
        # First check for Russian content
        if any(re.search(pattern, title) for pattern in self.content_patterns['Russian Content']['patterns']):
            return ['Russian Content']
        
        # Then check other categories
        for category, data in self.content_patterns.items():
            if category != 'Russian Content':  # Skip Russian content check
                for pattern in data['patterns']:
                    if re.search(pattern, title_lower):
                        categories.append(category)
                        break
                    
        return categories if categories else ['Other']

    def analyze_content(self, df):
        """Analyze content patterns in the dataset."""
        # Initialize results dictionary
        results = {
            'category_counts': defaultdict(int),
            'category_by_month': defaultdict(lambda: defaultdict(int)),
            'common_keywords': defaultdict(int),
            'multi_category_videos': 0
        }

        # Process each video
        for idx, row in df.iterrows():
            categories = self.categorize_video(row['Video Title'])
            
            # Count categories
            for category in categories:
                results['category_counts'][category] += 1
                
                # Count by month
                month = pd.to_datetime(row['Watch Date & Time']).strftime('%Y-%m')
                results['category_by_month'][month][category] += 1
            
            # Count multi-category videos
            if len(categories) > 1:
                results['multi_category_videos'] += 1

            # Extract and count common keywords
            words = row['Video Title'].lower().split()
            for word in words:
                if len(word) > 3:  # Skip very short words
                    results['common_keywords'][word] += 1

        return results

    def generate_visualizations(self, df):
        """Generate visualizations for content analysis."""
        results = self.analyze_content(df)
        
        # Create figures directory if it doesn't exist
        figures_dir = Path(__file__).parent.parent.parent / 'results' / 'figures'
        figures_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Category Distribution
        plt.figure(figsize=(15, 8))
        categories = list(results['category_counts'].keys())
        counts = list(results['category_counts'].values())
        plt.bar(categories, counts)
        plt.title('Distribution of Video Categories')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(figures_dir / 'category_distribution.png')
        plt.close()

        # 2. Category Evolution Over Time
        monthly_data = pd.DataFrame(results['category_by_month']).T
        monthly_data.fillna(0, inplace=True)
        
        plt.figure(figsize=(15, 8))
        monthly_data.plot(kind='area', stacked=True)
        plt.title('Evolution of Video Categories Over Time')
        plt.xlabel('Month')
        plt.ylabel('Number of Videos')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(figures_dir / 'category_evolution.png')
        plt.close()

        # Save analysis results
        stats_dir = Path(__file__).parent.parent.parent / 'results' / 'stats'
        stats_dir.mkdir(parents=True, exist_ok=True)
        
        with open(stats_dir / 'content_analysis.json', 'w') as f:
            # Convert defaultdict to regular dict for JSON serialization
            json_results = {
                'category_counts': dict(results['category_counts']),
                'multi_category_videos': results['multi_category_videos'],
                'top_keywords': dict(sorted(results['common_keywords'].items(), 
                                          key=lambda x: x[1], 
                                          reverse=True)[:100])
            }
            json.dump(json_results, f, indent=4)

    def generate_detailed_analysis(self, df):
        """Generate comprehensive analysis and visualizations."""
        stats_dir = Path(__file__).parent.parent.parent / 'results' / 'stats'
        figures_dir = Path(__file__).parent.parent.parent / 'results' / 'figures'
        
        # Ensure directories exist
        stats_dir.mkdir(parents=True, exist_ok=True)
        figures_dir.mkdir(parents=True, exist_ok=True)

        # 1. Time-based Analysis
        self._analyze_time_patterns(df, stats_dir, figures_dir)
        
        # 2. Content Category Analysis
        self._analyze_categories(df, stats_dir, figures_dir)
        
        # 3. Channel Analysis
        self._analyze_channels(df, stats_dir, figures_dir)
        
        # 4. Trend Analysis
        self._analyze_trends(df, stats_dir, figures_dir)

    def _analyze_time_patterns(self, df, stats_dir, figures_dir):
        """Analyze viewing patterns over time."""
        df['Year'] = pd.to_datetime(df['Watch Date & Time']).dt.year
        df['Month'] = pd.to_datetime(df['Watch Date & Time']).dt.month
        df['Weekday'] = pd.to_datetime(df['Watch Date & Time']).dt.day_name()
        
        # Monthly heatmap data
        monthly_views = df.groupby(['Year', 'Month']).size().unstack()
        
        # Create heatmap
        plt.figure(figsize=(15, 8))
        sns.heatmap(monthly_views, cmap='YlOrRd', annot=True, fmt='g')
        plt.title('Video Viewing Heatmap by Month and Year')
        plt.ylabel('Year')
        plt.xlabel('Month')
        plt.tight_layout()
        plt.savefig(figures_dir / 'monthly_heatmap.png')
        plt.close()

        # Save time-based statistics
        time_stats = {
            'yearly_views': df.groupby('Year').size().to_dict(),
            'monthly_views': df.groupby('Month').size().to_dict(),
            'weekday_views': df.groupby('Weekday').size().to_dict()
        }
        
        pd.DataFrame(time_stats).to_csv(stats_dir / 'time_patterns.csv')

    def _analyze_categories(self, df, stats_dir, figures_dir):
        """Analyze content categories."""
        # Add categories to DataFrame
        df['Categories'] = df['Video Title'].apply(self.categorize_video)
        
        # Explode categories for videos with multiple categories
        categories_df = df.explode('Categories')
        
        # Category counts
        category_counts = categories_df['Categories'].value_counts()
        
        # Create stacked area chart for category evolution
        category_by_date = pd.crosstab(
            pd.to_datetime(categories_df['Watch Date & Time']).dt.to_period('M'),
            categories_df['Categories']
        )
        
        plt.figure(figsize=(15, 8))
        category_by_date.plot(kind='area', stacked=True)
        plt.title('Evolution of Content Categories Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Videos')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(figures_dir / 'category_evolution.png')
        plt.close()

        # Save category statistics
        category_stats = pd.DataFrame({
            'category': category_counts.index,
            'count': category_counts.values,
            'percentage': (category_counts.values / len(df) * 100)
        })
        category_stats.to_csv(stats_dir / 'category_stats.csv', index=False)

    def _analyze_channels(self, df, stats_dir, figures_dir):
        """Analyze channel patterns."""
        # Channel statistics
        channel_stats = df.groupby('Channel Name').agg({
            'Video Title': 'count'
        }).sort_values('Video Title', ascending=False)

        # Top channels visualization
        plt.figure(figsize=(15, 8))
        top_20_channels = channel_stats.head(20)
        sns.barplot(x=top_20_channels.index, y='Video Title', data=top_20_channels)
        plt.xticks(rotation=45, ha='right')
        plt.title('Top 20 Most Watched Channels')
        plt.xlabel('Channel Name')
        plt.ylabel('Number of Videos Watched')
        plt.tight_layout()
        plt.savefig(figures_dir / 'top_channels.png')
        plt.close()

        # Save channel statistics
        channel_stats.to_csv(stats_dir / 'channel_stats.csv')

    def _analyze_trends(self, df, stats_dir, figures_dir):
        """Analyze viewing trends."""
        # Calculate moving averages
        daily_views = df.groupby(pd.to_datetime(df['Watch Date & Time']).dt.date).size()
        ma_7 = daily_views.rolling(window=7).mean()
        ma_30 = daily_views.rolling(window=30).mean()

        # Plot trend lines
        plt.figure(figsize=(15, 8))
        plt.plot(daily_views.index, daily_views, alpha=0.5, label='Daily Views')
        plt.plot(ma_7.index, ma_7, label='7-day Moving Average')
        plt.plot(ma_30.index, ma_30, label='30-day Moving Average')
        plt.title('Viewing Trends Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Videos')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(figures_dir / 'viewing_trends.png')
        plt.close()

        # Save trend statistics
        trend_stats = pd.DataFrame({
            'date': daily_views.index,
            'daily_views': daily_views.values,
            'ma_7': ma_7.values,
            'ma_30': ma_30.values
        })
        trend_stats.to_csv(stats_dir / 'trend_stats.csv', index=False)

def main():
    project_root = Path(__file__).parent.parent.parent
    data_file = project_root / 'data' / 'processed' / 'youtube_watch_history.csv'
    
    df = pd.read_csv(data_file)
    analyzer = ContentAnalyzer()
    analyzer.generate_detailed_analysis(df)

if __name__ == "__main__":
    main() 