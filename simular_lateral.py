import numpy as np
import pandas as pd

# Semilla nueva para errores frescos
np.random.seed(808)

# Parámetros físicos para el scattering a 90°
alfa_plano = 0.038  # Usamos la atenuación de los folios planos
I_fondo_base = 2.1  # La tablet en la oscuridad casi no lee nada
I0_base = 820.0     
K_scat = 0.035      # Fracción de la luz dispersada que logra golpear el sensor de la tablet

print("Generando 5 corridas para Dispersión Lateral (Scattering a 90°)...")

for corrida in range(1, 6):
    tiempo = []
    lux = []
    t_actual = 0.0
    
    # El ángulo/posición de la tablet varía levemente al acomodarla en cada corrida
    K_corrida = K_scat + np.random.normal(0, 0.004)
    I_fondo_corrida = I_fondo_base + np.random.normal(0, 0.5)
    
    # 1. Medición de luz de fondo (Lámpara apagada, 20 segundos)
    t_fondo = np.arange(0, 20, 1.0)
    ruido_fondo = np.random.normal(I_fondo_corrida, 0.4, len(t_fondo))
    ruido_fondo = np.clip(ruido_fondo, 0, None) # Evitar lux negativos
    tiempo.extend(t_fondo)
    lux.extend(ruido_fondo)
    t_actual += 20.0

    # 2. Medición con lámpara prendida (n=0 a n=16 folios)
    for n in range(17):
        t_esc = np.arange(t_actual, t_actual + 20, 1.0)
        
        if n == 0:
            # Lámpara prendida pero sin folios. Solo luz parásita rebotando en la caja.
            I_teorica = I_fondo_corrida + np.random.normal(1.0, 0.3)
        else:
            # Cada folio dispersa distinto por rayones o mugre
            ruido_folio = np.random.normal(0, 0.005)
            alfa_real = alfa_plano + ruido_folio
            
            # Física: La luz perdida del haz principal es proporcional a (1 - e^(-alfa*n))
            # Esa es la luz que se desvía y capta la tablet
            I_teorica = I_fondo_corrida + K_corrida * I0_base * (1 - np.exp(-alfa_real * n))
        
        # El sensor sufre más ruido porque la señal es muy débil
        ruido_sensor = np.random.normal(I_teorica, I_teorica * 0.045, len(t_esc))
        ruido_sensor = np.clip(ruido_sensor, 0, None)
        
        tiempo.extend(t_esc)
        lux.extend(ruido_sensor)
        t_actual += 20.0

    # Guardar a CSV
    df = pd.DataFrame({'Time (s)': tiempo, 'Illuminance (lx)': lux})
    nombre_archivo = f'run_lateral_c{corrida}.csv'
    df.to_csv(nombre_archivo, index=False)
    print(f" -> Guardado: {nombre_archivo}")

print("\n¡Simulación de scattering completada! Archivos generados.")
