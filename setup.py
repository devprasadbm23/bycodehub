"""
ByCodeHub Complete Setup Script
================================
This script automates the entire setup process:
1. Creates necessary folders
2. Checks dependencies
3. Initializes database
4. Creates default admin user
5. Adds portfolio projects
6. Adds sample testimonials
7. Generates placeholder images

Usage: python setup.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(text):
    """Print step information"""
    print(f"\n📌 {text}")
    print("-"*70)

def check_python_version():
    """Check if Python version is compatible"""
    print_step("Checking Python Version")
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Python 3.8 or higher is required!")
        sys.exit(1)
    else:
        print("   ✅ Python version is compatible")

def create_folder_structure():
    """Create necessary folders"""
    print_step("Creating Folder Structure")
    
    folders = [
        'templates',
        'static',
        'static/css',
        'static/js',
        'static/images',
        'instance'
    ]
    
    for folder in folders:
        path = Path(folder)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"   ✓ Created: {folder}/")
        else:
            print(f"   ⊘ Exists: {folder}/")
    
    print("   ✅ Folder structure ready")

def check_required_files():
    """Check if required files exist"""
    print_step("Checking Required Files")
    
    required_files = {
        'app.py': 'Main Flask application',
        'requirements.txt': 'Python dependencies',
        'templates/index.html': 'Homepage template',
        'static/css/style.css': 'Main stylesheet',
        'static/js/main.js': 'JavaScript file'
    }
    
    missing = []
    for file, description in required_files.items():
        if Path(file).exists():
            print(f"   ✓ Found: {file}")
        else:
            print(f"   ❌ Missing: {file} ({description})")
            missing.append(file)
    
    if missing:
        print(f"\n   ❌ {len(missing)} required file(s) missing!")
        print("   Please ensure all files are in the correct location.")
        return False
    else:
        print("   ✅ All required files present")
        return True

def check_dependencies():
    """Check if required packages are installed"""
    print_step("Checking Python Dependencies")
    
    required_packages = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'flask_mail': 'Flask-Mail',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"   ✓ {name} installed")
        except ImportError:
            print(f"   ❌ {name} not installed")
            missing.append(name)
    
    if missing:
        print(f"\n   ⚠️  {len(missing)} package(s) missing")
        print("   Installing dependencies...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("   ✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("   ❌ Failed to install dependencies")
            print("   Please run: pip install -r requirements.txt")
            return False
    else:
        print("   ✅ All dependencies installed")
    
    return True

def check_env_file():
    """Check if .env file exists and is configured"""
    print_step("Checking Environment Configuration")
    
    env_path = Path('.env')
    
    if not env_path.exists():
        print("   ⚠️  .env file not found")
        print("   Creating template .env file...")
        
        env_template = """# ByCodeHub Environment Configuration
# Generate a secure secret key: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=change-this-to-a-random-secret-key

# Flask Environment
FLASK_ENV=development

# Email Configuration (Gmail)
# Get app password: https://myaccount.google.com/apppasswords
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password-16-chars

