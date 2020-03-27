from OpenDSS import OpenDSS


path_ovelhas = 'Sistema_copel/Ovelhas.dss'

sys = OpenDSS(path = path_ovelhas, kV = 13.8, loadmult = 1)

sys.run_openDSS()
df = sys.get_all_v_pu_pandas()

