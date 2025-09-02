import pandas as pd
import numpy as np

class MarkovMethod():
    def build_markov_model(self, values, order=1, bins=None):
        """
        Construye el modelo de Markov (1er o 2do orden, con o sin bins).

        values: lista o array de valores (ej. córners)
        order: 1 o 2
        bins: lista de cortes para binning (ej. [-1,3,6,20]) o None
        """
        if bins is not None:
            values = pd.cut(values, bins=bins, labels=False, include_lowest=True)

        transitions = {}
        n = len(values)

        for i in range(order, n - 1):
            state = tuple(values[i - order:i]) if order > 1 else values[i]
            next_state = values[i + 1]

            relation = "p_igual"
            if next_state > values[i]:
                relation = "p_mayor"
            elif next_state < values[i]:
                relation = "p_menor"

            if state not in transitions:
                transitions[state] = {"p_mayor": 0, "p_igual": 0, "p_menor": 0}
            transitions[state][relation] += 1

        # convertir a probabilidades
        probs = {}
        for state, counts in transitions.items():
            total = sum(counts.values())
            if total > 0:
                probs[state] = {k: v / total for k, v in counts.items()}
            else:
                probs[state] = {"p_mayor": 0, "p_igual": 0, "p_menor": 0}
        return probs


    def get_probabilities(self, model, current_state, order=1, bins=None):
        """
        Obtiene las probabilidades de mayor/igual/menor dado un estado actual.

        model: dict generado con build_markov_model
        current_state: valor actual (o secuencia si es orden 2)
        order: 1 o 2
        bins: lista de cortes para binning (o None)
        """
        if bins is not None:
            # Crear etiquetas para los rangos
            range_labels = []
            for i in range(len(bins) - 1):
                range_labels.append(f"{bins[i] + 1 if i > 0 else bins[i]}-{bins[i + 1]}")

            if order == 1:
                current_state_binned = pd.cut([current_state], bins=bins, labels=False, include_lowest=True)[0]
            elif order == 2:
                current_state_binned = tuple(pd.cut(current_state, bins=bins, labels=False, include_lowest=True))
        else:
            current_state_binned = current_state

        if order == 1:
            state = current_state_binned
        elif order == 2:
            state = tuple(current_state_binned)

        probabilities = model.get(state, {"p_mayor": 0, "p_igual": 0, "p_menor": 0})

        # Si se usan bins, convertir las claves a rangos
        if bins is not None:
            # Obtener el rango actual
            current_range_index = current_state_binned if order == 1 else current_state_binned[-1]
            current_range = range_labels[current_range_index]

            # Crear nuevo diccionario con rangos
            ranged_probs = {}
            for relation, prob in probabilities.items():
                if relation == "p_mayor":
                    if current_range_index < len(range_labels) - 1:
                        ranged_probs[range_labels[current_range_index + 1]] = prob
                    else:
                        ranged_probs["fuera_de_rango"] = prob
                elif relation == "p_menor":
                    if current_range_index > 0:
                        ranged_probs[range_labels[current_range_index - 1]] = prob
                    else:
                        ranged_probs["fuera_de_rango"] = prob
                else:  # igual
                    ranged_probs[current_range] = prob

            return ranged_probs

        return probabilities


    # ============================
    # EJEMPLO DE USO
    # ============================

    def exec_model(self, values= None, estado_actual = None):
        # Supongamos que tienes un df con tu columna "córners"
        #df = pd.read_csv(f"./teams_data/Botafogo.csv", sep=";", encoding="utf-8")
        #df = df.head(100)
        #values = df["Tiros de esquina"].values

        # Crear modelo de 1er orden exacto
        model_1 = self.build_markov_model(values, order=1)

        # Crear modelo de 2do orden con bins
        bins = [-1, 3, 6, 15]  # ejemplo: pocos (0-3), medios (4-6), muchos (7+)
        model_2_bins = self.build_markov_model(values, order=1, bins=bins)

        # Probabilidades para un estado actual
        #estado_actual = 7  # ejemplo: hoy el equipo hizo 5 córners
        print("Probabilidades con modelo de 1er orden:", self.get_probabilities(model_1, estado_actual, order=1))

        # Probabilidades con estado de 2 partidos anteriores (ejemplo: 4 y 5 córners)
        print("Probabilidades con modelo de 1er orden con bins:",
              self.get_probabilities(model_2_bins, estado_actual, order=1, bins=bins))

if __name__ == "__main__":
    markovMethod = MarkovMethod()
    markovMethod.exec_model()
