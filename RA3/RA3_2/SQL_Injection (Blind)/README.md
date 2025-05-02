SQL_BLIND:
En el apartado SQL_BLIND no se muestra la información de la base de datos, pero se utiliza la función sleep() para comprobar si el resgistro existe en estas.
Como payload se busca la versión de la base de datos, para ello utilizando un script se comprueban la cantidad de caracteres para posteriormente buscar caracter a caracter el codigo de la versión.

Modificaciones al script original:
URL - Cambiar la IP por la utilizada en este laboratorio.
Cookie - Cambiar la id de la sesión a la de este laboratiorio.
Length - Incializar Length debido a cambios en las versiones de python.