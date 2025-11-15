// Flask API Backend Integration
// This replaces the Supabase backend with Flask API calls

const API_BASE_URL = window.location.origin;

const FlaskAPI = {
    // Hero Slides
    async getHeroSlides() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/hero-slides`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching hero slides:', error);
            return { success: false, error: error.message };
        }
    },

    // Gallery Slides
    async getGallerySlides() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/gallery-slides`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching gallery slides:', error);
            return { success: false, error: error.message };
        }
    },

    // Business Info
    async getBusinessInfo() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/business-info`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching business info:', error);
            return { success: false, error: error.message };
        }
    },

    // Chatbot Config
    async getChatbotConfig() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/chatbot-config`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching chatbot config:', error);
            return { success: false, error: error.message };
        }
    },

    async updateChatbotConfig(configData) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/chatbot-config`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(configData)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error updating chatbot config:', error);
            return { success: false, error: error.message };
        }
    },

    // Bookings / Lead Submission
    async submitLead(leadData) {
        try {
            // Determine if it's a contact message or booking
            const endpoint = leadData.source === 'Contact Form' ? 
                `${API_BASE_URL}/api/contact` : 
                `${API_BASE_URL}/api/bookings`;
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(leadData)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error submitting lead:', error);
            return { success: false, error: error.message };
        }
    },

    // Admin Login
    async verifyAdmin(password) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/admin/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ password })
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error verifying admin:', error);
            return { success: false, error: error.message };
        }
    },

    // Admin - Get Bookings
    async getLeads() {
        try {
            const [bookingsRes, messagesRes] = await Promise.all([
                fetch(`${API_BASE_URL}/api/admin/bookings`),
                fetch(`${API_BASE_URL}/api/admin/messages`)
            ]);
            
            const bookingsData = await bookingsRes.json();
            const messagesData = await messagesRes.json();
            
            // Combine both arrays
            const allLeads = [
                ...(bookingsData.bookings || []),
                ...(messagesData.messages || [])
            ];
            
            return { success: true, leads: allLeads };
        } catch (error) {
            console.error('Error fetching leads:', error);
            return { success: false, error: error.message };
        }
    },

    // Admin - Create Hero Slide
    async createHeroSlide(slideData) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/admin/hero-slides`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(slideData)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error creating hero slide:', error);
            return { success: false, error: error.message };
        }
    },

    // Admin - Create Gallery Slide
    async createGallerySlide(slideData) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/admin/gallery-slides`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(slideData)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error creating gallery slide:', error);
            return { success: false, error: error.message };
        }
    },

    // Admin - Get Testimonials
    async getTestimonials() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/admin/testimonials`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching testimonials:', error);
            return { success: false, error: error.message };
        }
    }
};

// Make FlaskAPI globally available (same interface as SupabaseAPI)
window.SupabaseAPI = FlaskAPI;
window.FlaskAPI = FlaskAPI;

console.log('Flask API backend initialized');
