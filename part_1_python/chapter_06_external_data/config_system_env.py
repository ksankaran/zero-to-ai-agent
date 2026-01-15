# From: Zero to AI Agent, Chapter 6, Section 6.5
# File: 04_config_system.py


import os

class Config:
    """Professional configuration management"""

    def __init__(self):
        # Determine environment
        self.ENV = os.environ.get('APP_ENV', 'development')

        # Load appropriate settings
        self.load_config()

    def load_config(self):
        """Load configuration based on environment"""

        # Common settings (all environments)
        self.APP_NAME = os.environ.get('APP_NAME', 'MyApp')
        self.LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

        # Environment-specific settings
        if self.ENV == 'production':
            self.load_production()
        elif self.ENV == 'testing':
            self.load_testing()
        else:
            self.load_development()

    def load_development(self):
        """Development environment settings"""
        self.DEBUG = True
        self.DATABASE_URL = os.environ.get(
            'DATABASE_URL',
            'sqlite:///development.db'
        )
        self.API_KEY = os.environ.get('API_KEY', 'dev-key-placeholder')
        self.SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
        self.PORT = int(os.environ.get('PORT', 3000))
        self.CACHE_ENABLED = False
        self.RATE_LIMIT = 1000  # requests per hour

    def load_production(self):
        """Production environment settings"""
        self.DEBUG = False

        # Required in production
        self.DATABASE_URL = self.get_required('DATABASE_URL')
        self.API_KEY = self.get_required('API_KEY')
        self.SECRET_KEY = self.get_required('SECRET_KEY')

        # Optional with defaults
        self.PORT = int(os.environ.get('PORT', 8080))
        self.CACHE_ENABLED = True
        self.RATE_LIMIT = 100  # requests per hour

    def load_testing(self):
        """Testing environment settings"""
        self.DEBUG = True
        self.DATABASE_URL = 'sqlite:///test.db'
        self.API_KEY = 'test-api-key'
        self.SECRET_KEY = 'test-secret-key'
        self.PORT = 5000
        self.CACHE_ENABLED = False
        self.RATE_LIMIT = 10000  # unlimited for tests

    def get_required(self, key):
        """Get required environment variable or raise error"""
        value = os.environ.get(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set!")
        return value

    def get_bool(self, key, default=False):
        """Get boolean environment variable"""
        value = os.environ.get(key, str(default))
        return value.lower() in ('true', '1', 'yes', 'on')

    def get_int(self, key, default=0):
        """Get integer environment variable"""
        try:
            return int(os.environ.get(key, str(default)))
        except ValueError:
            return default

    def get_list(self, key, default=None):
        """Get list from comma-separated environment variable"""
        value = os.environ.get(key, '')
        if not value:
            return default or []
        return [item.strip() for item in value.split(',')]
    
    def display(self):
        """Display current configuration"""
        print(f"\n🔧 CONFIGURATION ({self.ENV.upper()})")
        print("="*50)
        
        # Display settings (hide sensitive values in production)
        settings = {
            'Environment': self.ENV,
            'Debug': self.DEBUG,
            'Port': self.PORT,
            'Database': self.DATABASE_URL[:20] + '...' if len(self.DATABASE_URL) > 20 else self.DATABASE_URL,
            'API Key': '***' + self.API_KEY[-4:] if self.API_KEY and len(self.API_KEY) > 4 else '***',
            'Cache': self.CACHE_ENABLED,
            'Rate Limit': f"{self.RATE_LIMIT} req/hour"
        }
        
        for key, value in settings.items():
            print(f"{key:15}: {value}")

# Demo the configuration system
print("🎯 PROFESSIONAL CONFIGURATION SYSTEM\n")

# Test different environments
for env in ['development', 'testing', 'production']:
    os.environ['APP_ENV'] = env
    
    # Set some required variables for production
    if env == 'production':
        os.environ['DATABASE_URL'] = 'postgresql://user:pass@host/db'
        os.environ['API_KEY'] = 'sk-prod-key-123456'
        os.environ['SECRET_KEY'] = 'super-secret-production-key'
    
    try:
        config = Config()
        config.display()
    except ValueError as e:
        print(f"\n❌ Configuration error in {env}: {e}")

# Using the config in your application
print("\n" + "="*50)
print("USING CONFIGURATION IN YOUR APP:")
print("="*50)

os.environ['APP_ENV'] = 'development'
config = Config()

print(f"""
# In your application code:
if config.DEBUG:
    print("Debug mode is ON")

api_client = APIClient(key=config.API_KEY)
app.run(port=config.PORT)
""")
