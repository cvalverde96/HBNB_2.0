INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$sD1uqNfsC9uMTFQnvnWWKeHkKL9Udv/2dHVz4MtMPC3EIxkWfTZnC', --admin1234
    TRUE
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO Amenity (id, name)
VALUES
    ('cb2bb026-669f-443f-8bcb-e7ef87e59a8e', 'WiFi'),
    ('b9220957-dc92-4c06-a88b-18a63c4bf403', 'Swimming Pool'),
    ('9d5cd45b-ee54-41a7-81a1-676e12a17fe4', 'Air Conditioning')
ON CONFLICT (id) DO NOTHING;