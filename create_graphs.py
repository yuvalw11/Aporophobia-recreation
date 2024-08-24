import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import pathlib
from itertools import chain, combinations


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def load_data_for_norms(config_id):
    datasets = []
    full_datasets = []

    for file in pathlib.Path('./my_results').iterdir():
        if 'agent_vars' not in str(file):
            continue
        
        file_parameters = file.name.split('_')
        run_id = int(file_parameters[3])
        norm_config_id = int(file_parameters[3])
        norm_ids_string = f'({", ".join(file_parameters[4].split("-"))})'
        if norm_config_id != config_id:
            continue

        dataset = pd.read_csv(str(file), delimiter=";")
        dataset['RunId'] = run_id # Indicates the id of the norm configuration
        dataset['IterationId'] = f'{file_parameters[2]}_{file_parameters[4].split(".")[0]}' # indicates the id of the iteration within a specific run id
        dataset['norms_ind'] = str(norm_ids_string)
        datasets.append(dataset.loc[dataset['Step'] == dataset['Step'].max()])
        full_datasets.append(dataset)
    
    cluster = pd.concat(datasets)
    cluster.reset_index(drop=True, inplace=True)
    full_cluster = pd.concat(full_datasets)
    full_cluster.reset_index(drop=True, inplace=True)

    return cluster


def create_graph(cluster):
    fig, axs = plt.subplots(1, 1, figsize=(6, 4))

    gini_coefficients = []
    assert len(cluster['IterationId'].unique()) == 10
    for iteration_id in cluster['IterationId'].unique():
        values = cluster[cluster['IterationId'] == iteration_id]
        wealth_values = np.sort(values['wealth'])
        cumulative_wealth = np.cumsum(wealth_values)
        cumulative_percentage = cumulative_wealth / np.sum(wealth_values)

        n = len(cumulative_percentage)
        area_under_curve = np.trapz(cumulative_percentage, dx=1/n)
        area_of_inequality = 0.5 - area_under_curve
        gini_coefficient = area_of_inequality / 0.5
        gini_coefficients.append(gini_coefficient)

    # Plot the distribution of wealth for the current combination with a unique color
    sns.histplot(data=cluster, x='wealth', bins=20, color='grey', ax=axs, stat='frequency', kde=True)
    homeless_wealth = cluster[cluster['status'] == 'homeless']['wealth']

    # Plot the colored square with Gini coefficient text
    axs.text(0.55, 0.78, f'Gini: {np.average(gini_coefficients):.2f} ± {np.std(gini_coefficients):.2f}', weight='bold', fontsize=11, transform=axs.transAxes)
    square_color = 'grey'
    frame = plt.Rectangle((0.5, 0.75), 0.4, 0.10, fill=False, edgecolor=square_color, linewidth=2, transform=axs.transAxes)
    axs.add_patch(frame)

    axs.set_xlabel('Wealth (EUR)')
    axs.set_ylabel('Frequency')
    norms = cluster["norms_ind"].unique()
    assert len(norms) == 1
    axs.set_title(norms[0])

    plt.savefig(f'./graphs/{norms[0]}.png')


for i in range(64):
    print(i)
    cluster = load_data_for_norms(i)
    create_graph(cluster)
