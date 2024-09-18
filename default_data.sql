-- DATOS SINCRONIZADOS CON EL BUCKET DE OCI
INSERT INTO brands (id, name) VALUES
('8adea714-6522-48c5-b953-8d51129a3ef7', 'Banpresto'),
('a14a5d49-4cfa-4ade-b66f-23d42151b378', 'Ninjamo'),
('fb9f6205-39e7-44dc-ac4d-752a919e11de', 'Tommy'),
('b765c60b-d535-4912-ae80-5cab1b786cae', 'Funko'),
('3b0acdfb-33a5-4b76-a684-bd1ff459cc3a', 'Hasbro');

-- DATOS SINCRONIZADOS CON EL BUCKET DE OCI
INSERT INTO products (id, name, description, price, image_url, stock, brand_id)
VALUES
('161a410b-a4fb-44b5-9709-ed83d0b5406f', 'Pikachu Figure Deluxe', 'figura de Pikachu', 200.00, 'https://id1jd0atgfra.objectstorage.us-ashburn-1.oci.customer-oci.com/p/LRU10nLEVa55NBKQR1JEX6dxfMmEJvfViqywdbBRXxCi7j4ayzuKwPWgC7p7T_0r/n/id1jd0atgfra/b/bucket-figures-store/o/Tommy/161a410b-a4fb-44b5-9709-ed83d0b5406f.jpg', 10, 'fb9f6205-39e7-44dc-ac4d-752a919e11de'),
('2c8db97f-29f8-4505-8e27-270afb04bd5a', 'Naruto', 'Naruto', 50.00, 'https://id1jd0atgfra.objectstorage.us-ashburn-1.oci.customer-oci.com/p/LRU10nLEVa55NBKQR1JEX6dxfMmEJvfViqywdbBRXxCi7j4ayzuKwPWgC7p7T_0r/n/id1jd0atgfra/b/bucket-figures-store/o/Bandai/2c8db97f-29f8-4505-8e27-270afb04bd5a.jpg', 20, '8adea714-6522-48c5-b953-8d51129a3ef7'),
('71310853-0b54-4306-9dc8-2f72172d9ec0', 'Lucario', 'Lucario', 35.50, 'https://id1jd0atgfra.objectstorage.us-ashburn-1.oci.customer-oci.com/p/LRU10nLEVa55NBKQR1JEX6dxfMmEJvfViqywdbBRXxCi7j4ayzuKwPWgC7p7T_0r/n/id1jd0atgfra/b/bucket-figures-store/o/Funko/71310853-0b54-4306-9dc8-2f72172d9ec0.jpg', 15, 'b765c60b-d535-4912-ae80-5cab1b786cae'),
('a5a77b13-1631-4770-bcc1-41212107bc36', 'Goku SSJ', 'Figura de Goku', 74.90, 'https://id1jd0atgfra.objectstorage.us-ashburn-1.oci.customer-oci.com/p/LRU10nLEVa55NBKQR1JEX6dxfMmEJvfViqywdbBRXxCi7j4ayzuKwPWgC7p7T_0r/n/id1jd0atgfra/b/bucket-figures-store/o/Tommy/https://Nonebucket-figures-store/Ninjamo/a5a77b13-1631-4770-bcc1-41212107bc36.jpg', 4, 'a14a5d49-4cfa-4ade-b66f-23d42151b378');


INSERT INTO users
	(id, first_name, last_name, address, email, username, hashed_password, role)
VALUES
    -- password secret01
	('adda01a3-4650-41a0-9b92-9c688f8da1cd', 'Henry', 'Colonia', 'Calle 1 N 123', 'henjacolonia17@gmail.com', 'admin01', '$2b$12$V2QhchT4R2JocgL8Yp9AbeSmyUSl84.tJUBJbZtVNflILi.8Dt5S2', 'admin'),
	-- password secret02
	('ef3fadf0-0baa-4d51-af97-790fa0cf41b3', 'Alonso', 'Guillen', 'Av 1 N 345', 'alonso.guicon@gmail.com', 'admin02', '$2b$12$e5kAg4/1tkHZj2oELev9T.ha/oEOvwR3N.CbGi.FhjGt/7sng./A.', 'admin'),
	-- password secret03
	('f761041d-968c-4e41-8f08-a67e8a18835a', 'Mario', 'Rodriguez', 'Jr 134 N 09', 'mario.rodriguez@gmail.com', 'user01', '$2b$12$f.nMfqTkQJ0TEpYKci2p0eSm20938m5vsrfoT9sOE/G1WbLgVKGP6', 'user'),
	-- password secret04
	('cb748b68-19a8-4977-ac78-9202b1819d05', 'Rosa', 'Perez', 'Jr 225 N 345', 'rosa.perez@gmail.com', 'user02', '$2b$12$nkACgYcum0miynklSESohug2IvFS.jWU8CksF1p9zV82awwFMnsUq', 'user'),
	-- password secret05
	('c90e689b-baeb-4323-b1e7-16700d642a8e', 'Jose', 'Paz', 'Calle 45 N 345', 'jose.paz@gmail.com', 'user03', '$2b$12$/NMyxlnOO66cuj5CAi5P1.n7nQeS6KCzCXrl0jcdAG24td2T9cvGG', 'user');


