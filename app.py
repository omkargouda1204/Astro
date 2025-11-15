from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__, 
            static_folder='.',
            static_url_path='',
            template_folder='pages')
            
CORS(app)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
UPLOAD_FOLDER = 'assets/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'avif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Database setup
DATABASE = 'astrology.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Hero slides table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hero_slides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            image TEXT NOT NULL,
            display_order INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Gallery slides table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery_slides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image TEXT NOT NULL,
            display_order INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Business info table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_info (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            business_name TEXT,
            email_address TEXT,
            whatsapp_number TEXT,
            business_address TEXT,
            google_maps_url TEXT,
            google_review_url TEXT,
            facebook_url TEXT,
            instagram_url TEXT,
            twitter_url TEXT,
            youtube_url TEXT,
            linkedin_url TEXT,
            hours_weekday TEXT,
            hours_sunday TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chatbot config table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatbot_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            services TEXT,
            google_maps_url TEXT,
            google_review_url TEXT,
            facebook_url TEXT,
            instagram_url TEXT,
            twitter_url TEXT,
            youtube_url TEXT,
            linkedin_url TEXT,
            hours_weekday TEXT,
            hours_sunday TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            dob TEXT,
            service TEXT NOT NULL,
            booking_date DATE NOT NULL,
            booking_time TIME NOT NULL,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            source TEXT DEFAULT 'Website',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Contact messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Testimonials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS testimonials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER DEFAULT 5,
            review_text TEXT NOT NULL,
            google_account_url TEXT,
            google_place_id TEXT,
            is_selected BOOLEAN DEFAULT 0,
            display_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Admin users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default admin (password: Admin@12)
    password_hash = hashlib.sha256('Admin@12'.encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO admin_users (id, username, password_hash) 
        VALUES (1, 'admin', ?)
    ''', (password_hash,))
    
    # Insert default business info
    cursor.execute('''
        INSERT OR IGNORE INTO business_info (id, business_name, email_address, whatsapp_number) 
        VALUES (1, 'Cosmic Astrology', 'info@cosmicastrology.com', '+91 98765 43210')
    ''')
    
    # Insert default chatbot config
    default_services = json.dumps([
        "Kundali Reading",
        "Tarot Reading",
        "Career Guidance",
        "Love & Relationships",
        "Health Astrology",
        "Financial Forecast",
        "Vastu Consultation",
        "Gemstone Therapy"
    ])
    cursor.execute('''
        INSERT OR IGNORE INTO chatbot_config (id, services) 
        VALUES (1, ?)
    ''', (default_services,))
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Routes for serving HTML pages
@app.route('/')
def index():
    return send_from_directory('pages', 'index.html')

@app.route('/<path:filename>')
def serve_page(filename):
    if filename.endswith('.html'):
        return send_from_directory('pages', filename)
    return send_from_directory('.', filename)

# API Routes

@app.route('/api/hero-slides', methods=['GET'])
def get_hero_slides():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hero_slides WHERE is_active = 1 ORDER BY display_order')
    slides = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'slides': slides})

@app.route('/api/gallery-slides', methods=['GET'])
def get_gallery_slides():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gallery_slides WHERE is_active = 1 ORDER BY display_order')
    slides = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'slides': slides})

@app.route('/api/business-info', methods=['GET'])
def get_business_info():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM business_info WHERE id = 1')
    info = cursor.fetchone()
    conn.close()
    
    if info:
        info_dict = dict(info)
        # Parse social media into object
        info_dict['socialMedia'] = {
            'facebook': info_dict.get('facebook_url'),
            'instagram': info_dict.get('instagram_url'),
            'twitter': info_dict.get('twitter_url'),
            'youtube': info_dict.get('youtube_url'),
            'linkedin': info_dict.get('linkedin_url')
        }
        return jsonify({'success': True, **info_dict})
    return jsonify({'success': False, 'error': 'Business info not found'})

@app.route('/api/chatbot-config', methods=['GET'])
def get_chatbot_config():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chatbot_config WHERE id = 1')
    config = cursor.fetchone()
    conn.close()
    
    if config:
        config_dict = dict(config)
        # Parse services JSON
        if config_dict.get('services'):
            try:
                config_dict['services'] = json.loads(config_dict['services'])
            except:
                config_dict['services'] = []
        return jsonify({'success': True, 'config': config_dict})
    return jsonify({'success': False, 'error': 'Config not found'})

@app.route('/api/chatbot-config', methods=['POST'])
def update_chatbot_config():
    data = request.json
    
    # Convert services array to JSON string
    if 'services' in data and isinstance(data['services'], list):
        data['services'] = json.dumps(data['services'])
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE chatbot_config SET
            services = ?,
            google_maps_url = ?,
            google_review_url = ?,
            facebook_url = ?,
            instagram_url = ?,
            twitter_url = ?,
            youtube_url = ?,
            linkedin_url = ?,
            hours_weekday = ?,
            hours_sunday = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = 1
    ''', (
        data.get('services'),
        data.get('google_maps_url'),
        data.get('google_review_url'),
        data.get('facebook_url'),
        data.get('instagram_url'),
        data.get('twitter_url'),
        data.get('youtube_url'),
        data.get('linkedin_url'),
        data.get('hours_weekday'),
        data.get('hours_sunday')
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Config updated'})

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    
    # Handle both chatbot and contact form submissions
    booking_date = data.get('booking_date') or datetime.now().strftime('%Y-%m-%d')
    booking_time = data.get('booking_time') or '10:00:00'
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, phone, email, dob, service, booking_date, booking_time, notes, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('phone'),
        data.get('email', ''),
        data.get('dob', ''),
        data.get('service') or data.get('topic', 'General Consultation'),
        booking_date,
        booking_time,
        data.get('notes') or data.get('message', ''),
        data.get('source', 'Website')
    ))
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'id': booking_id, 'message': 'Booking created'})

@app.route('/api/contact', methods=['POST'])
def create_contact():
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contact_messages (name, email, phone, subject, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('email'),
        data.get('phone', ''),
        data.get('subject', 'Contact Form'),
        data.get('message')
    ))
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'id': message_id, 'message': 'Message sent'})

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    password = data.get('password')
    
    if not password:
        return jsonify({'success': False, 'error': 'Password required'})
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin_users WHERE password_hash = ?', (password_hash,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        session['admin_logged_in'] = True
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'error': 'Invalid password'})

@app.route('/api/admin/bookings', methods=['GET'])
def get_bookings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings ORDER BY created_at DESC LIMIT 100')
    bookings = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'bookings': bookings})

@app.route('/api/admin/messages', methods=['GET'])
def get_messages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 100')
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'messages': messages})

@app.route('/api/admin/hero-slides', methods=['POST'])
def create_hero_slide():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO hero_slides (title, description, image, display_order)
        VALUES (?, ?, ?, ?)
    ''', (data.get('title'), data.get('description'), data.get('image'), data.get('display_order', 0)))
    conn.commit()
    slide_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': slide_id})

@app.route('/api/admin/gallery-slides', methods=['POST'])
def create_gallery_slide():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO gallery_slides (title, image, display_order)
        VALUES (?, ?, ?)
    ''', (data.get('title'), data.get('image'), data.get('display_order', 0)))
    conn.commit()
    slide_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': slide_id})

@app.route('/api/admin/testimonials', methods=['GET'])
def get_testimonials():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM testimonials ORDER BY created_at DESC')
    testimonials = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'testimonials': testimonials})

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
