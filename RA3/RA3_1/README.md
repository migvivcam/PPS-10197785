# RA3_1
  
### Indice

* [Intro](#Intro): Intro
* [Desarrollo](#Desarrollo): Desarrollo
* [Navegación](#Navegación): Navegación
  
## Intro

El hardening de servidores web es el proceso de mejorar la seguridad de un servidor web, reduciendo vulnerabilidades y eliminando posibles puntos de entrada que los atacantes pueden explotar.
Para realizar este hardening vamos a realizar las siguientes acciones en el entorno de trabajo:
* Mantener Apache actualizado
* Desactivar modulos innecesarios
* Deshabilitar la visualización del servidor
* Usar HTTPS
* Limitación de metodos HTTP
* Protección contra ataques de inyección
* Implementar autenticación básica
* Habilitar y configurar correctamente los registros
* Usar un firewall
* Configurar Timeout
* Implementar limites de uso por IP

## Desarrollo
Estas acciones se ejecutan en los siguientes puntos:

### [RA3_1_1 CSP](./RA3_1_1)
En este primer apartado se crea y configura la imagen base con la que se trabajarán los siguientes puntos y se establece una Política de Seguridad de contenido.  
  
### [RA3_1_2 WAF y OWASP](./RA3_1_2)
En este segundo apartado se instala y configura el modulo modsecurity2 para establecer un Firewall y reglas OWASP usando la imagen creada anteriormente.
  
### [RA3_1_3 DDOS](./RA3_1_3)
En este tercer apartado se implementa el modulo evasive para prevenir ataques de DDOS y limites de uso por IP.
  
### [RA3_1_4 SSL](./RA3_1_4)
En este apartado se configura Apache para utilizar certificados y HTTPS.
  
### [RA3_1_5 Hardening adicional](./RA3_1_5)
En este ultimo apartado se realizan configuraciones adicionales para la fortificación de Apache.
  
#### Navegación
[Atrás](../)  -  [Arriba](#RA3_1)  -  [Siguiente](./RA3_1_1)