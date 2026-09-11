# GUÍA SEMANA 3: PROYECTO FINAL Y RÚBRICA DE EVALUACIÓN (50 PUNTOS)

Esta guía contiene la presentación final del proyecto y la **Rúbrica Oficial de Evaluación de 50 Puntos** para calificar el juego desarrollado por cada estudiante.

---

## 🎯 OBJETIVOS DE LA SEMANA 3
1. Integrar todas las características aprendidas (Movimiento, Disparos, Personalización).
2. Verificar los límites de pantalla y el correcto funcionamiento del juego.
3. Personalizar completamente el proyecto (título del juego, nombre del estudiante, imagen propia de la nave y configuración de pantalla).
4. Presentación y evaluación del proyecto según la rúbrica de 50 puntos.

---

## 📊 RÚBRICA DE EVALUACIÓN DE 50 PUNTOS

| Ítem | Criterio de Evaluación | Puntos Máximos | Puntaje Obtenido |
| :--- | :--- | :---: | :---: |
| **1. Movimiento Arriba** | La nave se desplaza correctamente hacia arriba al presionar `UP` respetando los límites de pantalla superiores. | **5 Pts** | |
| **2. Movimiento Abajo** | La nave se desplaza correctamente hacia abajo al presionar `DOWN` respetando los límites de pantalla inferiores. | **5 Pts** | |
| **3. Movimiento Izquierda** | La nave se desplaza correctamente hacia la izquierda al presionar `LEFT` respetando el límite izquierdo. | **5 Pts** | |
| **4. Movimiento Derecha** | La nave se desplaza correctamente hacia la derecha al presionar `RIGHT` respetando el límite derecho. | **5 Pts** | |
| **5. Sistema de Disparos** | Implementación correcta del método `shoot()` y tiempo de recarga (`cooldown`). Las balas se generan en la punta de la nave y avanzan hacia la derecha. | **15 Pts** | |
| **6. Colisiones y Daño** | Detección correcta de impactos entre las balas y los enemigos, otorgando puntos al jugador y eliminando los enemigos destruidos. | **10 Pts** | |
| **7. Juego Personalizado** | Personalización completa del juego con imagen propia de la nave en `images/player/`, título y nombre del alumno configurados en `config.py`. | **5 Pts** | |
| **TOTAL** | **PUNTAJE FINAL DEL PROYECTO** | **50 Pts** | |

---

## 📝 CHECKLIST DE VERIFICACIÓN PARA EL ESTUDIANTE

Antes de hacer tu presentacion final, asegúrate de cumplir con los siguientes puntos:

- [ ] ¿Tu nave se mueve en las 4 direcciones sin salirse del borde de la pantalla?
- [ ] ¿El archivo `config.py` tiene tu nombre y el título de tu juego en `TITLE`?
- [ ] ¿Tu nave tiene su propia imagen personalizada en la carpeta `images/player/`?
- [ ] ¿Al presionar la barra espaciadora (`SPACE`), tu nave dispara balas sin trabarse?
- [ ] ¿Al destruir naves enemigas sumas puntos en la pantalla?
- [ ] ¿Al llegar a 1000 puntos aparece el Jefe Final?
