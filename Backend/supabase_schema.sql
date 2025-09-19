-- Supabase Database Schema for FarmersHub
-- This file contains the complete database schema for the Kerala Farming Assistant

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    preferred_language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Farms table
CREATE TABLE farms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    location JSONB NOT NULL, -- {district, state, coordinates, address}
    total_area DECIMAL(10,2) NOT NULL, -- in acres
    soil_type VARCHAR(100) NOT NULL,
    soil_ph DECIMAL(3,1) NOT NULL,
    soil_nutrients JSONB NOT NULL, -- {nitrogen, phosphorus, potassium, organic_matter}
    irrigation_type VARCHAR(50) NOT NULL,
    farming_type VARCHAR(50) NOT NULL, -- organic, conventional, mixed, natural
    established_year INTEGER NOT NULL,
    contact_info JSONB NOT NULL, -- {phone, email, address}
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crops table
CREATE TABLE crops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID REFERENCES farms(id) ON DELETE CASCADE,
    crop_name VARCHAR(100) NOT NULL,
    planting_date DATE NOT NULL,
    expected_harvest DATE NOT NULL,
    area_acres DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'planted', -- planted, growing, harvested
    yield_actual DECIMAL(10,2), -- in kg
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Disease detections table
CREATE TABLE disease_detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID REFERENCES farms(id) ON DELETE CASCADE,
    crop_id UUID REFERENCES crops(id) ON DELETE SET NULL,
    image_url TEXT NOT NULL,
    disease_name VARCHAR(255) NOT NULL,
    confidence_score DECIMAL(5,2) NOT NULL, -- 0-100
    treatment_applied TEXT,
    detection_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Soil tests table
CREATE TABLE soil_tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID REFERENCES farms(id) ON DELETE CASCADE,
    ph_level DECIMAL(3,1) NOT NULL,
    nitrogen DECIMAL(8,2) NOT NULL, -- kg/ha
    phosphorus DECIMAL(8,2) NOT NULL, -- kg/ha
    potassium DECIMAL(8,2) NOT NULL, -- kg/ha
    organic_matter DECIMAL(5,2) NOT NULL, -- %
    carbon_content DECIMAL(5,2) NOT NULL, -- %
    bulk_density DECIMAL(5,2) NOT NULL, -- g/cm³
    water_holding_capacity DECIMAL(5,2) NOT NULL, -- %
    cation_exchange_capacity DECIMAL(5,2) NOT NULL, -- cmol/kg
    micronutrients JSONB NOT NULL, -- {zinc, iron, manganese, copper, boron}
    soil_texture VARCHAR(50) NOT NULL,
    soil_color VARCHAR(50) NOT NULL,
    drainage VARCHAR(50) NOT NULL,
    erosion_level VARCHAR(50) NOT NULL,
    lab_name VARCHAR(255) NOT NULL,
    test_date DATE NOT NULL,
    recommendations TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Market prices table
CREATE TABLE market_prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_name VARCHAR(100) NOT NULL,
    market_location VARCHAR(255) NOT NULL,
    price_per_kg DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL,
    source VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat sessions table
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    messages JSONB NOT NULL DEFAULT '[]', -- Array of message objects
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Government schemes table
CREATE TABLE government_schemes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL, -- Income Support, Crop Insurance, Credit, etc.
    eligibility_criteria JSONB NOT NULL, -- Criteria for eligibility
    benefits JSONB NOT NULL, -- Array of benefits
    application_process JSONB NOT NULL, -- Array of steps
    required_documents JSONB NOT NULL, -- Array of required documents
    contact_info JSONB NOT NULL, -- Contact information
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Community questions table
CREATE TABLE community_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    tags TEXT[] DEFAULT '{}',
    answers JSONB DEFAULT '[]', -- Array of answer objects
    votes INTEGER DEFAULT 0,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Weather data table
