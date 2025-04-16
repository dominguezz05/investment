# 🧠 Dolev-Strong Protocol Simulation

Este módulo implementa una simulación del protocolo de consenso Dolev-Strong descrito en el libro _Foundations of Distributed Consensus and Blockchains_ de Elaine Shi.

---

## 📁 Estructura del proyecto

```
market_sim/
├── consensus/
│   ├── dolev_strong.py         # Lógica del protocolo
│   ├── test_dolev_strong.py   # Pruebas unitarias con unittest
│   └── visualize_consensus.py # Visualización de resultados
```

---

## ⚙️ Cómo funciona

El protocolo permite que un grupo de nodos (algunos potencialmente corruptos) lleguen a un consenso sobre un bit binario enviado por un nodo inicial (el "sender").

- **f + 1 rondas** garantizan el consenso entre nodos honestos.
- **Firmas digitales simuladas** con listas de ID.
- **Detecta fallos bizantinos** y evita la manipulación del mensaje.

---

## ▶️ Ejecución

```bash
python visualize_consensus.py
```

---

## 🧪 Tests

```bash
python -m unittest test_dolev_strong.py
```

---

## 📚 Basado en

> **Capítulo 3: Byzantine Broadcast and the Dolev-Strong Protocol**  
> Foundations of Distributed Consensus and Blockchains — Elaine Shi

---

## 📩 Contacto

Simulación desarrollada como parte de la prueba técnica para Torbellino Tech.  
Para más información: [juan.diez@torbellino.tech](mailto:juan.diez@torbellino.tech)
