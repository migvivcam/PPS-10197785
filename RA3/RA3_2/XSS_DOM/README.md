LOW:
La pagina utiliza el metodo GET para seleccionar el idioma.
Cambiando la URL para introducir el paylod --> <script>alert(document.cookie);</script>

MEDIUM:
En el nivel medium los campos del formulario se encuentran dentro de la etiqueta option.
Usando el payload --> " ></option></select><img src=x onerror="alert(document.cookie)"> se sale de la etiqueta para cargar una imagen erronea y que se ejecute codigo al fallar la carga.