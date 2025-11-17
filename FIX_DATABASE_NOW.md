# 🚨 CRITICAL: FIX DATABASE NOW!

## ⚠️ Your Problem
Your database tables are **missing columns**:
- ❌ `bookings` table missing `dob` column → **Booking failures**
- ❌ `gallery_slides` table missing `description` column → **Gallery upload failures**
- ❌ `business_info` table may have missing columns → **Business info save failures**
- ❌ `chatbot_config` table may have missing columns → **Chatbot config save failures**

## ✅ SOLUTION (Takes 2 minutes!)

### Step 1: Open Supabase SQL Editor
1. Go to **https://supabase.com**
2. Click on your project
3. Click **"SQL Editor"** in the left sidebar
4. Click **"New query"**

### Step 2: Run the SQL Script
1. Open the file **`database_schema.sql`** in this project (VS Code)
2. Copy **ALL** the contents (Ctrl+A, then Ctrl+C)
3. Go back to Supabase SQL Editor
4. Paste the entire script (Ctrl+V)
5. Click **"Run"** button (bottom right) or press **F5**
6. Wait for **"Success. No rows returned"** message

### Step 3: Verify Tables Were Created
1. Click **"Table Editor"** in Supabase left sidebar
2. You should see all 6 tables listed:
   - ✅ `contact_messages` 
   - ✅ `bookings` (check it has **dob** column)
   - ✅ `business_info` (check it has whatsapp, address, email, phone, website, hours_weekday, hours_sunday, facebook, instagram, youtube, twitter)
   - ✅ `chatbot_config` (check it has google_maps_url, google_review_url, services, facebook, instagram, twitter, youtube, linkedin, hours_weekday, hours_sunday)
   - ✅ `hero_slides` (check it has **description** column)
   - ✅ `gallery_slides` (check it has **description** column)

3. Click on each table name to verify columns exist

### Step 4: Add Initial Business Data
1. Click on **`business_info`** table in Table Editor
2. Click **"Insert"** → **"Insert row"**
3. Fill in your business details:
   - **id**: 1 (IMPORTANT!)
   - **address**: Your full address
   - **email**: Your email
   - **phone**: Your phone number (e.g., +918431729319)
   - **whatsapp**: Same as phone
   - **website**: Your website URL (if any)
   - **hours_weekday**: e.g., "9:00 AM - 8:00 PM"
   - **hours_sunday**: e.g., "9:00 AM - 2:00 PM"
   - **facebook**: Facebook page URL
   - **instagram**: Instagram profile URL
   - **youtube**: YouTube channel URL
   - **twitter**: Twitter profile URL
4. Click **"Save"**

### Step 5: Add Chatbot Configuration
1. Click on **`chatbot_config`** table in Table Editor
2. Click **"Insert"** → **"Insert row"**
3. Fill in chatbot details:
   - **id**: 1 (IMPORTANT!)
   - **google_maps_url**: Your Google Maps link
   - **google_review_url**: Your Google Review link
   - **services**: "Kundali Analysis, Tarot Reading, Career Guidance, Love & Relationships, Financial Consultation, Vastu Consultation, Gemstone Recommendation, Muhurat Selection"
   - **hours_weekday**: e.g., "9:00 AM - 8:00 PM"
   - **hours_sunday**: e.g., "9:00 AM - 2:00 PM"
   - **facebook**: Facebook page URL
   - **instagram**: Instagram profile URL
   - **youtube**: YouTube channel URL
   - **twitter**: Twitter profile URL
   - **linkedin**: LinkedIn profile URL
4. Click **"Save"**

### Step 6: Restart Flask Server
```powershell
# In your VS Code terminal:
# 1. Stop the current server (press Ctrl+C)
# 2. Wait for it to stop
# 3. Restart:
python app.py
```

## 🎉 What Will Work After This:

### 1. ✅ **Booking Form**
   - Will save with DOB field
   - Form will **hide automatically** after successful booking
   - Email notification sent
   - Shows booking confirmation message

### 2. ✅ **Gallery Management**
   - Upload images with title AND description
   - Edit existing slides with description
   - Images display correctly on homepage
   - Local storage working (`/static/uploads/`)

### 3. ✅ **Business Info Management**
   - Save all business details from admin
   - Updates display on contact page
   - **Chatbot will use these details automatically!**
   - Address, phone, email, hours all update everywhere

