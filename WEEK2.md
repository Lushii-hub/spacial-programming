# GUÍA SEMANA 2: DISPAROS, BALAS Y COLISIONES

Esta guía contiene los pasos detallados para completar la **Semana 2** del proyecto, abarcando la creación de proyectiles, su movimiento y la detección de colisiones con los enemigos.

---

## 📋 OBJETIVOS DE LA SEMANA 2
1. Entender el concepto de **cadencia de disparo / recarga** (`cooldown`).
2. Implementar la función de disparo `shoot()` en `game/player.py`.
3. Comprender cómo la clase `Bullet` (`game/bullet.py`) maneja el movimiento de los proyectiles y la limpieza de memoria.
4. Comprender cómo el sistema de colisiones (`game/collisions.py`) detecta impactos entre rectángulos (*hitboxes*) usando `colliderect`.

---

## 🛠️ PASO A PASO DE LA SEMANA 2

### PASO 1: Atributos de Recarga (`cooldown`)
Para evitar que la computadora genere cientos de balas por segundo cuando el jugador presiona `SPACE`, definimos un tiempo de espera en el `__init__` de `game/player.py`:

```python
# game/player.py -> __init__()
self.cooldown = 10         # Espera total de cuadros (frames) entre disparos
self.cooldown_timer = 0    # Reloj regresivo
```

---

### PASO 2: Actualizar el Reloj de Recarga (`update_cooldown`)
En cada cuadro del juego, llamamos a `update_cooldown()` para descontar 1 al reloj hasta llegar a cero:

```python
def update_cooldown(self):
    if self.cooldown_timer > 0:
        self.cooldown_timer -= 1
```

---

### PASO 3: Programar la Función de Disparo (`shoot`)
Cuando el jugador presiona la barra espaciadora (`SPACE`), comprobamos si el reloj llegó a cero. Si es así, reiniciamos el reloj y creamos una bala en la punta de la nave:

```python
def shoot(self):
    # 1. Verificar si la nave puede disparar
    if self.cooldown_timer <= 0:
        # 2. Reiniciar el reloj de recarga
        self.cooldown_timer = self.cooldown
        
        # 3. Calcular la punta de la nave (X e Y)
        bullet_x = self.actor.x + (self.width // 2)
        bullet_y = self.actor.y
        
        # 4. Crear y retornar el objeto Bullet
        return Bullet(bullet_x, bullet_y)
    
    return None
```

---

### PASO 4: Movimiento de la Bala y Limpieza de Memoria (`game/bullet.py`)
Cada bala creada es un objeto de la clase `Bullet`. Tiene dos comportamientos clave:

1. **Movimiento Continuo**: Avanza hacia la derecha en cada cuadro:
   ```python
   def move(self):
       self.actor.x += self.speed
   ```
2. **Limpieza de Pantalla**: Si no impacta a ningún enemigo y sale volando fuera de la pantalla, se destruye para no saturar la memoria RAM:
   ```python
   def is_off_screen(self):
       return self.actor.x > WIDTH + 20
   ```

---

### PASO 5: Detección de Colisiones (`game/collisions.py`)
El sistema de colisiones compara las cajas rectangulares de cada bala y cada enemigo activo usando `colliderect`:

```python
# Recorremos todas las balas y enemigos
for b in bullets:
    for e in enemies:
        # ¿Impactó la bala al enemigo?
        if b.actor.colliderect(e.actor):
            bullets.remove(b)                      # 1. Destruye la bala
            enemies.remove(e)                      # 2. Destruye al enemigo
            player.score += e.points               # 3. Le otorga puntos al jugador
            explosions.append(Explosion(e.x, e.y)) # 4. Crea efecto visual de explosión
            break
```

---

### 🚀 PRUEBA TU CÓDIGO
Ejecuta en tu terminal:
```bash
python3 watch.py
```
Presiona **`Ctrl + S`**, presiona la **barra espaciadora (`SPACE`)** y ¡dispara a los enemigos!
