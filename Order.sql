CREATE TABLE customers(
id SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(30) NOT NULL,
email VARCHAR(40) UNIQUE,
phone VARCHAR(13),
registation_date DATE
);

CREATE TABLE products(
id SERIAL PRIMARY KEY,
name VARCHAR(30) NOT NULL,
category VARCHAR(30),
price DECIMAL NOT NULL,
stock_quantity INT NOT NULL
);

CREATE TABLE orders(
id SERIAL PRIMARY KEY,
customer_id INT,
order_date TIMESTAMP DEFAULT now(),
total_amount DECIMAL,
FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items(
id SERIAL PRIMARY KEY,
order_id INT,
product_id INT,
quantity INT NOT NULL,
price_per_unit DECIMAL NOT NULL,
FOREIGN KEY(order_id) REFERENCES orders(id),
FOREIGN KEY(product_id) REFERENCES products(id)
);



INSERT INTO customers (id, name, email, phone, registation_date)
VALUES (1, 'Nikita', 'nikitanikita@gmail.com', '+48526226262', '2025-09-02'),
(2, 'Stya', 'styastya@gmail.com', '+48525656262', '2025-09-03'),
(3, 'Peter', 'peterpeter@gmail.com', '+4852648274', '2025-09-04'),
(4, 'Nata', 'natanata@gmail.com', '+48521226245', '2025-09-02'),
(5, 'Andrei', 'andreiandrei@gmail.com', '+483434343', '2025-09-03');

INSERT INTO products (name, category, price, stock_quantity)
VALUES ('salmon', 'food', 17, 120),
('apple', 'food', 2, 1000),
('orange', 'food', 6, 100),
('shark', 'food', 300, 2),
('BMW', 'car', 50000, 1),
('TV', 'electrical_engineering', 5000, 12),
('Phone', 'electrical_engineering', 1450, 6),
('Jacket', 'clothes', 300, 1300),
('Shorts', 'clothes', 30, 1),
('Sneakers', 'shoes', 5000, 1);

INSERT INTO orders (customer_id, total_amount)
VALUES (2, 2),
(1, 1),
(4, 3),
(5, 1),
(3, 3);

INSERT INTO order_items (order_id, product_id, quantity, price_per_unit)
VALUES (1, 10, 1, 5000),
(1, 8, 10, 300),
(2, 9, 1, 30),
(3, 1, 40, 17),
(3, 2, 500, 2),
(3, 3, 100, 6),
(4, 7, 3, 1450),
(5, 5, 1, 50000),
(5, 4, 1, 300),
(5, 6, 4, 5000);



SELECT customer_id, name, email, phone FROM orders
LEFT JOIN customers
ON orders.customer_id = customers.id 
WHERE total_amount > 0
ORDER BY customer_id ASC;

SELECT quantity, name FROM order_items
LEFT JOIN products
ON order_items.product_id = products.id
ORDER BY quantity DESC;

SELECT name, total_amount FROM orders
LEFT JOIN customers
ON orders.customer_id = customers.id
ORDER BY total_amount DESC;

SELECT name, MAX(price_per_unit * quantity) AS Max_sale FROM order_items
LEFT JOIN products
ON order_items.order_id = products.id
GROUP BY name
ORDER BY max_sale DESC
LIMIT 1;

SELECT name, order_date FROM orders
LEFT JOIN customers
ON orders.id = customers.id
WHERE order_date <= '2024-12-02';

SELECT AVG(price_per_unit * quantity) AS Average_sale FROM order_items
LEFT JOIN orders
ON order_items.id = orders.id
WHERE order_date >= '2025-01-02';

SELECT customers.name, 
customers.email, 
customers.phone, 
customers.registation_date,
products.name,
products.price,
order_items.quantity,
order_date
FROM orders
JOIN customers
ON orders.customer_id = customers.id
JOIN products
ON orders.id = products.id
JOIN order_items
ON orders.id = order_items.id;
