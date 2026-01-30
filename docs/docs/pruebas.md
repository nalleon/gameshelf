---
icon: lucide/book-check
---

# Pruebas

## Estrategia de pruebas

La metodología para comprobar nuestra aplicación, ha sido la __implementación__ de __tests__ tanto __unitarios__ como de __integración__ y __aceptación__, proporcionados por el __profesor__ como un __requisito básico__ para saber que todo estaba bien.

## Casos de prueba

Por ejemplo, en los test siempre se comprueba que existan una __urls específicas__, que llamen a un __método específico__. También se comprueba que se muestre una __información específica__ en el __perfil__ del alumno o profesor. Que se pueda acceder a un lugar en concreto solo si __cumples unos requisitos__ o que el própio código __actue de una forma en concreto__.

## Cobertura de pruebas

En nuestro caso, el código esta siendo comprobado casi en su totalidad, ya que esto le ahorra trabajo al profesor a la hora de corregir el proyecto. Se podría decir que el 100% del código se revisa atraves de 122 tests unitarios para asegurar que __contenga todo lo solicitado__ y solo queda comprobar que se ha realizado de la forma más optima, que no haya variables sin usar, en resumen, todo lo que se puede mejorar.

## Automatización

La automatización de las pruebas en el proyecto __Lumino__ se basa en la ejecución automática de los tests proporcionados mediante comandos predefinidos. Estos comandos permiten verificar de forma rápida y repetible que la aplicación cumple con los requisitos establecidos.

El uso de recetas automatizadas facilita la ejecución de las pruebas sin necesidad de configuraciones adicionales, asegurando que el estado del proyecto puede comprobarse en cualquier momento de forma consistente. De este modo, cada cambio realizado en el código puede validarse ejecutando nuevamente los tests, reduciendo la posibilidad de introducir errores.

