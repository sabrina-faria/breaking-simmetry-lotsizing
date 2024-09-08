from utils import (
    running_all_instance_choose_capacity,
    running_all_instance_with_chosen_capacity,
)
from context import ProjectContext
from zero_formulation import build_model as classical_formulation_build_model
from first_formulation import build_model as first_formulation_build_model
from second_formulation import build_model as second_formulation_build_model
from third_formulation import build_model as third_formulation_build_model
from fourth_formulation import build_model as fourth_formulation_build_model
from fifth_formulation import build_model as fifth_formulation_build_model
from sixth_formulation import build_model as sixth_formulation_build_model
from seventh_formulation import build_model as seventh_formulation_build_model
from eigth_formulation import build_model as eigth_formulation_build_model
from ninth_formulation import build_model as ninth_formulation_build_model
from eleventh_formulation import build_model as eleventh_formulation_build_model
from twelfth_formulation import build_model as twelfth_formulation_build_model
from thirteenth_formulation import build_model as thirteenth_formulation_build_model

if __name__ == "__main__":
    # Mapeamento de números para formulações e seus respectivos modelos
    formulations = {
        0: ("0_ref", classical_formulation_build_model),
        1: ("1_ref", first_formulation_build_model),
        2: ("2_ref", second_formulation_build_model),
        3: ("3_ref", third_formulation_build_model),
        4: ("4_ref", fourth_formulation_build_model),
        5: ("5_ref", fifth_formulation_build_model),
        6: ("6_ref", sixth_formulation_build_model),
        7: ("7_ref", seventh_formulation_build_model),
        8: ("8_ref", eigth_formulation_build_model),
        9: ("9_ref", ninth_formulation_build_model),
        11: ("11_ref", eleventh_formulation_build_model),
        12: ("12_ref", twelfth_formulation_build_model),
        13: ("13_ref", thirteenth_formulation_build_model),
    }

    # Defina quais formulações deseja rodar usando números
    formulations_to_run = [7]  # Altere essa lista conforme necessário

    for num in [10]:
        context = ProjectContext(f"experimentos/experimento{num}.yml", num)

        for formulation_number in formulations_to_run:
            if formulation_number in formulations:
                env_formulation, build_model = formulations[formulation_number]
                # Ajuste o path_to_save para incluir o número do experimento e a formulação
                path_to_save = f"otimizados_{formulation_number}_experiment_{num}.xlsx"

                running_all_instance_with_chosen_capacity(
                    context,
                    build_model,
                    path_to_save=path_to_save,
                    env_formulation=env_formulation,
                )
            else:
                print(f"Formulação {formulation_number} não encontrada.")
