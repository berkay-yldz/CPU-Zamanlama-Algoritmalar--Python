"""
FCFS (First Come First Served) CPU Scheduling Algorithm

Process'ler varış zamanına göre sıralanır ve sırayla işlenir.
Her process için detaylı zamanlama bilgileri ve performans metrikleri hesaplanır.
"""

import pandas as pd

CONTEXT_SWITCH_TIME = 0.001
THROUGHPUT_TIME_POINTS = [50, 100, 150, 200]


def _print_metrics(df_results, total_idle_time, total_burst_time):
    """Performans metriklerini hesaplar ve yazdırır."""
    # Waiting Time
    print("\n-----------------------------------------------")
    print("Maximum, Total and Average Waiting Time Results: ")
    print("-----------------------------------------------\n")
    print(f"Maximum Waiting Time: {df_results['Waiting_Time'].max()}")
    print(f"Total Waiting Time: {df_results['Waiting_Time'].sum()}")
    print(f"Average Waiting Time: {df_results['Waiting_Time'].mean():.2f}")
    
    # Turnaround Time
    print("\n-----------------------------------------------")
    print("Maximum, Total and Average Turnaround Time Results: ")
    print("-----------------------------------------------\n")
    print(f"Maximum Turnaround Time: {df_results['Turnaround_Time'].max()}")
    print(f"Total Turnaround Time: {df_results['Turnaround_Time'].sum()}")
    print(f"Average Turnaround Time: {df_results['Turnaround_Time'].mean():.2f}")
    
    # Throughput
    print("\n-----------------------------------------------")
    print("Throughput For T=[50, 100, 150, 200]: ")
    print("-----------------------------------------------\n")
    for t in THROUGHPUT_TIME_POINTS:
        completed = (df_results["Completion_Time"] <= t).sum()
        throughput = completed / t
        print(f"T = {t} -> Completed processes: {completed}, Throughput: {throughput:.4f}")
    
    # CPU Utilization
    print("\n-----------------------------------------------")
    print("Average CPU Utilization [Context Switch = 0,001 unit.]: ")
    print("-----------------------------------------------\n")
    process_count = len(df_results)
    context_switch_time = (process_count - 1) * CONTEXT_SWITCH_TIME
    total_time = total_burst_time + total_idle_time + context_switch_time
    cpu_utilization = total_burst_time / total_time
    
    print(f"Total CPU Burst Time: {total_burst_time}")
    print(f"Total CPU Idle Time: {total_idle_time}")
    print(f"Total Context Switch Time: {context_switch_time:.3f}")
    print(f"Total Time: {total_time:.3f}")
    print(f"Average CPU Utilization: {cpu_utilization * 100:.2f}%")
    
    # Context Switch Count
    print("\n-----------------------------------------------")
    print("Toplam Bağlam Değiştirme Sayısı: ")
    print("-----------------------------------------------\n")
    print(f"Total Context Switch Count: {process_count - 1}")


def fcfs(df):
    """
    FCFS (First Come First Served) algoritmasını çalıştırır.
    
    Args:
        df: Process bilgilerini içeren DataFrame (Process_ID, Arrival_Time, CPU_Burst_Time)
    
    Returns:
        Process sonuçlarını içeren DataFrame
    """
    df = df.sort_values(by="Arrival_Time").reset_index(drop=True)
    
    current_time = 0.0
    total_idle_time = 0.0
    results = []
    
    print("F C F S  Algorithm")
    print("-----------------------------------------------")
    print("Timing Data Of Every Process: ")
    print("-----------------------------------------------\n")
    
    for _, row in df.iterrows():
        arrival_time = row["Arrival_Time"]
        burst_time = row["CPU_Burst_Time"]
        process_id = row["Process_ID"]
        
        # CPU boşta kalma durumu
        if current_time < arrival_time:
            idle_length = arrival_time - current_time
            total_idle_time += idle_length
            print(f"[{current_time}] | | IDLE | | [{arrival_time}]")
            current_time = arrival_time
        
        # Süreç işleme
        start_time = current_time
        end_time = start_time + burst_time
        waiting_time = start_time - arrival_time
        turnaround_time = end_time - arrival_time
        
        print(f"[{start_time}] - - {process_id} - - [{end_time}]")
        
        results.append({
            "Process_ID": process_id,
            "Arrival_Time": arrival_time,
            "CPU_Burst_Time": burst_time,
            "Start_Time": start_time,
            "Completion_Time": end_time,
            "Waiting_Time": waiting_time,
            "Turnaround_Time": turnaround_time,
        })
        
        current_time = end_time
    
    df_results = pd.DataFrame(results)
    total_burst_time = float(df["CPU_Burst_Time"].sum())
    _print_metrics(df_results, total_idle_time, total_burst_time)
    
    return df_results
