import random

# Definição dos parâmetros
params = {
    "NP": {"type": "c", "values": [2]},
    "PS": {"type": "i", "values": (10, 20)},
    "alpha": {"type": "i", "values": (5, 20)},
    "T": {"type": "i", "values": (1000, 3000)},
    "max_iter": {"type": "i", "values": (10000, 80000)},
    "scale_factor": {"type": "r", "values": (0.50, 3.00)},
    "is_obl": {"type": "c", "values": [0, 1]},
}

def generate_random_config():
    config = {}
    for name, spec in params.items():
        if spec["type"] == "c":
            config[name] = random.choice(spec["values"])
        elif spec["type"] == "i":
            config[name] = random.randint(*spec["values"])
        elif spec["type"] == "r":
            config[name] = round(random.uniform(*spec["values"]), 2)
    return config

# Exemplo de uso
if __name__ == "__main__":
    random_config = generate_random_config()

    # Imprime cada parâmetro em uma linha
    for k, v in random_config.items():
        print(f"{k}: {v}")

    print("\n--- Valores em linha ---")
    # Só os valores em uma linha
    values_only = " ".join(str(v) for v in random_config.values())
    print(values_only)
