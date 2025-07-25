import os
import time
import csv
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from prestodb import dbapi, exceptions

PRESTO_HOST = 'localhost'
PRESTO_PORT = 8080
PRESTO_USER = 'presto'
CATALOG = 'tpch'

# Get the absolute path to the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUERIES_DIR = os.path.join(SCRIPT_DIR, 'tpch_queries')

def run_benchmark(schema):
    """
    Connects to Presto, runs TPC-H queries against a specific schema, 
    and records the execution time for each.
    """
    results = []
    
    conn = dbapi.connect(
        host=PRESTO_HOST,
        port=PRESTO_PORT,
        user=PRESTO_USER,
        catalog=CATALOG,
        schema=schema,
    )

    def get_query_number(filename):
        basename, _ = os.path.splitext(filename)
        if basename.startswith('q'):
            try:
                return int(basename[1:])
            except ValueError:
                return float('inf')  # Sort malformed files last
        return float('inf')

    query_files = sorted(
        [f for f in os.listdir(QUERIES_DIR) if f.endswith('.sql')],
        key=get_query_number
    )

    for query_file in query_files:
        query_path = os.path.join(QUERIES_DIR, query_file)
        with open(query_path, 'r') as f:
            query = f.read()

        print(f"Executing {query_file} for schema {schema}...")
        start_time = time.time()

        try:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"{query_file} executed in {execution_time:.2f} seconds.")
            results.append({'schema': schema, 'query': query_file, 'execution_time_seconds': execution_time, 'status': 'success', 'error_type': '', 'error_message': ''})
        except Exception as e:
            error_type = type(e).__name__
            error_message = str(e)
            print(f"Error executing {query_file}: {error_type} - {error_message}")
            results.append({'schema': schema, 'query': query_file, 'execution_time_seconds': 0, 'status': 'error', 'error_type': error_type, 'error_message': error_message})
        finally:
            if 'cur' in locals() and cur:
                cur.close()
    
    conn.close()
    return results

def plot_results(df):
    """
    Plots the benchmark results as a stacked bar chart.
    """
    
    df_pivot = df.pivot(index='schema', columns='query', values='execution_time_seconds')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(18, 10))
    df_pivot.plot(kind='bar', stacked=True, ax=ax)

    # Add labels to each segment
    for i, c in enumerate(ax.containers):
        labels = [f'{df_pivot.iloc[j, i]:.2f}\n({df_pivot.columns[i]})' for j in range(len(df_pivot))]
        ax.bar_label(c, labels=labels, label_type='center', color='white', weight='bold')
    
    ax.set_title('TPC-H Query Execution Time by Schema', fontsize=16)
    ax.set_xlabel('Schema', fontsize=12)
    ax.set_ylabel('Total Execution Time (seconds)', fontsize=12)
    ax.legend(title='Query', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plot_file = 'benchmark_results.png'
    plt.savefig(plot_file)
    print(f"Plot saved to {plot_file}")

if __name__ == '__main__':
    schemas = ['sf1']
    all_results = []

    for schema in schemas:
        print(f"--- Starting benchmark for schema: {schema} ---")
        results = run_benchmark(schema)
        all_results.extend(results)
        print(f"--- Benchmark for schema {schema} complete ---")

    # Create a DataFrame from the results
    df = pd.DataFrame(all_results)
    
    # Save the detailed results to a CSV file
    df.to_csv('benchmark_results_sf1.csv', index=False)
    print("Detailed results saved to benchmark_results_sf1.csv")

    # Plot the results
    plot_results(df) 