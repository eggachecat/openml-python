"""
Tasks
=====

A tutorial on how to fetch evalutions on a task.
"""

import openml
# import pandas as pd
from pprint import pprint

############################################################################
#
# Evalutions contain details (IDs and names) of data, flow, tasks, of all runs
# and the resulting results that was uploaded for those settings.
# The listing functions take optional parameters which can be used to filter
# results and fetch only the evaluations required.
#
# In this example, we'll primarily see how to retrieve the results for a
# particular task and attempt to compare performance of different runs.

############################################################################
# Listing evaluations
# ^^^^^^^^^^^^^^^^^^^
#
# We shall retrieve a small set to test the listing function for evaluations
openml.evaluations.list_evaluations(function='predictive_accuracy', size=10,
                                    output_format='dataframe')
# Using other evaluation metrics
openml.evaluations.list_evaluations(function='precision', size=10,
                                    output_format='dataframe')

# Listing tasks
# ^^^^^^^^^^^^^
#
# We will start by displaying a simple *supervised classification* task:
task_id = 167140        # https://www.openml.org/t/167140
task = openml.tasks.get_task(task_id)
pprint(vars(task))

# Obtaining all the evaluations for the task
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
metric = 'predictive_accuracy'
evals = openml.evaluations.list_evaluations(function=metric, task=[task_id],
                                            output_format='dataframe')
# Displaying the first 10 rows
pprint(evals.head(n=10))
# Sorting the evaluations in decreasing order of the metric chosen
evals = evals.sort_values(by='value', ascending=False)
pprint(evals.head())

# Obtain CDF of metric for chosen task
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
from matplotlib import pyplot as plt


def plot_cdf(values, metric='predictive_accuracy'):
    plt.hist(values, density=True, histtype='step', cumulative=True, linewidth=3)
    plt.xlim(max(0, min(values) - 0.1), 1)
    plt.title('CDF')
    plt.xlabel(metric)
    plt.ylabel('Likelihood')
    plt.grid(b=True, which='major', linestyle='-')
    plt.grid(b=True, which='minor', linestyle='--')
    plt.show()


plot_cdf(evals.value, metric)

# Compare top 10 performing flows
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
import numpy as np
import pandas as pd


def plot_flow_compare(evaluations, top_n=10, metric='predictive_accuracy'):
    # Collecting the top 10 performing unique flow_id
    flow_list = np.unique(evaluations.flow_id)[:10]

    df = pd.DataFrame()
    for i in range(len(flow_list)):
        df = pd.concat([df, pd.DataFrame(evaluations[evaluations.flow_id == flow_list[i]].value)],
                       ignore_index=True, axis=1)
    fig, axs = plt.subplots()
    df.boxplot()
    axs.set_title('Boxplot comparing ' + metric + ' for different flows')
    axs.set_ylabel(metric)
    axs.set_xlabel('Flow ID')
    axs.set_xticklabels(flow_list)
    flow_freq = list(df.count(axis=0, numeric_only=True))
    print(len(flow_freq), flow_freq)
    print(len(flow_list), flow_list)
    for i in range(len(flow_list)):
        axs.text(i + 1.05, np.nanmin(df.values), str(flow_freq[i]) + ' run(s)')
    plt.show()


plot_flow_compare(evals, metric=metric)