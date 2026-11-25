"""Router de la calculadora: redirige cada solicitud al tópico de su rol.

Ejecuta uno por equipo, cada uno con su prioridad de relevo (1 = principal):
    python router.py --prioridad 1      (equipo 1)
    python router.py --prioridad 2      (equipo 2: en espera, relevo del 1)
    python router.py --prioridad 3      (equipo 3: en espera, relevo del 2)
Solo el de mejor prioridad que siga vivo trabaja; si cae, toma el mando el siguiente.
"""
import argparse
import sys

from kafka_nodo.enrutador import ejecutar_router
from kafka_nodo.kafka_util import ClusterIncompleto
from kafka_nodo.utilidades import imprimir_seguro

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--prioridad", type=int, default=1, help="1 = principal; mayor número = más abajo en la cola de relevo")
    try:
        ejecutar_router(ap.parse_args().prioridad)
    except ClusterIncompleto as e:
        imprimir_seguro(f"[ERROR] {e}")
        sys.exit(1)
