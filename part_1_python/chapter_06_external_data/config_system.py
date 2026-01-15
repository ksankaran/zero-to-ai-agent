# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: config_system.py

import json
import os

DEFAULT_CONFIG = {
    "app_settings": {
        "theme": "dark",
        "language": "en",
        "auto_save": True,
        "save_interval": 300  # seconds
    },
    "ai_settings": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 1000,
        "api_key": "",  # User needs to add this
        "system_prompt": "You are a helpful assistant."
    },
    "user_preferences": {
        "notifications": True,
        "sound_enabled": True,
        "font_size": 14,
        "recent_files": [],
        "favorite_commands": []
    },
    "advanced": {
        "debug_mode": False,
        "log_level": "info",
        "cache_enabled": True,
        "max_cache_size_mb": 100
    }
}

CONFIG_FILE = "app_config.json"

class ConfigManager:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            print(f"📂 Loading config from {self.config_file}")
            with open(self.config_file, "r") as file:
                loaded = json.load(file)
                # Merge with defaults (in case new settings were added)
                return self._merge_configs(DEFAULT_CONFIG, loaded)
        else:
            print(f"📝 Creating new config file: {self.config_file}")
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default, loaded):
        """Merge loaded config with defaults (keeps new default keys)"""
        merged = default.copy()
        
        def deep_merge(base, overlay):
            for key, value in overlay.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    base[key] = deep_merge(base[key], value)
                else:
                    base[key] = value
            return base
        
        return deep_merge(merged, loaded)
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        with open(self.config_file, "w") as file:
            json.dump(config, file, indent=4)
        print(f"💾 Config saved to {self.config_file}")
    
    def get(self, path, default=None):
        """Get config value using dot notation (e.g., 'ai_settings.model')"""
        keys = path.split(".")
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, path, value):
        """Set config value using dot notation"""
        keys = path.split(".")
        config = self.config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
        self.save_config()
    
    def display_menu(self):
        """Interactive config editor"""
        while True:
            print("\n" + "="*50)
            print("⚙️  CONFIGURATION MANAGER")
            print("="*50)
            print("1. View current config")
            print("2. Edit app settings")
            print("3. Edit AI settings")
            print("4. Edit user preferences")
            print("5. Toggle debug mode")
            print("6. Reset to defaults")
            print("7. Exit")
            
            choice = input("\nChoice: ")
            
            if choice == "1":
                self.view_config()
            elif choice == "2":
                self.edit_app_settings()
            elif choice == "3":
                self.edit_ai_settings()
            elif choice == "4":
                self.edit_preferences()
            elif choice == "5":
                self.toggle_debug()
            elif choice == "6":
                self.reset_config()
            elif choice == "7":
                print("✅ Configuration saved!")
                break
    
    def view_config(self):
        """Display current configuration"""
        print("\n📋 Current Configuration:")
        print(json.dumps(self.config, indent=2))
    
    def edit_app_settings(self):
        """Edit app settings"""
        print("\n🎨 App Settings:")
        print(f"1. Theme: {self.get('app_settings.theme')}")
        print(f"2. Language: {self.get('app_settings.language')}")
        print(f"3. Auto-save: {self.get('app_settings.auto_save')}")
        
        setting = input("\nEdit which setting (1-3)? ")
        
        if setting == "1":
            theme = input("Theme (dark/light): ").lower()
            if theme in ["dark", "light"]:
                self.set("app_settings.theme", theme)
                print(f"✅ Theme set to {theme}")
        elif setting == "2":
            lang = input("Language code (en/es/fr/de): ").lower()
            self.set("app_settings.language", lang)
            print(f"✅ Language set to {lang}")
        elif setting == "3":
            auto = input("Enable auto-save? (yes/no): ").lower() == "yes"
            self.set("app_settings.auto_save", auto)
            print(f"✅ Auto-save {'enabled' if auto else 'disabled'}")
    
    def edit_ai_settings(self):
        """Edit AI settings"""
        print("\n🤖 AI Settings:")
        print(f"1. Model: {self.get('ai_settings.model')}")
        print(f"2. Temperature: {self.get('ai_settings.temperature')}")
        print(f"3. Max tokens: {self.get('ai_settings.max_tokens')}")
        print(f"4. API Key: {'*' * 10 if self.get('ai_settings.api_key') else 'Not set'}")
        
        setting = input("\nEdit which setting (1-4)? ")
        
        if setting == "1":
            model = input("Model name: ")
            self.set("ai_settings.model", model)
            print(f"✅ Model set to {model}")
        elif setting == "2":
            try:
                temp = float(input("Temperature (0.0-1.0): "))
                if 0 <= temp <= 1:
                    self.set("ai_settings.temperature", temp)
                    print(f"✅ Temperature set to {temp}")
            except ValueError:
                print("❌ Invalid temperature")
        elif setting == "3":
            try:
                tokens = int(input("Max tokens: "))
                self.set("ai_settings.max_tokens", tokens)
                print(f"✅ Max tokens set to {tokens}")
            except ValueError:
                print("❌ Invalid number")
        elif setting == "4":
            api_key = input("API Key: ")
            self.set("ai_settings.api_key", api_key)
            print("✅ API key saved")
    
    def edit_preferences(self):
        """Edit user preferences"""
        current_size = self.get("user_preferences.font_size")
        new_size = input(f"Font size (current: {current_size}): ")
        
        try:
            size = int(new_size)
            self.set("user_preferences.font_size", size)
            print(f"✅ Font size set to {size}")
        except ValueError:
            print("❌ Invalid size")
    
    def toggle_debug(self):
        """Toggle debug mode"""
        current = self.get("advanced.debug_mode")
        self.set("advanced.debug_mode", not current)
        print(f"🔧 Debug mode {'enabled' if not current else 'disabled'}")
    
    def reset_config(self):
        """Reset to default configuration"""
        confirm = input("\n⚠️  Reset all settings to defaults? (yes/no): ")
        if confirm.lower() == "yes":
            self.config = DEFAULT_CONFIG.copy()
            self.save_config()
            print("♻️  Configuration reset to defaults")

# Demo the config system
if __name__ == "__main__":
    print("🚀 Advanced Configuration System Demo")
    print("This is how real applications manage settings!\n")
    
    config = ConfigManager()
    
    # Show some examples
    print("\n📖 Example Usage:")
    print(f"Theme: {config.get('app_settings.theme')}")
    print(f"AI Model: {config.get('ai_settings.model')}")
    print(f"Debug Mode: {config.get('advanced.debug_mode')}")
    
    # Interactive menu
    config.display_menu()
