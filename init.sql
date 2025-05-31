-- Create separate schemas for each microservice
CREATE SCHEMA IF NOT EXISTS user_service;
CREATE SCHEMA IF NOT EXISTS restaurant_service;
CREATE SCHEMA IF NOT EXISTS delivery_service;

-- User Service Tables
-- Users Table
CREATE TABLE IF NOT EXISTS user_service.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Orders Table
CREATE TABLE IF NOT EXISTS user_service.orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS user_service.order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    notes TEXT
);

-- Ratings Table
CREATE TABLE IF NOT EXISTS user_service.ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    restaurant_rating INTEGER CHECK (restaurant_rating BETWEEN 1 AND 5),
    delivery_rating INTEGER CHECK (delivery_rating BETWEEN 1 AND 5),
    comments TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Restaurant Service Tables
-- Restaurants Table
CREATE TABLE IF NOT EXISTS restaurant_service.restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    address TEXT NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    is_online BOOLEAN DEFAULT FALSE,
    opening_time TIME,
    closing_time TIME,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Menu Categories Table
CREATE TABLE IF NOT EXISTS restaurant_service.menu_categories (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Menu Items Table
CREATE TABLE IF NOT EXISTS restaurant_service.menu_items (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    category_id INTEGER REFERENCES restaurant_service.menu_categories(id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    image_url TEXT
);

-- Restaurant Orders Table (mirror of user_service.orders with additional fields)
CREATE TABLE IF NOT EXISTS restaurant_service.orders (
    id SERIAL PRIMARY KEY,
    user_order_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    delivery_agent_id INTEGER,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    preparation_time INTEGER, -- in minutes
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Delivery Service Tables
-- Delivery Agents Table
CREATE TABLE IF NOT EXISTS delivery_service.delivery_agents (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'inactive', -- inactive, available, busy
    current_latitude DECIMAL(10, 8),
    current_longitude DECIMAL(11, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Deliveries Table
CREATE TABLE IF NOT EXISTS delivery_service.deliveries (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    restaurant_order_id INTEGER NOT NULL,
    delivery_agent_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'assigned', -- assigned, picked_up, in_transit, delivered
    pickup_time TIMESTAMP WITH TIME ZONE,
    delivery_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create some sample data
-- Sample users
INSERT INTO user_service.users (username, email, password_hash, first_name, last_name, phone_number, address)
VALUES 
('john_doe', 'john@example.com', '$2b$12$eKjaHVRgOVClP22vhTGTq.amFbFka9eK5Ze.xOcVG9jk3wNF2yKQm', 'John', 'Doe', '555-123-4567', '123 Main St'),
('jane_smith', 'jane@example.com', '$2b$12$JCtfJ1VBn.n5r5Ll/VyjL.rWBdEl.L9nHL9q7A46rdRs9jKfCdup2', 'Jane', 'Smith', '555-234-5678', '456 Oak Ave');

-- Sample restaurants
INSERT INTO restaurant_service.restaurants (name, description, address, phone_number, email, is_online, opening_time, closing_time)
VALUES 
('Pizza Palace', 'Best pizza in town', '789 Elm St', '555-345-6789', 'info@pizzapalace.com', TRUE, '10:00', '22:00'),
('Burger Shack', 'Gourmet burgers', '321 Pine Rd', '555-456-7890', 'info@burgershack.com', TRUE, '11:00', '23:00'),
('Sushi World', 'Fresh sushi', '654 Maple Ln', '555-567-8901', 'info@sushiworld.com', FALSE, '12:00', '22:30');

-- Sample menu categories
INSERT INTO restaurant_service.menu_categories (restaurant_id, name, description)
VALUES 
(1, 'Pizzas', 'Our signature pizzas'),
(1, 'Sides', 'Perfect companions'),
(2, 'Burgers', 'Flame-grilled goodness'),
(2, 'Fries', 'Crispy delights'),
(3, 'Rolls', 'Fresh rolls'),
(3, 'Sashimi', 'Raw perfection');

-- Sample menu items
INSERT INTO restaurant_service.menu_items (restaurant_id, category_id, name, description, price, is_available)
VALUES 
(1, 1, 'Margherita', 'Classic cheese and tomato', 9.99, TRUE),
(1, 1, 'Pepperoni', 'Spicy pepperoni with cheese', 11.99, TRUE),
(1, 2, 'Garlic Bread', 'Toasted with garlic butter', 3.99, TRUE),
(2, 3, 'Classic Burger', 'Beef patty with lettuce and tomato', 8.99, TRUE),
(2, 3, 'Cheese Burger', 'Classic with melted cheese', 9.99, TRUE),
(2, 4, 'French Fries', 'Crispy golden fries', 2.99, TRUE),
(3, 5, 'California Roll', 'Crab, avocado, cucumber', 6.99, TRUE),
(3, 5, 'Spicy Tuna Roll', 'Fresh tuna with spicy sauce', 7.99, TRUE),
(3, 6, 'Salmon Sashimi', 'Fresh slices of salmon', 12.99, TRUE);

-- Sample delivery agents
INSERT INTO delivery_service.delivery_agents (username, email, password_hash, first_name, last_name, phone_number, status)
VALUES 
('mike_delivery', 'mike@delivery.com', '$2b$12$iKX0oEm7JwSIJApDTmrp6uc/6AE9HsAzRt3hWh3gJCR5SPdPGJRUm', 'Mike', 'Johnson', '555-678-9012', 'available'),
('lisa_delivery', 'lisa@delivery.com', '$2b$12$tOGK0HJ6mVsaAnAQZb.3HegiYOhz3.xhiDxBU/nhCi2Rb41KWxPeC', 'Lisa', 'Williams', '555-789-0123', 'available');
