import os
from itertools import chain
from typing import Dict, List
import types

import numpy as np
import pandas as pd


from pathlib import Path
from read_file import dataCS

try:
    from mpi4py.futures import MPIPoolExecutor
    from mpi4py import MPI

    MPI_BOOL = True
except:
    print("mpi4py not running")
    MPI_BOOL = False

import constants

import gc


def print_info(data: dataCS, status: str) -> None:
    if MPI_BOOL:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
    else:
        rank = None
    print(
        f"Instance = {data.instance} Cap = {data.cap[0]} nmaquinas = {data.r} {status} Process {rank}"
    )


def add_new_kpi(kpis: Dict[str, any], result, data: dataCS) -> dict:
    kpis["Instance"] = data.instance
    kpis["Best Bound"] = result.solve_details.best_bound
    kpis["Gap"] = result.solve_details.gap
    kpis["Nodes Processed"] = result.solve_details.gap
    kpis["Tempo de Solução"] = result.solve_details.time
    kpis["capacity"] = data.cap[0]
    kpis["utilization_capacity"] = (
        100 * kpis.get("used_capacity", 0) / (data.cap[0] * data.r * data.nperiodos)
    )
    kpis["nmaquinas"] = data.r
    return kpis


def closest_to_IDEAL_CAPACITY_percent(
    results_per_instance: List[Dict[str, any]]
) -> Dict[str, any]:
    """Dado uma lista de resultados para uma instância, retorne aquele mais próximo de IDEAL_CAPACITY de utilização da capacidade."""
    return min(
        results_per_instance,
        key=lambda x: abs(x["utilization_capacity"] - constants.IDEAL_CAPACITY),
    )


def choose_capacity(
    dataset: str,
    build_model,
    nmaquinas: int = 2,
    get_closest: bool = True,
) -> None:
    data = dataCS(dataset, r=nmaquinas)
    original_capacity = data.cap[0] / data.r
    instance_results = []

    for cap in np.linspace(
        original_capacity,
        original_capacity * data.r * 2,
        num=constants.NUM_POINTS,
        endpoint=True,
    ):
        mdl, data = build_model(data, np.ceil(cap))
        mdl.parameters.timelimit = constants.FAST_TIMELIMIT
        result = mdl.solve()

        if result == None:
            print_info(data, "infactível")
            continue

        kpis = mdl.kpis_as_dict(result, objective_key="objective_function")
        kpis = add_new_kpi(kpis, result, data)

        assert kpis["utilization_capacity"] <= 100, "Capacidade > 100%"

        instance_results.append(kpis)
        print_info(data, "concluído")
    if get_closest:
        if len(instance_results) > 0:
            df_ideal_capacity = pd.DataFrame(
                [closest_to_IDEAL_CAPACITY_percent(instance_results)]
            )
            data.cap[0] = int(df_ideal_capacity["capacity"].values[0])
            df_ideal_capacity.to_excel(
                f"{constants.RESULTADOS_INDIVIDUAIS_PATH}/{str(data)}.xlsx",
                engine="openpyxl",
            )
    else:
        df_ideal_capacity = pd.DataFrame(instance_results)
        df_ideal_capacity.to_excel(
            f"{constants.RESULTADOS_INDIVIDUAIS_PATH}/{str(data)}.xlsx",
            engine="openpyxl",
        )
    gc.collect()


def running_all_instance_choose_capacity(build_model) -> None:
    # Executando e coletando os resultados
    final_results = []

    if not MPI_BOOL:
        for dataset in constants.INSTANCES:
            for nmaq in constants.MAQUINAS:
                best_result = choose_capacity(dataset, build_model, nmaquinas=nmaq)

                if isinstance(best_result, pd.DataFrame):
                    final_results.append(best_result)
    else:
        with MPIPoolExecutor() as executor:
            futures = executor.starmap(
                choose_capacity,
                (
                    (dataset, build_model, nmaq)
                    for dataset in constants.INSTANCES
                    for nmaq in constants.MAQUINAS
                ),
            )
            final_results.append(futures)
            executor.shutdown(wait=True)

    get_and_save_results(
        path_to_read=constants.RESULTADOS_INDIVIDUAIS_PATH,
        path_to_save=constants.CAPACIDADES_PATH,
    )
    print("Processamento de capacidades concluído.")


def get_and_save_results(path_to_read: str, path_to_save: str) -> None:
    list_files = []
    for file in Path(path_to_read).glob("*"):
        list_files.append(pd.read_excel(file))
    df_results_optimized = pd.concat(list_files)
    df_results_optimized.to_excel(path_to_save, index=False)


def solve_optimized_model(
    dataset: str, build_model, env_formulation: int, nmaquinas: int = 8, capacity: int = 0
) -> None:
    data = dataCS(dataset, r=nmaquinas)
    if capacity > 0:
        data.cap = [capacity]    
    mdl, data = build_model(data, capacity=data.cap[0])
    mdl.parameters.timelimit = constants.TIMELIMIT
    result = mdl.solve()

    if result == None:
        print_info(data, "infactível")
        return None

    kpis = mdl.kpis_as_dict(result, objective_key="objective_function")
    kpis = add_new_kpi(kpis, result, data)

    # Cálculo da relaxação linear
    relaxed_model = mdl.clone()
    status = relaxed_model.solve(url=None, key=None, log_output=False)

    relaxed_objective_value = relaxed_model.objective_value
    kpis["Relaxed Objective Value"] = relaxed_objective_value

    suffix_path = str(data) + "_" + env_formulation
    complete_path_to_save = Path.resolve(
        constants.OTIMIZADOS_INDIVIDUAIS_PATH / suffix_path
    )

    df_results_optimized = pd.DataFrame([kpis])
    df_results_optimized.to_excel(f"{complete_path_to_save}.xlsx", index=False)

    print_info(data, "concluído")
    gc.collect()


def running_all_instance_with_chosen_capacity(
    build_model, path_to_save: str, env_formulation: int
):
    final_results = []

    try:
        pdf_capacidades = pd.read_excel(constants.CAPACIDADES_PATH, engine="openpyxl")
        caps = pd.pivot_table(
            pdf_capacidades, index=["Instance", "nmaquinas"], aggfunc={"capacity": "mean"}
        ).T.to_dict()
    except:
        print("Não foi encontrado arquivo de capacidades. Seguindo com dados default do Trigeiro.")
        caps = {}
        
    if not MPI_BOOL:
        for dataset in constants.INSTANCES:
            for nmaq in constants.MAQUINAS:
                best_result = solve_optimized_model(
                    dataset,
                    build_model,                    
                    nmaquinas=nmaq,
                    capacity=caps.get((dataset, nmaq), {}).get("capacity", 0),
                    env_formulation=env_formulation,
                )

                if best_result:
                    final_results.append(best_result)
    else:
        with MPIPoolExecutor() as executor:
            futures = executor.starmap(
                solve_optimized_model,
                (
                    (
                        dataset,
                        build_model,                        
                        env_formulation,
                        nmaq,
                    )
                    for dataset in constants.INSTANCES
                    for nmaq in constants.MAQUINAS
                ),
            )
            final_results.append(futures)
            executor.shutdown(wait=True)

    get_and_save_results(
        path_to_read=constants.OTIMIZADOS_INDIVIDUAIS_PATH,
        path_to_save=Path.resolve(constants.FINAL_PATH / path_to_save),
    )
    print(f"Concluído {env_formulation}")
