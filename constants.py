from pathlib import Path

# INSTANCES = [f"X{i}{j}{k}{l}{m}{n}.DAT" for i in [1] for j in range(1,3) for k in [1,2,4] 
#              for l in range(1,3) for m in range(7,10) for n in ["A", "B", "C", "D", "E"]]

# [f"F{i}.DAT" for i in range(1, 71)] + [f"G{i}.DAT" for i in range(1, 76)] + 
# f"X{i}{j}{k}{l}{m}{n}.DAT" for i in [1,2,3]


# INSTANCES = [#"F1.DAT"
#               #"F25.DAT", 
#               #"G59.DAT", 
#               #"G51.DAT"
#               "X12119B.DAT"
#               ]

# if MAQUINAS == [2]:
#     INSTANCES = ["X11229C.DAT"]
# if MAQUINAS == [4]:
#     INSTANCES = ["X11118A.DAT", "X11118E.DAT", "X11119C.DAT", "X11127C.DAT", "X11128A.DAT", "X11128D.DAT", "X11129A.DAT", "X11218A.DAT", "X11218E.DAT", "X11219E.DAT", "X11227B.DAT", "X11227C.DAT", "X11227E.DAT", "X11228A.DAT", "X11228D.DAT", "X11229A.DAT", "X11419A.DAT", "X11427C.DAT", "X11427D.DAT", "X11428B.DAT", "X11429C.DAT", "X12117A.DAT", "X12118D.DAT", "X12118E.DAT", "X12127C.DAT", "X12127D.DAT", "X12129B.DAT", "X12129C.DAT", "X12129E.DAT", "X12217D.DAT"]
# if MAQUINAS == [6]:
INSTANCES = ["X11117C.DAT", "X11118A.DAT", "X11118E.DAT", "X11119A.DAT", "X11119B.DAT", "X11119C.DAT", "X11127B.DAT", "X11127C.DAT", "X11127E.DAT", "X11128A.DAT", "X11128C.DAT", "X11128E.DAT", "X11129C.DAT", "X11217B.DAT", "X11218B.DAT", "X11227C.DAT", "X11227E.DAT", "X11228C.DAT", "X11228D.DAT", "X11228E.DAT", "X11229A.DAT", "X11229C.DAT", "X11427B.DAT", "X11427E.DAT", "X11428B.DAT", "X12117A.DAT", "X12118D.DAT", "X12119B.DAT", "X12127C.DAT", "X12127E.DAT", "X12128D.DAT", "X12129A.DAT", "X12229D.DAT"]
MAQUINAS = [6]
NUM_POINTS = 10
FAST_TIMELIMIT = 20
TIMELIMIT = 3600

CAPACIDADES_PATH = Path.resolve(Path.cwd() / "resultados" / "capacidades.xlsx")
RESULTADOS_INDIVIDUAIS_PATH = Path.resolve(Path.cwd() / "resultados" / "individuais")
OTIMIZADOS_INDIVIDUAIS_PATH = Path.resolve(Path.cwd() / "resultados" / "otimizados")
DETALHADOS_INDIVIDUAIS_PATH = Path.resolve(Path.cwd() / "resultados" / "detalhados")
FINAL_PATH = Path.resolve(Path.cwd() / "resultados")

IDEAL_CAPACITY = 75
