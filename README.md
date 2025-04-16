# 📊 PokemonProject

> Small machine learning project using **Pytorch** for training and evaluation.  
This project serves as a starter template or sandbox for developing and testing models with clean structure.

---

## 📦 Installation

```bash
# Create a virtual environment
python -m venv .venv

# Activate the environment
# On Windows
.venv\Scripts\activate

# On Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
---

## 🗂️ Project Structure
```bash
pokemonML/
│
├── main.py               # Entry point – model training or evaluation
├── check_pytorch.py
├── pokemonml/
│   └── __init__.py
│   └── create_pokemon.py
│   └── display.py
│   └── moves.py
│   └── pokemon_damage_calculator.py
│   └── right_move_machine.py
│   └── stats.py
│   └── utils.py
│
├── data/                 # Input dataset directory
│   └── chart.csv
│   └── moves.csv
│   └── pokemon.csv
│
├── models/         # Folder where trained models are saved
│
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```
---
