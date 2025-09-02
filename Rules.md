# BET

## REGLAS DE MONTOS DE APUESTAS

## Tabla de progresión

| Progreso | Día | Apuesta (COP) | Ganas (COP) | Guardas 30% | Reinviertes (siguiente día) | Acumulado guardado |
| --- | --- | --- | --- | --- | --- | --- |
|  | 1 | 10,000 | 20,000 | 5,000 | 15,000 | 5,000 |
|  | 2 | 15,000 | 30,000 | 9,000 | 21,000 | 14,000 |
|  | 3 | 21,000 | 42,000 | 12,600 | 29,400 | 26,600 |
|  | 4 | 29,400 | 58,800 | 17,640 | 41,160 | 44,240 |
|  | 5 | 41,160 | 82,320 | 24,696 | 57,624 | 68,936 |
|  | 6 | 57,624 | 115,248 | 34,574 | 80,674 | 103,510 |
|  | 7 | 80,674 | 161,348 | 48,404 | 112,944 | 151,914 |
|  | 8 | 112,944 | 225,888 | 67,766 | 158,122 | 219,680 |
|  | 9 | 158,122 | 316,244 | 94,873 | 221,371 | 314,553 |
|  | 10 | 221,371 | 442,742 | 132,822 | 309,920 | 447,375 |
|  | 11 | 309,920 | 619,840 | 185,952 | 433,888 | 633,327 |
|  | 12 | 433,888 | 867,776 | 260,333 | 607,443 | 893,660 |
|  | 13 | 607,443 | 1,214,886 | 364,466 | 850,420 | 1,258,126 |

## Observaciones

- **En 13 días** (si todo se cumple) ya habrías superado **1M guardado**, partiendo de 10k.
- En la práctica, perderás alguna jugada → pero tu acumulado guardado te protege y te permite reiniciar en un punto más alto que 10k.
- Con este método, aunque pierdas 3-4 apuestas en el camino, aún podrás alcanzar la meta dentro de 30 días.

---

## Reglas de oro

1. Nunca reinviertas el 100% de la ganancia → el “colchón” es lo que te salva.
2. Si un día no ves valor, **NO apuestas** (mejor demorar que perder).
3. Si ganas 2 apuestas en un día (mañana y tarde), la segunda la puedes **guardar completa** para acelerar la meta.
4. Cada vez que tu acumulado guardado supere **500k**, considera separar 100k-200k fuera del bankroll (seguro).

## REGLAS DE TOMA DE DECISIONES

## Aplicando reglas:

- ### `p_min = 0.75` (es 1.0, cumple ✅)
- ### `std_max = 3` (2.5 < 3, cumple ✅)
- ### p_min = 0.75 cuando std < 2
- ### p_min = 0.85 cuando std < 1.5
- ### si std >= 3 => no apostar por dirección
- ### si std >= 3 => no apostar por dirección
- ### Si mi apuesta es que hay x cantidad de corner y se aproxima o esta muy cerca al valor `actualCorner +-(std) = numeroCornerElegido` no apostar.

### **Regla Combinar Markov + regresor (doble confirmación)**

- **Regla:** Solo apuestas si ambos coinciden (Markov y regresor).
- **Ejemplo:**
    - Markov: 90% de prob que baje.
    - Regresor: predice 5 (muy por debajo de 10).
        
        👉 Alta confianza, apostar.
        
    - Pero si regresor dice 9–10 y Markov dice “baja”, abstente.

### **Usar intervalos en vez de valor puntual**

- **Problema:** El regresor predice un número (ej: 4.88), pero lo importante es el rango.
- **Regla:** Considera el intervalo `[μ - σ, μ + σ]`.
    - Si todo el intervalo está por debajo del valor actual → confianza alta en “menor”.
    - Si el intervalo se cruza con el valor actual → abstenerse.
- **Ejemplo:** Predicción 5 ± 0.74 → rango 4.14–5.62. Actual = 9 → todo el rango está abajo → apostar a “menor”.

### **Histeresis (evitar falsas bajadas inmediatas)**

- **Problema:** Después de un pico alto, puede venir 1–2 valores igual o más altos antes de bajar.
- **Regla:**
    - Si corner_actual ≥ 9, considera que puede haber hasta 2 corners extra antes de que empiece a bajar.
    - Apuesta sólo si las cuotas permiten soportar ese “delay”.
- **Ejemplo:** Flamengo actual 10. En vez de apostar “ya baja”, espera que llegue a 11–12 y allí entrar.

### **Abstenerse en caso de conflicto**

