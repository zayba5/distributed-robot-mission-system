CREATE TABLE robots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    x_position INTEGER DEFAULT 0,
    y_position INTEGER DEFAULT 0,
    battery INTEGER DEFAULT 100,
    status VARCHAR(50) DEFAULT 'AVAILABLE',
    last_telemetry TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE missions (
    id SERIAL PRIMARY KEY,
    start_x INTEGER NOT NULL,
    start_y INTEGER NOT NULL,
    destination_x INTEGER NOT NULL,
    destination_y INTEGER NOT NULL,
    priority INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'QUEUED',
    assigned_robot_id INTEGER REFERENCES robots(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

INSERT INTO robots
(name, x_position, y_position, battery, status)
VALUES
('Robot-1', 0, 0, 100, 'AVAILABLE'),
('Robot-2', 0, 0, 100, 'AVAILABLE'),
('Robot-3', 0, 0, 100, 'AVAILABLE'),
('Robot-4', 0, 0, 100, 'AVAILABLE'),
('Robot-5', 0, 0, 100, 'AVAILABLE');
