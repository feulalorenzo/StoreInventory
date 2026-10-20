-- Creazione del database
CREATE DATABASE IF NOT EXISTS negozio_inventario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE negozio_inventario;

-- Tabella dei prodotti
CREATE TABLE IF NOT EXISTS prodotti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descrizione TEXT,
    prezzo DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    quantita INT NOT NULL DEFAULT 0,
    data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;