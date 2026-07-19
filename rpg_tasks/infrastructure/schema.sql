-- BASE DE DATOS
CREATE DATABASE IF NOT EXISTS rpg_tasks_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE rpg_tasks_db;

-- TABLA USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_externo_usuario VARCHAR(100) UNIQUE NOT NULL, -- Id del usuario para usar en la plataforma externa
    nombre_usuario VARCHAR(100) NOT NULL,
    password_usuario VARCHAR(20) NOT NULL,
    email_usuario VARCHAR(100),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    rango VARCHAR(50) DEFAULT "NOVATO",
    tipo_usuario INT DEFAULT 0,
    idioma_usuario VARCHAR(2)
) ENGINE=InnoDB;

-- TABLA PLATAFORMAS
CREATE TABLE IF NOT EXISTS plataformas (
    id_conexion INT AUTO_INCREMENT PRIMARY KEY,
    id_plataforma INT,
    nombre_plataforma VARCHAR(100),
    id_usuario INT,
    id_externo_usuario VARCHAR(100), 
    token_usuario VARCHAR(100), -- Token de sesion del usuario
    fecha_expiracion DATETIME DEFAULT (DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 7 DAY)), -- Fecha de expiracion del token de sesion
    id_usuario_en_plataforma VARCHAR(100) UNIQUE, -- ID para evitar la duplicación de cuentas en una sola plataforma
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_externo_usuario) REFERENCES usuarios(id_externo_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;


-- TABLA PERSONAJES
CREATE TABLE IF NOT EXISTS personajes (
    id_usuario INT,
    id_personaje INT AUTO_INCREMENT PRIMARY KEY,
    nombre_personaje VARCHAR(50),
    genero VARCHAR(50),
    clase VARCHAR(30),
    nivel INT DEFAULT 1,
    exp INT DEFAULT 0,
    evolucion INT DEFAULT 0,
    icono_personaje TEXT,
    imagen_personaje TEXT,
    animacion_personaje TEXT,
    descripcion_personaje TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

-- TABLA TAREAS
CREATE TABLE IF NOT EXISTS tareas (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_personaje INT,
    nombre_tarea VARCHAR(500),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    tarea_completada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_personaje) REFERENCES personajes(id_personaje) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;