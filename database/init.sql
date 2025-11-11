CREATE TABLE IF NOT EXISTS app_info (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO app_info (service_name, version) VALUES 
('backend-api', '1.0.0'),
('database', 'postgres-15'),
('frontend', '1.0.0')
ON CONFLICT DO NOTHING;
