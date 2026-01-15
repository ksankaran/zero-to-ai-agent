# From: Zero to AI Agent, Chapter 6, Section 6.5
# File: 05_managing_secrets.py


import os
import json
import hashlib
from getpass import getpass

print("🔐 MANAGING SECRETS SECURELY\n")

class SecretManager:
    """Manage application secrets securely"""
    
    def __init__(self):
        self.secrets = {}
        self.load_secrets()
    
    def load_secrets(self):
        """Load secrets from environment variables"""
        # API Keys
        self.secrets['api_keys'] = {
            'openai': os.environ.get('OPENAI_API_KEY'),
            'github': os.environ.get('GITHUB_TOKEN'),
            'stripe': os.environ.get('STRIPE_SECRET_KEY'),
            'sendgrid': os.environ.get('SENDGRID_API_KEY')
        }
        
        # Database credentials
        self.secrets['database'] = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', '5432'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'name': os.environ.get('DB_NAME')
        }
        
        # App secrets
        self.secrets['app'] = {
            'secret_key': os.environ.get('SECRET_KEY'),
            'jwt_secret': os.environ.get('JWT_SECRET'),
            'encryption_key': os.environ.get('ENCRYPTION_KEY')
        }
    
    def get_secret(self, category, key, required=False):
        """Get a secret value safely"""
        value = self.secrets.get(category, {}).get(key)
        
        if required and not value:
            raise ValueError(f"Required secret {category}.{key} is not set!")
        
        return value
    
    def validate_secrets(self):
        """Check that all required secrets are set"""
        print("🔍 Validating Secrets...")
        print("-" * 40)
        
        required_secrets = [
            ('api_keys', 'openai', False),
            ('database', 'host', True),
            ('database', 'port', True),
            ('app', 'secret_key', True)
        ]
        
        all_valid = True
        for category, key, required in required_secrets:
            value = self.get_secret(category, key)
            
            if value:
                # Show masked value
                if len(str(value)) > 8:
                    masked = str(value)[:4] + '***' + str(value)[-4:]
                else:
                    masked = '***'
                status = f"✅ Set ({masked})"
            elif required:
                status = "❌ MISSING (Required!)"
                all_valid = False
            else:
                status = "⚠️  Not set (Optional)"
            
            print(f"{category}.{key}: {status}")
        
        return all_valid
    
    def mask_secret(self, secret):
        """Mask a secret for display"""
        if not secret:
            return None
        
        secret_str = str(secret)
        if len(secret_str) <= 8:
            return '***'
        
        return secret_str[:4] + '***' + secret_str[-4:]

# Demonstrate secret management
manager = SecretManager()

print("="*50)
print("SECRET MANAGEMENT DEMO:")
print("="*50)

# Set some demo secrets
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'
os.environ['SECRET_KEY'] = 'my-super-secret-key-123'
os.environ['OPENAI_API_KEY'] = 'sk-demo-1234567890abcdef'

# Reload with new secrets
manager.load_secrets()

# Validate secrets
if manager.validate_secrets():
    print("\n✅ All required secrets are configured!")
else:
    print("\n❌ Some required secrets are missing!")

# Safe secret usage patterns
print("\n" + "="*50)
print("SAFE SECRET USAGE PATTERNS:")
print("="*50)

print("""
✅ DO:
- Store in environment variables
- Use .env files for development
- Validate on startup
- Mask when displaying
- Rotate regularly
- Use different keys per environment

❌ DON'T:
- Hardcode in source code
- Commit to version control  
- Log or print full values
- Share across environments
- Use default/weak values in production
- Store in plain text files
""")

# Creating a secure configuration file
print("\n" + "="*50)
print("SECURE CONFIGURATION EXAMPLE:")
print("="*50)

def create_secure_config():
    """Create a secure configuration"""
    config = {
        'public': {
            'app_name': 'MySecureApp',
            'version': '1.0.0',
            'environment': os.environ.get('APP_ENV', 'development')
        },
        'private': {
            'api_key': manager.mask_secret(os.environ.get('API_KEY')),
            'db_password': manager.mask_secret(os.environ.get('DB_PASSWORD')),
            'secret_key': manager.mask_secret(os.environ.get('SECRET_KEY'))
        },
        'settings': {
            'debug': os.environ.get('DEBUG', 'False').lower() == 'true',
            'port': int(os.environ.get('PORT', 3000)),
            'max_connections': int(os.environ.get('MAX_CONNECTIONS', 100))
        }
    }
    
    return config

secure_config = create_secure_config()
print("Secure configuration (safe to log):")
print(json.dumps(secure_config, indent=2))
