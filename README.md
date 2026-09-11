# COSMIC ADVENTURE

Juego creado por Lucía Campos Umaña para el taller Spacial Programming.

---

## 1. CÓMO INSTALAR EL PROYECTO

Clona o descarga la carpeta del proyecto y abre tu terminal en ella:
```bash
cd spacial-programming
```

### Paso 1: Crear el Entorno Virtual (`.venv`) con Python 3.12
- **En macOS / Linux**:
  ```bash
  python3.12 -m venv .venv
  ```
- **En Windows (CMD / PowerShell)**:
  ```cmd
  py -3.12 -m venv .venv
  ```

### Paso 2: Activar el Entorno Virtual
- **En macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```
- **En Windows (CMD / PowerShell)**:
  ```cmd
  .venv\Scripts\activate
  ```

### Paso 3: Instalar las Dependencias (`pgzero` y `pygame`)
Con el entorno virtual activado, instala las dependencias del proyecto:
```bash
pip install -r requirements.txt
```

---

## 2. CÓMO EJECUTAR EL JUEGO

Con el entorno virtual activado (`.venv`), ejecuta el juego con cualquiera de estos dos comandos:

### Abrir el proyecto en Visual Studio Code como en la guía

1. Haz doble clic en `2_ABRIR_EN_VISUAL_STUDIO_CODE.bat`.
2. El proyecto completo aparecerá en el explorador izquierdo y se abrirá este `README.md`.
3. Para colocar la vista previa del README a la derecha, presiona `Ctrl + K` y después `V`.
4. Para mostrar la terminal en la parte inferior, presiona `Ctrl + J`.
5. Para instalar y ejecutar el juego desde esa terminal, presiona `Ctrl + Shift + B`.

También puedes abrir **Ejecutar y depurar** en la barra izquierda y pulsar el
botón verde junto a `Cosmic Adventure: ejecutar juego`. Este botón prepara el
entorno automáticamente la primera vez.

Visual Studio Code utilizará automáticamente el Python 3.12 de la carpeta `.venv`.

### Windows por primera vez (doble clic)

Abre `1_INSTALAR_Y_ABRIR_JUEGO.bat`. Este archivo instala o verifica Python 3.12,
entra automáticamente en la carpeta correcta, crea el entorno, instala las
dependencias necesarias y abre el juego. No abras `watch.py` mediante doble clic.

### Opción A (Recomendada con Auto-reinicio al guardar con Ctrl + S):
```bash
python watch.py
```

### Opción B (Ejecución directa):
```bash
pgzrun main.py
```

### Controles personalizados

- Flecha izquierda: mover hacia la izquierda.
- Flecha derecha: mover hacia la derecha.
- Flecha arriba: subir.
- Flecha abajo: bajar.
- Barra espaciadora: lanzar el ovillo.
- Tecla `P`: pausar y reanudar la partida.
- En la pausa, botón `GO HOME`: guardar el récord y volver a la portada.

Después de seleccionar `START GAME`, aparece la pantalla **ELIGE TU PERSONAJE**:

- Nyan Cat dispara el ovillo con un maullido y utiliza la música original.
- Kirby dispara estrellas con el sonido Poyo y utiliza su propia música de fondo.
- Ambos personajes conservan la misma estela de arcoíris animada.
- Si se dispara muchas veces seguidas, el sonido termina antes de volver a sonar.

La nave acelera gradualmente con la puntuación y deja una estela de arcoíris animada.
El objetivo es superar el récord mostrado en la portada y en la partida. El mejor
puntaje se guarda automáticamente y continúa disponible al volver a abrir el juego.
El jefe final utiliza una animación de gato con fondo transparente.
Cada proyectil del jefe reproduce su efecto de sonido especial.
El único objeto extra es la lata RUN FAST. Al recogerla se activa el modo HARDCORE
durante 45 segundos. Kirby utiliza Kirby Theme y Nyan Cat utiliza Nyan Cat Trap
Remix; mientras tanto, los enemigos aparecen y se mueven más rápido.
No hay escudos ni objetos de vida extra; la nave comienza cada partida con 5 vidas.
La música de fondo se reproduce durante la partida y baja gradualmente de volumen
al acercarse a los 1000 puntos; al aparecer el jefe final termina de desvanecerse.
El fondo espacial se desplaza continuamente sin mostrar bordes ni cortes.
Al derrotar al jefe se reproduce la secuencia de victoria original de la versión
14: aparece el meme animado Galaxy Brain, se desvanece y comienza el audio de
Harry Maguire antes de mostrar "MISSION COMPLETE!".

---

## 3. USO DE FUENTES TIPOGRAFICAS (.TTF / .OTF)

Para cambiar la fuente de texto de todo el juego (Menu, Puntaje, Marcador, Vidas, Pantalla de Victoria y Game Over):

1. Descarga cualquier archivo de fuente con extension `.ttf` o `.otf` (por ejemplo `arcade.ttf`).
2. Guardalo dentro de la carpeta:
   `fonts/`
3. El juego detectara automaticamente tu archivo `.ttf` o `.otf` y aplicara esa tipografia a todo el juego.

---

## 4. ESTRUCTURA DEL PROYECTO

```
Spacial_Programming_Lucia/
│
├── main.py                   # Punto de entrada principal (Pygame Zero)
├── README.md                 # Guia de instalacion y didactica
├── requirements.txt          # Dependencia (pgzero)
│
├── fonts/                    # Carpeta para colocar archivos .ttf o .otf
├── sonido/                   # Música y sonidos de Nyan Cat, Kirby y efectos
│
├── images/                   # Carpeta para colocar tus imagenes PNG
│   ├── player/               # Nyan Cat y Kirby (spaceship.png, kirby.png)
│   ├── enemies/              # Imagenes de enemigos y boss (alien.png, boss.png)
│   ├── bullets/              # Ovillo, disparos enemigos y estrella de Kirby
│   ├── backgrounds/          # Imagenes de fondo de pantalla
│   ├── effects/              # Imagenes de explosiones
│   └── powerups/             # Lata RUN FAST del modo HARDCORE
│
└── game/
    ├── player.py             # ARCHIVO DE TRABAJO DE LOS ESTUDIANTES (Clase Player)
    ├── powerup.py            # Lata RUN FAST (único objeto extra)
    ├── enemy.py              # Clase Enemy
    ├── boss.py               # Clase Boss (Jefe final tipo Metal Slug)
    ├── bullet.py             # Clases Bullet y EnemyBullet (Herencia)
    ├── explosion.py          # Clase Explosion
    ├── victory.py            # Secuencia animada de victoria
    ├── background.py         # Modulo de fondo continuo
    ├── ui.py                 # Renderizado de la interfaz
    ├── waves.py              # Administrador de enemigos
    ├── collisions.py         # Administrador de colisiones
    └── game_manager.py       # Controlador principal del juego
```

---

## 5. GUÍAS SEMANALES Y PLAN DE CLASE DE POO

Para seguir el taller paso a paso divido en semanas o clases, consulta los documentos oficiales:

1. **[SEMANA 1: La Nave del Jugador y Movimiento](WEEK1.md)**
   - Creación de atributos con `self`, carga de imágenes personalizadas, programación del movimiento (UP, DOWN, LEFT, RIGHT) y límites de pantalla con `half_width`/`half_height`.
2. **[SEMANA 2: Disparos, Balas y Colisiones](WEEK2.md)**
   - Cadencia de disparos (`cooldown`), generación de proyectiles (`Bullet`), movimiento de balas y sistema de colisiones con `colliderect`.
3. **[SEMANA 3: Proyecto Final y Rúbrica de 50 Puntos](WEEK3.md)**
   - Rúbrica oficial de evaluación por 50 puntos y lista de verificación final para el estudiante.
