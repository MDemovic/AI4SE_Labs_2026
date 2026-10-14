"""Reproduce Task 4 tables, paired tests, error examples, and Matplotlib figures.
Run from repository root: python Week_03_Prompting/Assignments/Task_4/analyze_results.py
Requires matplotlib and numpy. Reuses Task 3's standard-library evaluation.
"""
import csv
import importlib.util
import itertools
import json
import re
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
TASK2 = HERE.parent / 'Task_2'
TASK3 = HERE.parent / 'Task_3'
NAMES = ['ICIO', 'REACT', 'SCOPE']
DISPLAY = ['ICIO', 'ReAct', 'SCOPE']
COLORS = ['#3178A8', '#2B997D', '#8665AF']


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))


def write_csv(name, rows):
    with (HERE / name).open('w', encoding='utf-8', newline='') as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def paired_test(a, b):
    """Two-sided sign-flip test on paired mean differences.

    Swap prompt labels within each question. Zero differences do not change
    the statistic. If all differences are zero, the exact p-value is 1.
    """
    differences = np.asarray(a) - np.asarray(b)
    nonzero = differences[differences != 0]
    observed = float(differences.mean())
    if not len(nonzero):
        return observed, 1.0, 'exact: all paired differences zero'
    threshold = abs(float(differences.sum()))
    if len(nonzero) <= 18:
        total = 2 ** len(nonzero)
        extreme = sum(
            abs(float(np.dot(signs, nonzero))) >= threshold - 1e-12
            for signs in itertools.product([-1, 1], repeat=len(nonzero))
        )
        return observed, extreme / total, 'exact sign-flip enumeration'
    rng = np.random.default_rng(20261014)
    signs = rng.choice([-1, 1], size=(10000, len(nonzero)))
    extreme = np.sum(np.abs(signs @ nonzero) >= threshold - 1e-12)
    return observed, float((extreme + 1) / 10001), '10000 sign flips; seed 20261014'


def save_figure(fig, name):
    fig.savefig(HERE / name, dpi=200, facecolor='white', bbox_inches='tight')
    plt.close(fig)


