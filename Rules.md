## Aplicando reglas:

- `p_min = 0.75` (es 1.0, cumple ✅)
- `s_max = 3` (2.5 < 3, cumple ✅)
- p_min = 0.75 cuando std < 2
- p_min = 0.85 cuando std < 1.5
- si std >= 3 => no apostar por dirección
- si std >= 3 => no apostar por dirección

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