# Programacion4to
Repositorio creado para guardar codigos de la materia de programacion de 4to año del instituto tecnologico isaac newton
from pathlib import Path
import pypandoc

md = """# Programación - 4.º Año

## Bienvenido/a

Este repositorio reúne las actividades, ejercicios y proyectos realizados durante la materia **Programación** de 4.º año.

## Contenidos

Durante el año se trabajarán los siguientes temas de Python:

- Introducción a la programación
- Instalación y uso del entorno de desarrollo
- Variables y tipos de datos
- Entrada y salida de datos (`input` y `print`)
- Operadores aritméticos, lógicos y relacionales
- Condicionales (`if`, `elif`, `else`)
- Bucles (`for` y `while`)
- Funciones
- Cadenas de texto
- Listas
- Tuplas
- Diccionarios

## Proyecto Final

Una vez aprendidos los conceptos básicos de Python, el objetivo será desarrollar un **videojuego**, aplicando todos los conocimientos adquiridos durante el año.

## Objetivos

- Aprender la lógica de programación.
- Resolver problemas mediante algoritmos.
- Escribir código claro y ordenado.
- Trabajar en proyectos cada vez más complejos.
- Integrar todos los contenidos en un videojuego funcional.

## Autor

**Alumno:** ........................................  
**Curso:** 4.º Año  
**Materia:** Programación
"""
path="/mnt/data/README.md"
Path(path).write_text(md,encoding="utf-8")
print(path)
