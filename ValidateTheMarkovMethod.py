import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


# ============================
# Funciones auxiliares
# ============================

def get_transition_counts(values, order=1, bins=None):
    """
    Calcula las transiciones para un Markov de 1er o 2do orden.
    values: lista de córners
    order: 1 o 2
    bins: lista de cortes para binning (opcional)
    """
    if bins is not None:
        values = pd.cut(values, bins=bins, labels=False, include_lowest=True)

    transitions = {}
    n = len(values)

    for i in range(order, n - 1):
        state = tuple(values[i - order:i]) if order > 1 else values[i]
        next_state = values[i + 1]

        relation = "igual"
        if next_state > values[i]:
            relation = "mayor"
        elif next_state < values[i]:
            relation = "menor"

        if state not in transitions:
            transitions[state] = {"mayor": 0, "igual": 0, "menor": 0}
        transitions[state][relation] += 1
    return transitions


def get_transition_probs(transitions):
    """
    Convierte conteos en probabilidades.
    """
    probs = {}
    for state, counts in transitions.items():
        total = sum(counts.values())
        if total == 0:
            probs[state] = {"mayor": 0, "igual": 0, "menor": 0}
        else:
            probs[state] = {k: v / total for k, v in counts.items()}
    return probs


def predict_next(probs, current_state):
    """
    Predice la categoría más probable dado el estado actual.
    """
    if current_state not in probs:
        return np.random.choice(["mayor", "igual", "menor"])  # fallback
    return max(probs[current_state], key=probs[current_state].get)


def evaluate(values, order=1, bins=None):
    """
    Entrena Markov con train y evalúa en test.
    """
    # split train-test
    train, test = train_test_split(values, test_size=0.2, shuffle=False)

    # entrenar
    transitions = get_transition_counts(train, order=order, bins=bins)
    probs = get_transition_probs(transitions)

    # predecir en test
    correct = 0
    total = 0
    for i in range(order, len(test) - 1):
        state = tuple(test[i - order:i]) if order > 1 else test[i]
        if bins is not None:
            state = tuple(pd.cut([s], bins=bins, labels=False, include_lowest=True)[0] for s in
                          (test[i - order:i] if order > 1 else [test[i]]))
            if order == 1:
                state = state[0]
            elif order == 2:
                state = tuple(state)

        pred = predict_next(probs, state)

        # verdadero
        next_state = test[i + 1]
        relation = "igual"
        if next_state > test[i]:
            relation = "mayor"
        elif next_state < test[i]:
            relation = "menor"

        if pred == relation:
            correct += 1
        total += 1

    return correct / total if total > 0 else 0


# ============================
# MAIN
# ============================

# Supongamos que tu df tiene la columna "córners"
df = pd.read_csv("./teams_data/Corinthians.csv", sep=";", encoding="utf-8")

values = df["Tiros de esquina"].values

# Evaluar modelos
acc_1 = evaluate(values, order=1)  # 1er orden exacto
acc_2 = evaluate(values, order=2)  # 2do orden exacto
acc_bins = evaluate(values, order=1, bins=[-1, 3, 6, 20])  # 1er orden con bins (ejemplo: pocos, medios, muchos)

print("Accuracy 1er orden:", acc_1)
print("Accuracy 2do orden:", acc_2)
print("Accuracy con bins:", acc_bins)

best_model = max(
    [("1er orden", acc_1),
     ("2do orden", acc_2),
     ("1er orden con bins", acc_bins)],
    key=lambda x: x[1]
)
print("➡️ Mejor modelo:", best_model)
