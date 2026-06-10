"""
Add Portfolio Projects to Database
Run this script once to populate your portfolio with completed projects
Usage: python add_projects.py
"""

from app import app
from extensions import db
from models import Portfolio, Testimonial
from datetime import datetime

def add_portfolio_projects():
    """Add completed projects to the portfolio"""
    
    with app.app_context():
        # Clear existing projects (optional - comment out if you want to keep existing)
        # Portfolio.query.delete()
        # db.session.commit()
        
        projects = [
            {
                'title': 'Agro-Hub – Demand & Price Prediction System',
                'description': 'A comprehensive full-stack application designed for agricultural demand forecasting and price prediction. Built with Python, Flask, MySQL, and Flutter, featuring RESTful APIs for user management, product listings, and order processing. Implements advanced statistical and machine learning techniques for accurate demand and price prediction.',
                'category': 'ml',
                'technologies': 'Python, Flask, MySQL, Flutter, Machine Learning, REST APIs',
                'image_url': '/static/images/agro-hub.jpg'
            },
            {
                'title': 'Maatri Suraksha – Predictive Maternal Health Platform',
                'description': 'A secure, data-driven web application focused on maternal health prediction and monitoring. Developed using Python, Flask, and MongoDB with real-time health data processing APIs. Achieved 86%+ prediction accuracy through quantitative assessment and advanced analytics.',
                'category': 'ml',
                'technologies': 'Python, Flask, MongoDB, Machine Learning, Healthcare Analytics',
                'image_url': '/static/images/maatri-suraksha.jpg'
            },
            {
                'title': 'Demand Forecasting Optimization System',
                'description': 'An advanced analytics project implementing backend forecasting services using Python. Improved prediction accuracy by 22% through sophisticated feature engineering and data analysis. Generates actionable analytical insights to support data-driven business decision-making.',
                'category': 'ml',
                'technologies': 'Python, Data Analytics, Feature Engineering, Forecasting Models',
                'image_url': '/static/images/demand-forecast.jpg'
            },
            {
                'title': 'Juggle.AI – AI SaaS Content Generation Platform',
                'description': 'A cutting-edge AI-powered SaaS platform for automated content generation. Developed comprehensive backend services with third-party API integrations. Supported end-to-end testing, debugging, and performance optimization for enterprise-grade scalability.',
                'category': 'web',
                'technologies': 'Python, AI APIs, Backend Services, Third-party Integrations',
                'image_url': '/static/images/juggle-ai.jpg'
            },
            {
                'title': 'E-Commerce Platform with Payment Gateway',
                'description': 'Full-featured online shopping platform with integrated payment processing. Includes user authentication, product catalog, shopping cart, order management, and secure payment gateway integration. Built with modern web technologies for optimal performance.',
                'category': 'web',
                'technologies': 'Flask, SQLAlchemy, Stripe API, JavaScript, Bootstrap',
                'image_url': '/static/images/ecommerce.jpg'
            },
            {
                'title': 'Hospital Management System',
                'description': 'Comprehensive hospital management application covering patient records, appointment scheduling, billing, and inventory management. Features role-based access control for doctors, nurses, and administrative staff.',
                'category': 'web',
                'technologies': 'Django, PostgreSQL, REST Framework, React',
                'image_url': '/static/images/hospital-mgmt.jpg'
            },
            {
                'title': 'Disease Prediction Using Machine Learning',
                'description': 'ML-based system for early disease detection using patient symptoms and medical history. Implements multiple classification algorithms including Random Forest, SVM, and Neural Networks. Provides probability scores and treatment recommendations.',
                'category': 'ml',
                'technologies': 'Python, Scikit-learn, TensorFlow, Pandas, NumPy',
                'image_url': '/static/images/disease-predict.jpg'
            },
            {
                'title': 'Sentiment Analysis Dashboard',
                'description': 'Real-time sentiment analysis tool for social media monitoring and brand reputation management. Analyzes tweets, reviews, and comments using NLP techniques. Features interactive visualization dashboard.',
                'category': 'ml',
                'technologies': 'Python, NLTK, TextBlob, Flask, Chart.js',
                'image_url': '/static/images/sentiment-analysis.jpg'
            },
            {
                'title': 'Fitness Tracker Android App',
                'description': 'Native Android application for tracking workouts, nutrition, and fitness goals. Features GPS tracking for running/cycling, calorie counter, workout plans, and progress visualization. Integrates with wearable devices.',
                'category': 'android',
                'technologies': 'Java, Android SDK, Firebase, Google Fit API, Material Design',
                'image_url': '/static/images/fitness-tracker.jpg'
            },
            {
                'title': 'Student Attendance System',
                'description': 'Mobile-based attendance management system using QR code scanning and geolocation verification. Includes admin panel for teachers, automated reporting, and parent notification system.',
                'category': 'android',
                'technologies': 'Kotlin, Firebase, Room Database, ZXing Library',
                'image_url': '/static/images/attendance-app.jpg'
            },
            {
                'title': 'Food Delivery Application',
                'description': 'Full-stack food delivery platform with customer app, restaurant dashboard, and delivery partner app. Features real-time order tracking, payment integration, ratings/reviews, and push notifications.',
                'category': 'android',
                'technologies': 'Flutter, Node.js, MongoDB, Google Maps API, Razorpay',
                'image_url': '/static/images/food-delivery.jpg'
            },
            {
                'title': 'Stock Price Prediction System',
                'description': 'Advanced time-series forecasting system for stock market prediction using LSTM neural networks. Includes technical indicators, sentiment analysis, and risk assessment features.',
                'category': 'ml',
                'technologies': 'Python, TensorFlow, Keras, LSTM, Technical Analysis',
                'image_url': '/static/images/stock-predict.jpg'
            },
            {
                'title': 'Library Management System',
                'description': 'Complete library automation system with book cataloging, member management, issue/return tracking, and fine calculation. Features barcode scanning and automated reminder system.',
                'category': 'web',
                'technologies': 'Flask, MySQL, Bootstrap, JavaScript, PDF Generation',
                'image_url': '/static/images/library-mgmt.jpg'
            },
            {
                'title': 'Weather Forecasting App',
                'description': 'Android application providing accurate weather forecasts with beautiful UI. Features hourly/weekly forecasts, weather alerts, multiple location support, and weather maps.',
                'category': 'android',
                'technologies': 'Kotlin, OpenWeatherMap API, Retrofit, Material Design',
                'image_url': '/static/images/weather-app.jpg'
            },
            {
                'title': 'Online Examination Portal',
                'description': 'Secure online examination system with automatic grading, timer functionality, and proctoring features. Includes admin panel for question bank management and result analysis.',
                'category': 'web',
                'technologies': 'Django, PostgreSQL, WebRTC, JavaScript, Chart.js',
                'image_url': '/static/images/exam-portal.jpg'
            }
        ]
        
        # Add projects to database
        added_count = 0
        for project_data in projects:
            # Check if project already exists
            existing = Portfolio.query.filter_by(title=project_data['title']).first()
            if not existing:
                project = Portfolio(**project_data)
                db.session.add(project)
                added_count += 1
                print(f"✓ Added: {project_data['title']}")
            else:
                print(f"⊘ Skipped (already exists): {project_data['title']}")
        
        db.session.commit()
        print(f"\n✅ Successfully added {added_count} new projects to portfolio!")
        print(f"📊 Total projects in database: {Portfolio.query.count()}")


