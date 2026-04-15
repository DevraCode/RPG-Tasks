-- BASE DE DATOS
CREATE DATABASE IF NOT EXISTS rpg_tasks_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE rpg_tasks_db;

-- TABLA USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario VARCHAR(50) PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    password_usuario VARCHAR(20) NOT NULL,
    email_usuario VARCHAR(100),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB;

-- TABLA PLATAFORMAS (Desde donde se conecta el usuario)
CREATE TABLE IF NOT EXISTS plataformas (
    id_conexion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario VARCHAR(50) NOT NULL,
    nombre_plataforma VARCHAR(100) NOT NULL,
    id_externo_usuario VARCHAR(100) NOT NULL, -- Id del usuario de Telegram, Discord, etc
    UNIQUE KEY (nombre_plataforma, id_externo_usuario),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    
) ENGINE=InnoDB;

-- TABLA PERSONAJES
CREATE TABLE IF NOT EXISTS personajes (
    id_usuario VARCHAR(50),
    id_personaje INT AUTO_INCREMENT PRIMARY KEY,
    nombre_personaje VARCHAR(50),
    genero VARCHAR(50),
    clase VARCHAR(30),
    nivel INT DEFAULT 1,
    exp INT DEFAULT 0,
    evolucion INT DEFAULT 1,
    img VARCHAR(500),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

-- TABLA TAREAS
CREATE TABLE IF NOT EXISTS tareas (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario VARCHAR(50),
    nombre_tarea VARCHAR(500),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    tarea_completada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;