
INSERT INTO brands
  ( id, name )
VALUES
  ('415ef8eb-e141-4e44-9ea5-1f8dfb5b15f8', 'Funko'),
  ('742f12ef-a896-4274-9efc-0fe604b2d335', 'Banpresto'),
  ('946d48ad-53ed-49a3-b7a8-d4f456a9f3b4', 'Megahouse'),
  ('ffc1f3be-74a9-4fe7-86ee-0fe51fa5422b', 'Figuarts'),
  ('f77a0a60-e5b3-4c48-92d8-d52a2b4e24fa', 'MythCloth'),
  ('0ae3358b-a2cc-4e2f-ac22-98abdbdddd59', 'Hasbro');

INSERT INTO products
	(id, name, description, price, image_url, stock, brand_id)
VALUES
	('415ef8eb-e141-4e44-9ea5-1f8dfb5b15f8', 'No Way Home - Spider-Man AAA', 'Funko Pop Marvel : No Way Home - Spider-Man AAA (Unmasked) #1073', 89.90, 'https://sevenfiguarts.com.pe/wp-content/uploads/2024/08/Funko-Pop-Marvel-No-Way-Home-Spider-Man-AAA-Unmasked-1073-P-1.png', 11, '415ef8eb-e141-4e44-9ea5-1f8dfb5b15f8'),
	('ffc1f3be-74a9-4fe7-86ee-0fe51fa5422b', 'One Piece: Sabo - Revolutionary Army Chief of Staff', 'One Piece: Sabo - Revolutionary Army Chief of Staff', 107.65, 'https://sevenfiguarts.com.pe/wp-content/uploads/2024/09/SH-FIGUARTS-ONE-PIECE-SABO.png', 6, 'ffc1f3be-74a9-4fe7-86ee-0fe51fa5422b');

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