CREATE TABLE weather_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location VARCHAR(255) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    humidity DECIMAL(5,2) NOT NULL,
    pressure DECIMAL(8,2) NOT NULL,
    wind_speed DECIMAL(5,2) NOT NULL,
    description VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Farm analytics table
CREATE TABLE farm_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID REFERENCES farms(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    metric_unit VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_farms_user_id ON farms(user_id);
CREATE INDEX idx_crops_farm_id ON crops(farm_id);
CREATE INDEX idx_disease_detections_farm_id ON disease_detections(farm_id);
CREATE INDEX idx_disease_detections_crop_id ON disease_detections(crop_id);
CREATE INDEX idx_soil_tests_farm_id ON soil_tests(farm_id);
CREATE INDEX idx_market_prices_crop_name ON market_prices(crop_name);
CREATE INDEX idx_market_prices_date ON market_prices(date);
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_community_questions_user_id ON community_questions(user_id);
CREATE INDEX idx_community_questions_category ON community_questions(category);
CREATE INDEX idx_weather_data_location ON weather_data(location);
CREATE INDEX idx_weather_data_date ON weather_data(date);
CREATE INDEX idx_farm_analytics_farm_id ON farm_analytics(farm_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_farms_updated_at BEFORE UPDATE ON farms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON chat_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_community_questions_updated_at BEFORE UPDATE ON community_questions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample government schemes
INSERT INTO government_schemes (name, description, category, eligibility_criteria, benefits, application_process, required_documents, contact_info) VALUES
('PM-KISAN Scheme', 'Direct income support to farmers', 'Income Support', 
 '{"land_holding_max": 2, "annual_income_max": 100000, "aadhaar_required": true}',
 '["₹6000 per year in 3 installments", "Direct bank transfer", "No middlemen"]',
 '["Register on PM-KISAN portal", "Submit land documents", "Link bank account", "Wait for verification"]',
 '["Aadhaar card", "Land documents", "Bank account details", "Mobile number"]',
 '{"website": "https://pmkisan.gov.in", "helpline": "18001155266"}'),

('Pradhan Mantri Fasal Bima Yojana', 'Crop insurance scheme', 'Crop Insurance',
 '{"all_farmers": true, "crop_coverage": "all_crops", "seasonal_coverage": "all_seasons"}',
 '["Premium subsidy up to 90%", "Quick claim settlement", "Weather-based insurance"]',
 '["Contact insurance company", "Submit application", "Pay premium", "Get policy document"]',
 '["Land documents", "Bank account details", "Aadhaar card", "Crop details"]',
 '{"website": "https://pmfby.gov.in", "helpline": "18001155266"}'),

('Soil Health Card Scheme', 'Free soil testing for farmers', 'Soil Testing',
 '{"all_farmers": true, "land_holding": "any_size", "state": "Kerala"}',
 '["Free soil testing", "Nutrient recommendations", "Fertilizer advice"]',
 '["Visit agriculture office", "Submit application", "Soil sample collection", "Get results"]',
 '["Land documents", "Aadhaar card", "Mobile number"]',
 '{"website": "https://soilhealth.dac.gov.in", "helpline": "18001155266"}'),

('Paramparagat Krishi Vikas Yojana', 'Organic farming promotion', 'Organic Farming',
 '{"group_size_min": 50, "land_holding_min": 0.4, "organic_certification": false}',
 '["₹50000 per hectare for 3 years", "Organic certification support", "Training programs"]',
 '["Form farmer group", "Submit proposal", "Get approval", "Start organic farming"]',
 '["Group formation documents", "Land documents", "Bank account details"]',
 '{"website": "https://pgsindia-ncof.gov.in", "helpline": "18001155266"}');

-- Insert sample market prices for Kerala crops
INSERT INTO market_prices (crop_name, market_location, price_per_kg, date, source) VALUES
('Rice', 'Thiruvananthapuram', 25.50, CURRENT_DATE, 'Kerala State Civil Supplies'),
('Coconut', 'Kochi', 8.75, CURRENT_DATE, 'Kerala Coconut Development Board'),
('Black Pepper', 'Kozhikode', 450.00, CURRENT_DATE, 'Spices Board India'),
('Cardamom', 'Idukki', 1200.00, CURRENT_DATE, 'Spices Board India'),
('Rubber', 'Kottayam', 180.00, CURRENT_DATE, 'Rubber Board India'),
('Tea', 'Munnar', 120.00, CURRENT_DATE, 'Tea Board India'),
('Coffee', 'Wayanad', 280.00, CURRENT_DATE, 'Coffee Board India'),
('Banana', 'Thrissur', 15.00, CURRENT_DATE, 'Kerala Horticulture Department'),
('Ginger', 'Kannur', 85.00, CURRENT_DATE, 'Spices Board India'),
('Turmeric', 'Kozhikode', 65.00, CURRENT_DATE, 'Spices Board India');

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE farms ENABLE ROW LEVEL SECURITY;
ALTER TABLE crops ENABLE ROW LEVEL SECURITY;
ALTER TABLE disease_detections ENABLE ROW LEVEL SECURITY;
ALTER TABLE soil_tests ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_questions ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (basic policies - adjust based on your auth requirements)
CREATE POLICY "Users can view own data" ON users FOR SELECT USING (auth.uid()::text = id::text);
CREATE POLICY "Users can update own data" ON users FOR UPDATE USING (auth.uid()::text = id::text);

CREATE POLICY "Users can view own farms" ON farms FOR SELECT USING (auth.uid()::text = user_id::text);
CREATE POLICY "Users can insert own farms" ON farms FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);
CREATE POLICY "Users can update own farms" ON farms FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can view own crops" ON crops FOR SELECT USING (farm_id IN (SELECT id FROM farms WHERE user_id::text = auth.uid()::text));
CREATE POLICY "Users can insert own crops" ON crops FOR INSERT WITH CHECK (farm_id IN (SELECT id FROM farms WHERE user_id::text = auth.uid()::text));
CREATE POLICY "Users can update own crops" ON crops FOR UPDATE USING (farm_id IN (SELECT id FROM farms WHERE user_id::text = auth.uid()::text));

CREATE POLICY "Users can view own disease detections" ON disease_detections FOR SELECT USING (farm_id IN (SELECT id FROM farms WHERE user_id::text = auth.uid()::text));
CREATE POLICY "Users can insert own disease detections" ON disease_detections FOR INSERT WITH CHECK (farm_id IN (SELECT id FROM farms WHERE user_id::text = auth.uid()::text));

CREATE POLICY "Users can view own soil tests" ON soil_tests FOR SELECT USING (farm_id IN (SELECT id FROM farms WHERE user_id::text = auth.uid()::text));
CREATE POLICY "Users can insert own soil tests" ON soil_tests FOR INSERT WITH CHECK (farm_id IN (SELECT id FROM farms WHERE user_id::text = auth.uid()::text));

CREATE POLICY "Users can view own chat sessions" ON chat_sessions FOR SELECT USING (auth.uid()::text = user_id::text);
CREATE POLICY "Users can insert own chat sessions" ON chat_sessions FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);
CREATE POLICY "Users can update own chat sessions" ON chat_sessions FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can view own community questions" ON community_questions FOR SELECT USING (auth.uid()::text = user_id::text);
CREATE POLICY "Users can insert own community questions" ON community_questions FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);
CREATE POLICY "Users can update own community questions" ON community_questions FOR UPDATE USING (auth.uid()::text = user_id::text);

-- Public read access for market prices, government schemes, and weather data
CREATE POLICY "Anyone can view market prices" ON market_prices FOR SELECT USING (true);
CREATE POLICY "Anyone can view government schemes" ON government_schemes FOR SELECT USING (true);
CREATE POLICY "Anyone can view weather data" ON weather_data FOR SELECT USING (true);
CREATE POLICY "Anyone can view community questions" ON community_questions FOR SELECT USING (true);