def add_sample_testimonials():
    """Add sample testimonials"""
    
    with app.app_context():
        testimonials = [
            {
                'client_name': 'Rahul Sharma',
                'project_type': 'Machine Learning Project',
                'rating': 5,
                'feedback': 'Excellent work on the demand forecasting system! The team delivered ahead of schedule with perfect documentation. The ML model accuracy exceeded our expectations. Highly recommend for final year projects!',
                'is_approved': True
            },
            {
                'client_name': 'Priya Patel',
                'project_type': 'Web Application',
                'rating': 5,
                'feedback': 'Best decision for my final year project. The e-commerce platform was well-designed with all features working perfectly. Great support throughout the development and even after submission.',
                'is_approved': True
            },
            {
                'client_name': 'Amit Kumar',
                'project_type': 'Android Application',
                'rating': 5,
                'feedback': 'Amazing Android app development! The fitness tracker app has beautiful UI and smooth performance. They understood all my requirements perfectly and delivered a quality product.',
                'is_approved': True
            },
            {
                'client_name': 'Sneha Reddy',
                'project_type': 'Python ML Project',
                'rating': 5,
                'feedback': 'Got my disease prediction project done with 90%+ accuracy. Complete documentation, PPT, and video demo included. Team was very professional and responsive. Worth every penny!',
                'is_approved': True
            },
            {
                'client_name': 'Karthik Iyer',
                'project_type': 'Web Development',
                'rating': 5,
                'feedback': 'The hospital management system was delivered with all features working flawlessly. Clean code, proper database design, and excellent documentation. Impressed with the quality!',
                'is_approved': True
            },
            {
                'client_name': 'Divya Menon',
                'project_type': 'Android App',
                'rating': 5,
                'feedback': 'Student attendance system turned out better than expected! QR code scanning and GPS verification work perfectly. My professors were very impressed. Thank you ByCodeHub!',
                'is_approved': True
            }
        ]
        
        added_count = 0
        for testimonial_data in testimonials:
            # Check if testimonial already exists
            existing = Testimonial.query.filter_by(
                client_name=testimonial_data['client_name']
            ).first()
            
            if not existing:
                testimonial = Testimonial(**testimonial_data)
                db.session.add(testimonial)
                added_count += 1
                print(f"✓ Added testimonial from: {testimonial_data['client_name']}")
            else:
                print(f"⊘ Skipped (already exists): {testimonial_data['client_name']}")
        
        db.session.commit()
        print(f"\n✅ Successfully added {added_count} new testimonials!")
        print(f"📊 Total approved testimonials: {Testimonial.query.filter_by(is_approved=True).count()}")


