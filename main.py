from utils import (
    running_all_instance_choose_capacity,
    running_all_instance_with_chosen_capacity,
)
from context import ProjectContext
from zero_formulation import build_model as classical_formulation_build_model
from first_formulation import build_model as first_formulation_build_model
from second_formulation import build_model as second_formulation_build_model
from third_formulation import build_model as third_formulation_build_model
from fourth_formulation import build_model as fourth_reformulation_build_model

if __name__ == "__main__":
    # for num in [1]:
    context = ProjectContext(f"experimentos/experimento1.yml", 1)
    #     running_all_instance_choose_capacity(
    #         context,
    #         classical_formulation_build_model,
    #     )
    # running_all_instance_with_chosen_capacity(
    #     classical_formulation_build_model,
    #     path_to_save="otimizados0.xlsx",
    #     env_formulation="0_ref",
    # )
    running_all_instance_with_chosen_capacity(
        context,
        first_formulation_build_model,
        path_to_save=f"otimizados_1_experiment_1.xlsx",
        env_formulation="1_ref",
    )
    running_all_instance_with_chosen_capacity(
        context,
        second_formulation_build_model,
        path_to_save=f"otimizados_2_experiment_1.xlsx",
        env_formulation="2_ref",
    )
    running_all_instance_with_chosen_capacity(
        context,
        third_formulation_build_model,
        path_to_save=f"otimizados_3_experiment_1.xlsx",
        env_formulation="3_ref",
    )
    running_all_instance_with_chosen_capacity(
        context,
        fourth_reformulation_build_model,
        path_to_save="otimizados_4_experiment_1.xlsx",
        env_formulation="4_ref",
    )