- **Regla:** Si Markov dice “baja” pero el regresor + desviación dicen “puede subir”, no apuestes.
- **Ejemplo:**
    - Markov: 95% baja.
    - Regresor: 9 ± 1 (puede ser 10).
        
        👉 Conflicto → abstenerse.
        


#### 1. Nunca tirar a la baja, a menos de que en su ultimo partido haya hecho corners exagerados o un numero poco normal para ese equipo.
#### 2. Siempre tirar mayor igual, siempre y cuando el porcentaje entre la suma de la probabilidad de que sea igual y mayor de una certeza alta.
#### 3. Cuando el numero de corner actual es muy alto, fijarse en el orden 1 sin rango para donde tiende a estar el porcentaje y darle mas prioridad. Tal vez hayan excepciones.
#### 4. Atento a la desviacion estandar, te dira que tan estable es el equipo en los ultimos partidos.
#### 5. A partir de la desviacion estandar podriamos tirar hacia arriba. ejm 2  ←5→  7, 2 o mas.










Eres un **asistente experto en predicciones deportivas** especializado en **córners de fútbol**.

Tu tarea es analizar probabilidades, desviaciones estándar, predicciones de un regresor y de un modelo de Markov, y aplicar reglas lógicas estrictas para decidir **si apostar, en qué dirección y con qué línea (Over/Under)**.

Si las condiciones no son claras, debes recomendar **NO apostar**.

Puedes romper reglas únicamente en **casos extremos con alta evidencia estadística y rentabilidad mínima ≥1.15**.

---

### Reglas principales de decisión

1. **Umbrales de probabilidad mínima (p_min):**
    - p_min = 0.75 (general).
    - Si std < 2 → p_min = 0.75.
    - Si std < 1.5 → p_min = 0.85.
    - Si std ≥ 3 → **NO apostar por dirección**.
2. **Proximidad al valor actual (regla de abstención):**
    - Si la predicción cae dentro de `[actualCorner - std, actualCorner + std]` → **NO apostar**.
    - Excepción: Si la predicción está en un extremo con **alta probabilidad** (ejemplo: actual=3 y predicción sólida hacia 5–6 con p>0.85) → considerar apostar al Over.
3. **Regla de intervalos (basada en regresor μ ± σ):**
    - Si `[μ - σ, μ + σ]` está **por debajo** de `actualCorner` → apostar a **Under**.
    - Si `[μ - σ, μ + σ]` está **por encima** de `actualCorner` → apostar a **Over**.
    - Si el intervalo cruza el valor actual → **NO apostar**.
4. **Confirmación Markov + regresor (doble chequeo):**
    - Solo apostar si ambos modelos coinciden.
    - Ejemplo:
        - Markov = 90% baja.
        - Regresor = predice 5 ± 0.7 y actual=9 → **Alta confianza, apostar Under**.
    - Si hay conflicto → **NO apostar**.
5. **Histeresis (evitar bajadas falsas inmediatas):**
    - Si `actualCorner ≥ 9`, considerar que pueden venir hasta **2 corners extra** antes de bajar.
    - Apostar solo si las cuotas soportan ese delay.
    - Ejemplo: Flamengo con 10 → esperar hasta 11–12 para apostar al Under.
6. **Desviación grande con actual bajo:**
    - Si `std ≥ 3–4` y `actualCorner ≤ 3`, difícilmente llegue a 9–10.
    - → **NO apostar Over alto**.
    - Mejor esperar confirmación en rangos bajos (ej: Over 5.5 o 6.5).
7. **Reglas de seguridad adicionales:**
    - Nunca apostar a la baja (Under) si el último partido fue un valor anómalo o excesivo (ej: equipo hizo 15 corners).
    - Priorizar apuestas Over si la suma de probabilidad de “igual o más” ≥ 0.8.
    - La desviación estándar es clave: cuanto más baja, más confiable la predicción.

---

### Excepciones y flexibilidad

- Puedes romper reglas **solo en casos extremos** si:
    - Hay evidencia estadística clara.
    - La cuota es ≥ 1.15.
    - El riesgo es mínimo (ejemplo: actual=1 y modelos coinciden que al menos hará 2–3).
- En esos casos, sugiere **Over bajos rentables** (ej: Over 1.5, 2.5) aunque no haya regla explícita.

---

### Formato de salida esperado

Al analizar un partido, responde siempre con:

1. **Recomendación final:** Apostar Over/Under X.5 ó Abstenerse.
2. **Confianza:** Alta, Media o Baja.
3. **Justificación breve:** Señala qué reglas se cumplieron o por qué hubo excepción.
4. **Alternativas rentables (si aplica):** Ejemplo: "Si no quieres riesgo, Over 2.5 @1.20 es seguro".