def display_statistics():
    """Display current database statistics"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("📊 DATABASE STATISTICS")
        print("="*60)
        
        # Portfolio statistics
        total_projects = Portfolio.query.count()
        web_projects = Portfolio.query.filter_by(category='web').count()
        ml_projects = Portfolio.query.filter_by(category='ml').count()
        android_projects = Portfolio.query.filter_by(category='android').count()
        
        print(f"\n📁 PORTFOLIO:")
        print(f"   Total Projects: {total_projects}")
        print(f"   - Web Applications: {web_projects}")
        print(f"   - Machine Learning: {ml_projects}")
        print(f"   - Android Apps: {android_projects}")
        
        # Testimonial statistics
        total_testimonials = Testimonial.query.count()
        approved_testimonials = Testimonial.query.filter_by(is_approved=True).count()
        
        print(f"\n⭐ TESTIMONIALS:")
        print(f"   Total: {total_testimonials}")
        print(f"   Approved: {approved_testimonials}")
        
        # Submission statistics
        from models import Submission
        total_submissions = Submission.query.count()
        pending = Submission.query.filter_by(status='pending').count()
        in_progress = Submission.query.filter_by(status='in_progress').count()
        completed = Submission.query.filter_by(status='completed').count()
        
        print(f"\n📋 SUBMISSIONS:")
        print(f"   Total: {total_submissions}")
        print(f"   - Pending: {pending}")
        print(f"   - In Progress: {in_progress}")
        print(f"   - Completed: {completed}")
        
        print("\n" + "="*60)


if __name__ == '__main__':
    print("🚀 Starting Portfolio Database Population...")
    print("="*60)
    
    # Add portfolio projects
    print("\n📁 Adding Portfolio Projects...")
    print("-"*60)
    add_portfolio_projects()
    
    # Add testimonials
    print("\n" + "-"*60)
    print("⭐ Adding Sample Testimonials...")
    print("-"*60)
    add_sample_testimonials()
    
    # Display statistics
    display_statistics()
    
    print("\n✅ Database population completed successfully!")
    print("\n💡 Next steps:")
    print("   1. Run your Flask app: python app.py")
    print("   2. Visit: http://localhost:5000")
    print("   3. Check portfolio page: http://localhost:5000/portfolio")
    print("   4. View admin dashboard: http://localhost:5000/admin/login")
    print("\n🎉 Your ByCodeHub platform is ready to go!")