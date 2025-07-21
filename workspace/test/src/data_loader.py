"""
Data loading and preprocessing utilities
"""
import pandas as pd
import numpy as np
from pathlib import Path

class DataLoader:
    """Handle data loading and basic preprocessing"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """Load CSV file"""
        file_path = self.data_dir / filename
        return pd.read_csv(file_path)
    
    def basic_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Basic data cleaning"""
        # Remove duplicates
        df_clean = df.drop_duplicates()
        
        # Handle missing values (simple strategy)
        df_clean = df_clean.fillna(df_clean.mean(numeric_only=True))
        
        return df_clean