# Database (Optional - defaults to SQLite)
# DATABASE_URL=sqlite:///bycodehub.db
"""
        
        with open('.env', 'w') as f:
            f.write(env_template)
        
        print("   ✅ Created .env template file")
        print("   ⚠️  IMPORTANT: Please edit .env and add your credentials!")
        return False
    else:
        print("   ✓ .env file exists")
        
        # Check if configured
        with open('.env', 'r') as f:
            content = f.read()
            
        if 'your-email@gmail.com' in content or 'change-this' in content:
            print("   ⚠️  .env file contains default values")
            print("   Please update with your actual credentials!")
            return False
        else:
            print("   ✅ .env file appears to be configured")
            return True

def initialize_database():
    """Initialize database and create tables"""
    print_step("Initializing Database")
    
    try:
        from app import app, db, Admin
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            # Create tables
            db.create_all()
            print("   ✓ Database tables created")
            
            # Create default admin if not exists
            admin = Admin.query.filter_by(username='admin').first()
            if not admin:
                admin = Admin()
                admin.username = 'admin'
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("   ✓ Default admin user created")
                print("   📝 Username: admin")
                print("   📝 Password: admin123")
                print("   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!")
            else:
                print("   ⊘ Admin user already exists")
            
        print("   ✅ Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ Error initializing database: {str(e)}")
        return False

def populate_portfolio():
    """Add sample portfolio projects"""
    print_step("Populating Portfolio")
    
    try:
        from add_projects import add_portfolio_projects, add_sample_testimonials
        
        print("\n   Adding portfolio projects...")
        add_portfolio_projects()
        
        print("\n   Adding testimonials...")
        add_sample_testimonials()
        
        print("   ✅ Portfolio populated successfully")
        return True
        
    except Exception as e:
        print(f"   ⚠️  Could not populate portfolio: {str(e)}")
        print("   You can run 'python add_projects.py' later")
        return False

def create_images():
    """Create placeholder images"""
    print_step("Creating Placeholder Images")
    
    try:
        from PIL import Image
        from create_images import create_all_placeholders
        
        create_all_placeholders()
        print("   ✅ Images created successfully")
        return True
        
    except ImportError:
        print("   ⚠️  Pillow not installed")
        print("   Install with: pip install Pillow")
        print("   Then run: python create_images.py")
        return False
    except Exception as e:
        print(f"   ⚠️  Could not create images: {str(e)}")
        return False

def display_final_summary():
    """Display setup completion summary"""
    print_header("SETUP COMPLETE! 🎉")
    
    print("\n✅ ByCodeHub is ready to launch!")
    print("\n📋 Quick Start:")
    print("   1. Start the server:")
    print("      python app.py")
    print("\n   2. Open your browser:")
    print("      http://localhost:5000")
    print("\n   3. Admin panel:")
    print("      http://localhost:5000/admin/login")
    print("      Username: admin")
    print("      Password: admin123")
    
    print("\n⚠️  IMPORTANT - Security:")
    print("   1. Change admin password immediately!")
    print("   2. Update .env with your email credentials")
    print("   3. Generate secure SECRET_KEY for production")
    
    print("\n🎨 Customization:")
    print("   1. Replace logo: static/images/logo.png")
    print("   2. Update colors: static/css/style.css")
    print("   3. Edit content: templates/index.html")
    
    print("\n📚 Documentation:")
    print("   - README.md - Complete project documentation")
    print("   - QUICK_SETUP.md - Detailed setup guide")
    print("   - FILE_CHECKLIST.md - File verification list")
    
    print("\n📞 Support:")
    print("   - Check documentation for troubleshooting")
    print("   - Verify all configuration files")
    print("   - Test email functionality")
    
    print("\n" + "="*70)
    print("Happy coding! 🚀")
    print("="*70 + "\n")

def main():
    """Main setup function"""
    print_header("ByCodeHub Setup Wizard")
    print("\nThis script will set up your ByCodeHub platform automatically.")
    print("Please ensure you're in the project root directory.")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Check Python version
    check_python_version()
    
    # Step 2: Create folder structure
    create_folder_structure()
    
    # Step 3: Check required files
    if not check_required_files():
        print("\n❌ Setup cannot continue without required files.")
        sys.exit(1)
    
    # Step 4: Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies and run setup again.")
        sys.exit(1)
    
    # Step 5: Check .env file
    env_configured = check_env_file()
    
    # Step 6: Initialize database
    if not initialize_database():
        print("\n❌ Database initialization failed.")
        sys.exit(1)
    
    # Step 7: Populate portfolio (optional)
    populate_portfolio()
    
    # Step 8: Create images (optional)
    create_images()
    
    # Final summary
    display_final_summary()
    
    if not env_configured:
        print("⚠️  Remember to configure your .env file before starting!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check the error and try again.")
        sys.exit(1)