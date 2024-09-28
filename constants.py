from pathlib import Path

INSTANCES = [f"F{i}.DAT" for i in range(1, 10)]# + [f"G{i}.DAT" for i in range(1, 76)]
# INSTANCES = ["F1.DAT",
#               "G12.DAT",
#               "G53.DAT"]
MAQUINAS = [2]
NUM_POINTS = 10
FAST_TIMELIMIT = 20
TIMELIMIT = 3600

CAPACIDADES_PATH = Path.resolve(Path.cwd() / "resultados" / "capacidades.xlsx")
RESULTADOS_INDIVIDUAIS_PATH = Path.resolve(Path.cwd() / "resultados" / "individuais")
OTIMIZADOS_INDIVIDUAIS_PATH = Path.resolve(Path.cwd() / "resultados" / "otimizados")
DETALHADOS_INDIVIDUAIS_PATH = Path.resolve(Path.cwd() / "resultados" / "detalhados")
FINAL_PATH = Path.resolve(Path.cwd() / "resultados")

IDEAL_CAPACITY = 75
