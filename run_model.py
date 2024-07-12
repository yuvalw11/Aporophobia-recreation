import argparse
import pathlib
import multiprocessing as mp
from itertools import chain, combinations
from model import CityModel, lista_distritos
from data import all_norms

parser = argparse.ArgumentParser(description="Run a sample of models.")
parser.add_argument('-P', default='.', type=str, help="Path to save results")
parser.add_argument('-N', default=100, type=int, help="number of agents")
parser.add_argument('-T', default=100, type=int, help="number of time steps")
parser.add_argument('-M', default=100, type=int, help="number of samples per \
                    norm configuration")

args = parser.parse_args()
path = args.P
N, T, M = args.N, args.T, args.M


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def from_combinations(norms, combinations):
    return [[norms[i] for i in combination] for combination in combinations]


def run_model(I):
    process_id = mp.current_process().pid

    for index, norm_config in enumerate(from_combinations(all_norms, [[],[0],[1],[2],[3],[4],[5],[0,1,2],[3,4,5]])):
        norms_indicator = f"{index}:{'-'.join([str(all_norms.index(norm)) for norm in norm_config])}"
        for i in range(I):

            for norm in norm_config:
                norm.count = 0

            barcelona = CityModel('Barcelona', lista_distritos, N, norm_config)
            for j in range(T):
                print(f'step {j}/{T} simulation id: {process_id}:{i}, norms config: {norms_indicator}')
                barcelona.step()

            # collect and save data
            run_id = f"{process_id}_{norms_indicator}_{i}"
            model_vars_df = barcelona.datacollector.get_model_vars_dataframe()
            agent_vars_df = barcelona.datacollector.get_agent_vars_dataframe()
            model_vars_df.to_csv(f"{path}/model_vars_{run_id}.csv", sep=';')
            agent_vars_df.to_csv(f"{path}/agent_vars_{run_id}.csv", sep=';')

            for norm in norm_config:
                pathlib.Path(f'{path}/Norm Config: {norms_indicator} Norm: {all_norms.index(norm)} RunID:{i}.txt').write_text(str(norm.count))


def distribute(runs, cpus):
    base, extra = divmod(runs, cpus)
    return [base + (i < extra) for i in range(cpus)]


if __name__ == '__main__':

    n_cpus = mp.cpu_count()

    pool = mp.Pool(n_cpus)
    _ = pool.map(run_model, distribute(M, n_cpus))
    pool.close()
