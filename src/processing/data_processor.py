from lxml import etree
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

class YouTubeHistoryProcessor:
    def __init__(self):
        self.month_translation = {
            'января': 'January', 'февраля': 'February', 'марта': 'March',
            'апреля': 'April', 'мая': 'May', 'июня': 'June',
            'июля': 'July', 'августа': 'August', 'сентября': 'September',
            'октября': 'October', 'ноября': 'November', 'декабря': 'December',
            'янв.': 'January', 'февр.': 'February', 'мар.': 'March',
            'апр.': 'April', 'май': 'May', 'июн.': 'June',
            'июл.': 'July', 'авг.': 'August', 'сен.': 'September',
            'окт.': 'October', 'нояб.': 'November', 'дек.': 'December'
        }

    def convert_russian_date(self, russian_date):
        """Convert a Russian date string to a proper datetime format."""
        try:
            russian_date = russian_date.replace('\u202f', ' ').strip().replace('г.', '').strip()
            parts = russian_date.split(' ')
            if len(parts) < 3:
                return None
            
            day, month_russian, year = parts[0], parts[1], parts[2]
            month_english = self.month_translation.get(month_russian.lower(), month_russian)
            english_date_str = f"{day} {month_english} {year}"
            return datetime.strptime(english_date_str, "%d %B %Y")
        except Exception as e:
            print(f"Error converting date: {e}")
            return None

    def process_history(self, input_file, output_file):
        """Process YouTube history from HTML to CSV."""
        # Read HTML file
        with open(input_file, 'r', encoding='utf-8') as file:
            html_data = file.read()

        # Parse HTML
        tree = etree.HTML(html_data)
        data = []

        # Extract data
        for div in tree.xpath('//div[contains(@class, "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")]'):
            video_title = div.xpath('.//a[1]/text()')
            channel_name = div.xpath('.//a[2]/text()')
            watch_date_time = div.xpath('.//text()[2]')

            video_title = video_title[0].strip() if video_title else 'Unknown Title'
            channel_name = channel_name[0].strip() if channel_name else 'Unknown Channel'
            watch_date_time = watch_date_time[0].strip() if watch_date_time else 'Unknown Date'
            watch_date_time = self.convert_russian_date(watch_date_time)

            data.append({
                'Video Title': video_title,
                'Channel Name': channel_name,
                'Watch Date & Time': watch_date_time
            })

        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Filter invalid entries
        df = df[
            (df['Video Title'] != 'Unknown Title') & 
            (df['Channel Name'] != 'Unknown Channel') & 
            (df['Watch Date & Time'].notna())
        ]

        # Save to CSV
        df.to_csv(output_file, index=False)
        return df

def main():
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Set up file paths
    input_file = project_root / 'data' / 'raw' / 'watch_history.html'
    output_file = project_root / 'data' / 'processed' / 'youtube_watch_history.csv'

    # Process data
    processor = YouTubeHistoryProcessor()
    df = processor.process_history(input_file, output_file)
    print("Data processing completed successfully!")
    print("\nFirst few rows of processed data:")
    print(df.head())

if __name__ == "__main__":
    main()
