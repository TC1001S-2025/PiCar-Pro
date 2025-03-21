# PiCar-Pro

Esta es la documentación para usar la librería de PiCar.py
Con las siguientes funciones podrás manipular todas las funciones del robot para completar una tarea en específico.

A considerar:
- Al ejecutar el código del robot, todos los servos vuelven a su posición inicial. Por esta razón todas las instrucciones que requieran ser ejecutadas, deberán ser aplicadas en una sola ejecución.

## Instrucciones
1. Prender la Raspberry Pi insertando las pilas en la parte inferior del robot o conectando un cable de alimentación tipo C a la Raspberry Pi.
2. Prender un router y conectar tanto la Raspberry Pi como la computadora que se usará para programar al PiCar a la misma red.
3. Conectar la computadora a la Raspberry Pi mediante el método de preferencia (Putty, SSH). `Usuario: car`, `Contraseña: raspberry`. Por SSH sería de la siguiente manera: ssh car@ip-de-la-RaspberryPI -p 22
5. Crear un nuevo archivo .py e importar la librería PiCar localizada en `Documents/PiCar-Pro`
6. Usar las librerías libremente :)
7. Ejecutar el programa con `python3 <nombre_del_programa>.py`

## Movimiento

Las funciones de movimiento son las siguientes:

- `moveForward()`: El robot se mueve hacia enfrente por 1 segundo
- `moveBackward()`: El robot se mueve hacia atrás por 1 segundo
- `rotateRight()`: El robot se mueve hacia la derecha por 1 segundo
- `rotateLeft():` El robot se mueve hacia la izquierda por 1 segundo

## Brazo

Las funciones del brazo son las siguientes:

- `moveArmUp()`: El robot mueve el brazo 15° hacia arriba
- `moveArmDown()`: El robot mueve el brazo 15° hacia abajo
- `rotateArmRight()`: El robot rota el brazo 15° hacia la derecha
- `rotateArmLeft()`: El robot rota el brazo 15° hacia la izquierda

## Garra

Las funciones de la garra son las siguientes:

- `openClaw()`: El robot abre la garra
- `closeClaw()`: El robot cierra la garra
- `moveWristUp()`: El robot mueve la garra 15° hacia arriba
- `moveWristDown()`: El robor mueve la garra 15° hacia abajo

## Luces

Las funciones de las luces son las siguientes:

- `ledOn()`: El robot enciende las luces
- `ledOff()`: El robot apaga las luces
