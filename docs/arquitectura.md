# Índice
- [Arquitectura del proyecto](#diagrama-de-la-arquitectura-del-proyecto)
- [Estructura de carpetas](#estructura-de-carpetas)

--- 

## Diagrama de la arquitectura del Proyecto


<div align="center">
<img width="1500" height="1200" alt="DiagramaBackendFrontEnd" src="https://github.com/user-attachments/assets/3dd9264c-7b93-45a5-ba97-674ab4b0ce84" />
</div>

Como se puede apreciar en la imagen, la idea principal del proyecto consiste en una arquitectura hexagonal que contiene el núcleo de la aplicación. 
Las aplicaciones externas, que tienen el rol de clientes, se conectarán a través de FastApi realizando peticiones http.
De esta forma, el núcleo de la aplicación es totalmente independiente de las tecnologías acopladas.

## Estructura de carpetas