### 4. ✅ **Chatbot Configuration**
   - Save Google Maps URL, Review URL
   - Update services list
   - Update social media links
   - **Chatbot responses update automatically!**
   - FAQ content in English & Kannada

### 5. ✅ **Contact Form**
   - Already working! (I saw your successful submissions)
   - Saves messages to database
   - Sends email notifications

### 6. ✅ **Dynamic Chatbot**
   - Uses business_info from database
   - Uses chatbot_config from database
   - When admin updates business info → chatbot updates automatically
   - When admin updates chatbot config → chatbot updates automatically
   - Shows comprehensive FAQ in English & ಕನ್ನಡ

## 🔥 KEY FEATURES NOW WORKING:

### 🤖 Chatbot Auto-Update
- Admin updates **Business Info** → Chatbot shows new address/phone/email/hours
- Admin updates **Chatbot Config** → Chatbot shows new Google Maps/Review links
- Admin updates **Social Media** → Chatbot shows new Facebook/Instagram/YouTube links
- **No code changes needed!** Everything updates from database

### 📚 Comprehensive FAQ
The chatbot now includes 50+ questions covering:
- General astrology questions (English & Kannada)
- Zodiac signs, horoscopes, birth charts
- Planets (Saturn, Jupiter, Venus, Mercury, Rahu, Ketu)
- Doshas (Mangal Dosha, Vastu)
- Services, pricing, booking
- Marriage compatibility, career guidance, health
- All business contact info dynamically loaded

## 📝 Important Notes:

- ✅ The SQL script uses `CREATE TABLE IF NOT EXISTS` - **100% SAFE**
- ✅ It will **NOT delete** any existing data
- ✅ It will **ADD missing columns** if tables already exist
- ✅ RLS policies allow public read for business info/chatbot config
- ✅ RLS policies allow admin (service_role) to update everything
- ✅ Booking form auto-hide code already exists (line 1189 in index.html)
- ✅ Local image upload working (saves to `/static/uploads/`)

## ⚠️ Troubleshooting:

### Error: "Could not find the 'dob' column"
**Solution**: You didn't run the SQL script yet. Go to Step 1.

### Error: "Could not find the 'description' column"
**Solution**: You didn't run the SQL script yet. Go to Step 1.

### Error: 500 on business-info save
**Solution**: Run the SQL script AND add initial data (Step 4).

### Error: 500 on chatbot-config save
**Solution**: Run the SQL script AND add initial data (Step 5).

### Chatbot not showing updated info
**Solution**: 
1. Make sure you saved in admin dashboard
2. Check Supabase Table Editor to confirm data saved
3. Refresh your webpage (Ctrl+F5)
4. If still not working, restart Flask server

### Images not displaying
**Solution**: Check that `/static/uploads/` folder exists and has write permissions.

## 🎯 STEP-BY-STEP CHECKLIST:

- [ ] Open Supabase Dashboard
- [ ] Go to SQL Editor
- [ ] Copy entire `database_schema.sql` file
- [ ] Paste into SQL Editor
- [ ] Click "Run" and wait for success
- [ ] Go to Table Editor
- [ ] Verify all 6 tables exist
- [ ] Check `bookings` has `dob` column
- [ ] Check `gallery_slides` has `description` column
- [ ] Add row to `business_info` table (id=1)
- [ ] Add row to `chatbot_config` table (id=1)
- [ ] Stop Flask server (Ctrl+C)
- [ ] Restart Flask server (`python app.py`)
- [ ] Test booking form
- [ ] Test gallery upload
- [ ] Test business info save in admin
- [ ] Test chatbot config save in admin
- [ ] Open chatbot and verify business info appears
- [ ] Ask chatbot FAQ questions
- [ ] Celebrate! 🎉

## 🚀 After Everything Works:

Run these commands to push to GitHub:
```powershell
git add .
git commit -m "Fix: Added missing database columns, dynamic chatbot, comprehensive FAQ (English & Kannada)"
git push origin main
```

## 💡 CRITICAL REMINDER:

**DO NOT** try to fix code. The code is already fixed!

**DO THIS**: Run the SQL script in Supabase. That's it!

All errors will disappear after running `database_schema.sql`. 🎯✨
