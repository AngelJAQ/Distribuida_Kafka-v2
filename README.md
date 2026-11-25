# Distribuida_Kafka

Chat por tópicos + calculadora distribuida sobre un cluster Kafka de 3 equipos (KRaft).
Todo corre con Docker Compose: no hace falta instalar Python ni Kafka, solo Docker.

## Qué levanta cada equipo

| Servicio  | Qué hace                                                     |
|-----------|--------------------------------------------------------------|
| `kafka`   | Broker del cluster (los 3 forman el cuórum)                  |
| `router`  | Router de la calculadora; prioridad de relevo = `NODE_ID`    |
| `nodo`    | Nodo de cálculo; atiende los roles de `NODO_ROLES`           |
| `cliente` | Consola de chat + calculadora (bajo demanda, no arranca solo)|

## Puesta en marcha (repetir en CADA equipo)

1. Abre los puertos **9092** y **9093** (TCP) en el firewall de cada equipo.
2. `cp equipo.env.ejemplo equipo.env` y edítalo:
   - `NODE_ID`: 1, 2 o 3 (distinto en cada equipo; define la prioridad de relevo)
   - `MI_IP`: IP de ese equipo en la red
   - `IP_PC1`, `IP_PC2`, `IP_PC3`: las 3 IP (idénticas en los 3 equipos)
   - `NODO_ROLES`: `todos` o una lista, p. ej. `suma resta`
3. Levanta el sistema:

   ```bash
   docker compose --env-file equipo.env up -d --build
   docker compose --env-file equipo.env ps
   ```

   Hasta que haya al menos 2 brokers arriba, `router` y `nodo` se reinician solos
   mientras esperan al cuórum; es normal.

## Cliente interactivo

```bash
docker compose --env-file equipo.env run --rm cliente                    # solo cliente
docker compose --env-file equipo.env run --rm cliente --rol suma resta   # cliente + roles
docker compose --env-file equipo.env run --rm cliente --rol todos
```

## Utilidades

```bash
docker compose --env-file equipo.env logs -f router     # ver qué router está ACTIVO
docker compose --env-file equipo.env logs -f nodo
docker compose --env-file equipo.env stop router        # simular caída del router de este equipo
docker compose --env-file equipo.env down               # apagar (conserva los datos de Kafka)
docker compose --env-file equipo.env down -v            # apagar y BORRAR los datos de Kafka
```

## Pruebas de relevo entre equipos

- Apaga el equipo 1 (o `stop router` / `stop kafka`): el router y el broker de prioridad 2 toman el mando.
- Al volver el equipo 1 recupera el liderazgo solo (~10 s para el broker).
- Para probar solo la parte de cálculo, usa distintos `NODO_ROLES` por equipo
  (p. ej. PC1 `suma resta`, PC2 `multiplicacion division`, PC3 `potencia modulo raiz`).

## Sin Docker (opcional)

`pip install -r requirements.txt` y `python router.py --prioridad N`, `python nodo_calculo.py todos`,
`python cliente.py`. Los brokers se leen de la variable `KAFKA_SERVER` o de `kafka_servidores.txt`.
