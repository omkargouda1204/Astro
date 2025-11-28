-- Migration script for new sections and navbar
-- Run this in your Supabase SQL editor

-- Navbar settings table
CREATE TABLE IF NOT EXISTS navbar_settings (
    id SERIAL PRIMARY KEY,
    logo_url TEXT,
    logo_alt TEXT DEFAULT 'Logo',
    primary_color TEXT DEFAULT '#667eea',
    secondary_color TEXT DEFAULT '#764ba2',
    show_language_dropdown BOOLEAN DEFAULT true,
    phone_number TEXT,
    whatsapp_number TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default navbar settings
INSERT INTO navbar_settings (logo_url, phone_number, whatsapp_number)
VALUES ('', '+91 9876543210', '+91 9876543210')
ON CONFLICT DO NOTHING;

-- Menu items table
CREATE TABLE IF NOT EXISTS menu_items (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    display_order INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT true,
    target TEXT DEFAULT '_self',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default menu items
INSERT INTO menu_items (title, url, display_order, active) VALUES
('Home', '/', 1, true),
('Services', '#services', 2, true),
('Pooja', '#pooja', 3, true),
('About Us', '#about', 4, true),
('Contact', '/contact.html', 5, true),
('Gallery', '#gallery', 6, true),
('Reviews', '#reviews', 7, true)
ON CONFLICT DO NOTHING;

-- Announcement bar table
CREATE TABLE IF NOT EXISTS announcement_bar (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    active BOOLEAN DEFAULT true,
    background_color TEXT DEFAULT '#f59e0b',
    text_color TEXT DEFAULT '#ffffff',
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default announcement
INSERT INTO announcement_bar (text, active, display_order) VALUES
('🌟 Welcome to our Astrology Portal! Book your consultation today 🌟', true, 1),
('📞 24/7 Support Available | Free First Consultation 📞', true, 2)
ON CONFLICT DO NOTHING;

-- Astrological services table
CREATE TABLE IF NOT EXISTS astrological_services (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    icon_url TEXT,
    active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default astrological services
INSERT INTO astrological_services (title, description, icon_url, display_order, active) VALUES
('Horoscope Reading', 'Get detailed insights into your future through personalized horoscope analysis', '', 1, true),
('Palmistry', 'Discover your destiny through the ancient art of palm reading', '', 2, true),
('Numerology', 'Unlock the secrets of numbers and their influence on your life', '', 3, true),
('Face Reading', 'Understand personality traits and future through facial features', '', 4, true),
('Kundali Analysis', 'Comprehensive birth chart analysis for life guidance', '', 5, true),
('Gemstone Guidance', 'Find the perfect gemstone to enhance your fortune', '', 6, true),
('Vaastu Consultation', 'Harmonize your space with ancient Vaastu principles', '', 7, true),
('Match Making', 'Ensure compatibility for a harmonious married life', '', 8, true)
ON CONFLICT DO NOTHING;

-- Pooja services table
CREATE TABLE IF NOT EXISTS pooja_services (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    image_url TEXT,
    active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default pooja services
INSERT INTO pooja_services (title, description, image_url, display_order, active) VALUES
('Ganesh Pooja', 'Remove obstacles and bring prosperity to your home', '', 1, true),
('Lakshmi Pooja', 'Invoke the blessings of Goddess Lakshmi for wealth and abundance', '', 2, true),
('Durga Pooja', 'Seek protection and strength from Goddess Durga', '', 3, true),
('Hanuman Pooja', 'Gain courage and overcome challenges with Lord Hanuman''s blessings', '', 4, true),
('Krishna Pooja', 'Experience divine love and wisdom through Lord Krishna worship', '', 5, true),
('Navagraha Pooja', 'Balance planetary influences for a harmonious life', '', 6, true),
('Rudrabhishek', 'Powerful Shiva worship for spiritual growth and prosperity', '', 7, true),
('Kaal Bhairav Pooja', 'Protection from negative energies and time-related issues', '', 8, true)
ON CONFLICT DO NOTHING;

-- Expert solutions table
CREATE TABLE IF NOT EXISTS expert_solutions (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    image_url TEXT,
    active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default expert solutions
INSERT INTO expert_solutions (title, description, image_url, display_order, active) VALUES
('Love & Marriage Problems', 'Expert guidance for relationship issues, compatibility analysis, and marital harmony. Get personalized solutions for your love life challenges.', '', 1, true),
('Career & Education Issues', 'Strategic astrological insights for career growth, job changes, and educational success. Make informed decisions about your professional life.', '', 2, true),
('Business & Financial Problems', 'Astrological remedies for business growth, financial stability, and wealth creation. Overcome financial obstacles with expert guidance.', '', 3, true),
('Health & Family Challenges', 'Holistic solutions for health concerns and family disputes. Restore harmony and well-being in your personal life.', '', 4, true)
ON CONFLICT DO NOTHING;

-- Create updated_at trigger function if not exists
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
DROP TRIGGER IF EXISTS update_navbar_settings_updated_at ON navbar_settings;
CREATE TRIGGER update_navbar_settings_updated_at BEFORE UPDATE ON navbar_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_menu_items_updated_at ON menu_items;
CREATE TRIGGER update_menu_items_updated_at BEFORE UPDATE ON menu_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_announcement_bar_updated_at ON announcement_bar;
CREATE TRIGGER update_announcement_bar_updated_at BEFORE UPDATE ON announcement_bar FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_astrological_services_updated_at ON astrological_services;
CREATE TRIGGER update_astrological_services_updated_at BEFORE UPDATE ON astrological_services FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_pooja_services_updated_at ON pooja_services;
CREATE TRIGGER update_pooja_services_updated_at BEFORE UPDATE ON pooja_services FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_expert_solutions_updated_at ON expert_solutions;
CREATE TRIGGER update_expert_solutions_updated_at BEFORE UPDATE ON expert_solutions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
