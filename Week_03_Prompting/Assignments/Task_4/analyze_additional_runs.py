"""Evaluate both configurations and reproduce the additional comparison.
Model/setting labels are user-reported; this is not a controlled reasoning-only test.
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

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
FRAMEWORKS=['ICIO','ReAct','SCOPE']
CONFIGS=['GPT-6.1 SOL / Medium','GPT luna / High / Instant']


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def save(name,rows):
    with (HERE/name).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def main(paired_test=None):
    if paired_test is None:paired_test=module('analysis',HERE/'analyze_results.py').paired_test
    csv.field_size_limit(1000000000)
    evaluator=module('original',BASE/'Task_2/data/evaluate_retrieval_predictions.py')
    metric=module('metric',BASE/'Task_3/evaluate_name_metrics.py')
    labels=read(BASE/'Task_2/data/restaurants_dataset.csv')
    connection=evaluator.load_database();connection.execute('PRAGMA query_only = ON')
    details=[];summaries=[];runs={};results={};sqls={}
    try:
        for config in CONFIGS:
            for framework in FRAMEWORKS:
                folder=(BASE/'Task_2'/('REACT' if framework=='ReAct' else framework)) if config==CONFIGS[0] else HERE/(framework+'_rerun')
                predictions=read(folder/'restaurants_dataset_predictions.csv')
                assert [r['question'] for r in predictions]==[r['question'] for r in labels]
                seconds=int(re.search(r'Generation time: (\d+) seconds',(folder/'metadata.txt').read_text())[1])
                key=(config,framework);current=[];results[key]=[];sqls[key]=[r['predicted_sql'] for r in predictions]
                for i,(prediction,label) in enumerate(zip(predictions,labels),1):
                    cursor=connection.execute(prediction['predicted_sql'])
                    assert [c[0].upper() for c in cursor.description]==['HOUSE_NUMBER','NAME'], (key,i,cursor.description)
                    predicted=cursor.fetchall();expected=json.loads(label['result'])
                    precision,recall,f1,exact=metric.name_metrics([r[1] for r in expected],[r[1] for r in predicted])
                    row={'configuration':config,'framework':framework,'question_index':i,'question':label['question'],
                         'expected_count':len(expected),'predicted_count':len(predicted),
                         'original_exact':int(Counter(predicted)==Counter(tuple(r) for r in expected)),
                         'name_exact':int(exact),'name_precision':precision,'name_recall':recall,'name_f1':f1}
                    details.append(row);current.append(row);results[key].append(Counter(predicted))
                runs[key]=current
                nonempty=[r for r in current if r['expected_count']]
                summaries.append({'configuration':config,'framework':framework,'question_count':len(current),
                    'original_correct':sum(r['original_exact'] for r in current),'original_accuracy':np.mean([r['original_exact'] for r in current]),
                    'name_exact_correct':sum(r['name_exact'] for r in current),'name_exact_accuracy':np.mean([r['name_exact'] for r in current]),
                    'macro_name_precision':np.mean([r['name_precision'] for r in current]),'macro_name_recall':np.mean([r['name_recall'] for r in current]),
                    'macro_name_f1':np.mean([r['name_f1'] for r in current]),'nonempty_macro_name_f1':np.mean([r['name_f1'] for r in nonempty]),
                    'generation_seconds':seconds,'execution_errors':0})
    finally:connection.close()
    save('additional_comparison_summary.csv',summaries);save('additional_metrics_per_question.csv',details)
    save('additional_mismatch_examples.csv',[r for r in details if not r['original_exact']])
    pairs=[]
    for config in CONFIGS:
        for a,b in itertools.combinations(FRAMEWORKS,2):pairs.append(((config,a),(config,b),'within configuration'))
    for framework in FRAMEWORKS:pairs.append(((CONFIGS[0],framework),(CONFIGS[1],framework),'across configurations'))
    tests=[];differences=[]
    for a,b,kind in pairs:
        differences.append({'configuration_a':a[0],'framework_a':a[1],'configuration_b':b[0],'framework_b':b[1],
            'different_sql_questions':sum(x!=y for x,y in zip(sqls[a],sqls[b])),
            'different_result_questions':sum(x!=y for x,y in zip(results[a],results[b]))})
        for measure in ['original_exact','name_exact','name_f1']:
            x=[r[measure] for r in runs[a]];y=[r[measure] for r in runs[b]]
            difference,pvalue,method=paired_test(x,y)
            tests.append({'comparison_type':kind,'configuration_a':a[0],'framework_a':a[1],'configuration_b':b[0],'framework_b':b[1],
                'metric':measure,'mean_difference_a_minus_b':difference,'two_sided_p_value':pvalue,'nonzero_paired_differences':sum(u!=v for u,v in zip(x,y)),
                'method':method,'holm_adjusted_p_value':0,'significant_after_holm_at_0_05':0})
    # Nine comparisons per metric: three within each configuration plus three matched-framework comparisons.
    for measure in ['original_exact','name_exact','name_f1']:
        group=sorted([r for r in tests if r['metric']==measure],key=lambda r:r['two_sided_p_value'])
        adjusted=0
        for i,r in enumerate(group):
            adjusted=max(adjusted,min(1.,(len(group)-i)*r['two_sided_p_value']))
            r['holm_adjusted_p_value']=adjusted;r['significant_after_holm_at_0_05']=int(adjusted<.05)
    save('additional_paired_comparisons.csv',tests);save('additional_sql_result_comparison.csv',differences)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,3,figsize=(14,5));x=np.arange(3)
    colors=['#3178A8','#D08334']
    for j,(field,title,ylabel,maximum) in enumerate([('original_accuracy','Exact-result accuracy','Accuracy (%)',110),('macro_name_f1','Name-based partial credit','Macro name F1 (%)',110),('generation_seconds','Observed generation time','Seconds',130)]):
        for k,config in enumerate(CONFIGS):
            rows=[r for r in summaries if r['configuration']==config]
            values=[float(r[field])*(100 if j<2 else 1) for r in rows]
            bars=axes[j].bar(x+(k-.5)*.36,values,.34,color=colors[k],label=config,yerr=[1]*3 if j==2 else None,capsize=3)
            for b,v in zip(bars,values):axes[j].text(b.get_x()+b.get_width()/2,v+1.6,f'{v:.2f}' if j<2 else f'{v:.0f}',ha='center',fontsize=8)
        axes[j].set(xticks=x,xticklabels=FRAMEWORKS,title=title,ylabel=ylabel,ylim=(0,maximum));axes[j].set_axisbelow(True);axes[j].grid(axis='y',alpha=.2)
    handles,legend_labels=axes[0].get_legend_handles_labels();fig.legend(handles,legend_labels,loc='upper center',bbox_to_anchor=(.5,.94),ncol=2)
    fig.suptitle('Two model configurations, three prompting frameworks',fontsize=16,y=.99)
    fig.text(.05,.02,'One run per combination. Model and settings both changed. Timing uncertainty ±1 s is not run-to-run variability.',fontsize=9)
    fig.tight_layout(rect=(0,.06,1,.84));fig.savefig(HERE/'Task_4_additional_comparison.png',dpi=200,facecolor='white');plt.close(fig)
    indices=sorted({r['question_index'] for r in details if r['configuration']==CONFIGS[1] and r['name_f1']<1})
    values=np.array([[runs[(CONFIGS[1],f)][i-1]['name_f1']*100 for f in FRAMEWORKS] for i in indices])
    fig,ax=plt.subplots(figsize=(7,max(4,len(indices)*.35)))
    im=ax.imshow(values,vmin=0,vmax=100,cmap='YlGnBu',aspect='auto')
    ax.set(xticks=range(3),xticklabels=FRAMEWORKS,yticks=range(len(indices)),yticklabels=[f'Question {i}' for i in indices],title='GPT luna / High / Instant: name F1 on mismatches')
    for y in range(len(indices)):
        for x in range(3):ax.text(x,y,f'{values[y,x]:.1f}%',ha='center',va='center',color='white' if values[y,x]>65 else 'black',fontsize=8)
    fig.colorbar(im,ax=ax,label='Name F1 (%)');fig.tight_layout();fig.savefig(HERE/'Task_4_additional_mismatches.png',dpi=200,facecolor='white');plt.close(fig)
    for r in summaries:print(r['configuration'],r['framework'],r['original_correct'],f"F1={r['macro_name_f1']:.6%}",r['generation_seconds'])
    print('Additional analysis: generated six-run tables, 27 paired tests, and two figures.')

if __name__=='__main__':main()