def main():
    metric = load_module('name_metric', TASK3 / 'evaluate_name_metrics.py')
    metric.main()
    summary = read_csv(TASK3 / 'name_metrics_summary.csv')
    details = read_csv(TASK3 / 'name_metrics_per_question.csv')
    by_framework = {name: [r for r in details if r['framework'] == name] for name in NAMES}
    times = []
    for name in NAMES:
        metadata = (TASK2 / name / 'metadata.txt').read_text(encoding='utf-8')
        times.append(int(re.search(r'Generation time: (\d+) seconds', metadata)[1]))

    tests = []
    for a, b in itertools.combinations(NAMES, 2):
        assert [r['question'] for r in by_framework[a]] == [r['question'] for r in by_framework[b]]
        for key in ['original_exact', 'name_exact', 'name_f1']:
            x = [float(r[key]) for r in by_framework[a]]
            y = [float(r[key]) for r in by_framework[b]]
            difference, pvalue, method = paired_test(x, y)
            tests.append({
                'prompt_a': a, 'prompt_b': b, 'metric': key,
                'question_count': len(x), 'nonzero_paired_differences': sum(u != v for u, v in zip(x, y)),
                'mean_difference_a_minus_b': difference, 'two_sided_p_value': pvalue,
                'significant_at_0_05': int(pvalue < .05), 'method': method,
            })
    write_csv('paired_comparisons.csv', tests)
    table = []
    for r, seconds in zip(summary, times):
        table.append({**r, 'generation_seconds': seconds, 'estimated_timing_uncertainty_seconds': 1})
    write_csv('comparison_summary.csv', table)

    evaluator = load_module('original_evaluator', TASK2 / 'data/evaluate_retrieval_predictions.py')
    connection = evaluator.load_database()
    connection.execute('PRAGMA query_only = ON')
    labels = read_csv(TASK2 / 'data/restaurants_dataset.csv')
    predictions = {name: read_csv(TASK2 / name / 'restaurants_dataset_predictions.csv') for name in NAMES}
    outputs = {}
    errors = []
    audit = {}
    try:
        for name in NAMES:
            outputs[name] = [connection.execute(r['predicted_sql']).fetchall() for r in predictions[name]]
        for i, (label, predicted, scores) in enumerate(zip(labels, outputs['ICIO'], by_framework['ICIO']), 1):
            expected = json.loads(label['result'])
            a, b = Counter(r[1] for r in expected), Counter(r[1] for r in predicted)
            if a != b:
                errors.append({
                    'question_index': i, 'question': label['question'],
                    'expected_count': len(expected), 'predicted_count': len(predicted),
                    'name_f1': scores['name_f1'],
                    'missing_name_counts_json': json.dumps(dict(a - b), ensure_ascii=False),
                    'extra_name_counts_json': json.dumps(dict(b - a), ensure_ascii=False),
                    'distinct_name_sets_equal': int(set(a) == set(b)),
                    'ICIO_SQL': predictions['ICIO'][i-1]['predicted_sql'],
                })
        db_names = dict(connection.execute('SELECT ID, NAME FROM RESTAURANT'))
        expected_rows = [row for label in labels for row in json.loads(label['result'])]
        audit = {
            'expected_row_occurrences': len(expected_rows),
            'inconsistent_id_name_occurrences': sum(db_names.get(row[0]) != row[1] for row in expected_rows),
            'empty_expected_questions': sum(not json.loads(r['result']) for r in labels),
            'reference_note': 'Counts are row occurrences, not unique restaurant identities.',
        }
    finally:
        connection.close()
    write_csv('name_mismatch_examples.csv', errors)
    pairs = []
    for a, b in itertools.combinations(NAMES, 2):
        pairs.append({
            'prompt_a': a, 'prompt_b': b,
            'different_sql_questions': sum(x['predicted_sql'] != y['predicted_sql'] for x,y in zip(predictions[a], predictions[b])),
            'different_result_multisets': sum(Counter(x) != Counter(y) for x,y in zip(outputs[a],outputs[b])),
        })
    write_csv('sql_result_comparison.csv', pairs)
    (HERE / 'reference_audit.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig, ax = plt.subplots(figsize=(10,5))
    keys = ['original_accuracy','name_exact_accuracy','macro_name_f1','nonempty_macro_name_f1']
    labels_plot = ['Original row\naccuracy','Name exact\nmatch','Macro name\nF1','Name F1: nonempty\nreferences only']
    x = np.arange(4)
    for i, (r, display, color) in enumerate(zip(summary, DISPLAY, COLORS)):
        values = [float(r[k])*100 for k in keys]
        bars = ax.bar(x+(i-1)*.24, values, .23, label=display, color=color)
        for bar, value in zip(bars,values):
            ax.text(bar.get_x()+bar.get_width()/2,value+1.3,f'{value:.2f}',ha='center',fontsize=8)
    ax.set(xticks=x,xticklabels=labels_plot,ylabel='Score (%)',ylim=(0,113),title='Identical scores across the three prompts')
    ax.legend(loc='upper left',ncol=3);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.2)
    fig.tight_layout();save_figure(fig,'Task_4_metric_comparison.png')

    fig, axes = plt.subplots(1,2,figsize=(11,4.8))
    scores = [float(r['name_f1']) for r in by_framework['ICIO']]
    counts = [sum(v==1 for v in scores),sum(0<v<1 for v in scores),sum(v==0 for v in scores)]
    bars=axes[0].bar(['Exact name\nmatch','Partial\noverlap','No name\noverlap'],counts,color=['#2B997D','#D69B35','#BE5151'])
    for bar,value in zip(bars,counts):axes[0].text(bar.get_x()+bar.get_width()/2,value+2,str(value),ha='center')
    axes[0].set(title='Per-question name F1 outcomes',ylabel='Number of questions',ylim=(0,165))
    bars=axes[1].bar(DISPLAY,times,color=COLORS,yerr=[1]*3,capsize=4)
    for bar,value in zip(bars,times):axes[1].text(bar.get_x()+bar.get_width()/2,value+6,f'{value} s',ha='center')
    axes[1].set(title='One observed generation time per prompt',ylabel='Seconds',ylim=(0,215))
    for ax in axes:ax.set_axisbelow(True);ax.grid(axis='y',alpha=.2)
    fig.suptitle('All prompts share the same outcomes; measured times differ',fontsize=14)
    fig.text(.05,.02,'Left: counts apply to each framework. Right: ±1 s estimated manual uncertainty, not repeated-run variability.',fontsize=9,color='#555555')
    fig.tight_layout(rect=(0,.06,1,.94));save_figure(fig,'Task_4_outcomes_and_time.png')

    fig,ax=plt.subplots(figsize=(9,5.8))
    indices=[int(r['question_index']) for r in errors]
    values=[float(r['name_f1'])*100 for r in errors]
    ax.barh([f'Question {i}' for i in indices],values,color=['#BE5151' if v==0 else '#3178A8' for v in values])
    for y,value in enumerate(values):ax.text(value+1,y,f'{value:.2f}%',va='center',fontsize=9)
    ax.invert_yaxis();ax.set(xlabel='Name-based F1 (%)',xlim=(0,114),title='The 12 name mismatches shared by all three prompts')
    ax.set_axisbelow(True);ax.grid(axis='x',alpha=.2)
    fig.tight_layout();save_figure(fig,'Task_4_name_mismatches.png')
    print('Task 4: saved comparison tables, paired tests, error examples, audit, and three figures.')


if __name__ == '__main__':
    main()
