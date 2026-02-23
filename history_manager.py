"""
History Management for Prompt Generator AI Agent
Handles saving, loading, and managing prompt history
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from config import Config


class HistoryManager:
    """Manages prompt history and favorites"""
    
    def __init__(self):
        self.history_file = Config.history_file
        self.favorites_file = Config.favorites_file
        self._ensure_data_directory()
        self._initialize_files()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
    
    def _initialize_files(self):
        """Initialize history and favorites files if they don't exist"""
        if not os.path.exists(self.history_file):
            self._save_json(self.history_file, [])
        
        if not os.path.exists(self.favorites_file):
            self._save_json(self.favorites_file, [])
    
    def _save_json(self, filepath: str, data: any):
        """Save data to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_json(self, filepath: str) -> any:
        """Load data from JSON file"""
        if not os.path.exists(filepath):
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_prompt(self, prompt_data: Dict) -> bool:
        """Save a generated prompt to history"""
        try:
            history = self._load_json(self.history_file)
            
            # Add to beginning of list
            history.insert(0, {
                'id': prompt_data['id'],
                'timestamp': prompt_data['timestamp'],
                'user_input': prompt_data['user_input'],
                'generated_prompt': prompt_data['generated_prompt'],
                'config': prompt_data['config']
            })
            
            # Limit history size
            if len(history) > Config.max_history_items:
                history = history[:Config.max_history_items]
            
            self._save_json(self.history_file, history)
            return True
        
        except Exception as e:
            print(f"Error saving prompt: {e}")
            return False
    
    def get_history(self) -> List[Dict]:
        """Retrieve all prompt history"""
        return self._load_json(self.history_file)
    
    def get_prompt_by_id(self, prompt_id: str) -> Optional[Dict]:
        """Get a specific prompt by ID"""
        history = self._load_json(self.history_file)
        
        for item in history:
            if item.get('id') == prompt_id:
                return item
        
        return None
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt from history"""
        try:
            history = self._load_json(self.history_file)
            history = [item for item in history if item.get('id') != prompt_id]
            self._save_json(self.history_file, history)
            return True
        
        except Exception as e:
            print(f"Error deleting prompt: {e}")
            return False
    
    def clear_history(self) -> bool:
        """Clear all history"""
        try:
            self._save_json(self.history_file, [])
            return True
        
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
    
    def save_favorite(self, prompt: str, note: str = "") -> bool:
        """Save a prompt to favorites"""
        try:
            favorites = self._load_json(self.favorites_file)
            
            favorite = {
                'id': str(datetime.now().timestamp()),
                'prompt': prompt,
                'note': note,
                'created_at': datetime.now().isoformat()
            }
            
            favorites.insert(0, favorite)
            self._save_json(self.favorites_file, favorites)
            return True
        
        except Exception as e:
            print(f"Error saving favorite: {e}")
            return False
    
    def get_favorites(self) -> List[Dict]:
        """Retrieve all favorites"""
        return self._load_json(self.favorites_file)
    
    def delete_favorite(self, favorite_id: str) -> bool:
        """Delete a favorite"""
        try:
            favorites = self._load_json(self.favorites_file)
            favorites = [f for f in favorites if f.get('id') != favorite_id]
            self._save_json(self.favorites_file, favorites)
            return True
        
        except Exception as e:
            print(f"Error deleting favorite: {e}")
            return False
    
    def search_history(self, query: str) -> List[Dict]:
        """Search history for prompts matching query"""
        history = self._load_json(self.history_file)
        query_lower = query.lower()
        
        results = []
        for item in history:
            # Search in user input and generated prompt
            if (query_lower in item.get('user_input', '').lower() or 
                query_lower in item.get('generated_prompt', '').lower()):
                results.append(item)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        history = self._load_json(self.history_file)
        
        return {
            'total_prompts': len(history),
            'favorites_count': len(self._load_json(self.favorites_file)),
            'models_used': self._get_model_distribution(history),
            'complexity_distribution': self._get_complexity_distribution(history)
        }
    
    def _get_model_distribution(self, history: List[Dict]) -> Dict:
        """Get distribution of models used"""
        models = {}
        for item in history:
            model = item.get('config', {}).get('model', 'Unknown')
            models[model] = models.get(model, 0) + 1
        return models
    
    def _get_complexity_distribution(self, history: List[Dict]) -> Dict:
        """Get distribution of complexity levels"""
        complexities = {}
        for item in history:
            complexity = item.get('config', {}).get('complexity', 'Unknown')
            complexities[complexity] = complexities.get(complexity, 0) + 1
        return complexities
    
    def export_history(self, format: str = 'json') -> str:
        """Export history in specified format"""
        history = self._load_json(self.history_file)
        
        if format == 'json':
            return json.dumps(history, indent=2, ensure_ascii=False)
        
        elif format == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            if history:
                writer = csv.DictWriter(output, fieldnames=history[0].keys())
                writer.writeheader()
                writer.writerows(history)
            
            return output.getvalue()
        
        else:
            return str(history)