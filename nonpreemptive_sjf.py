import pandas as pd


def non_preemptive_sjf(df):
    df = df.sort_values(by="Arrival_Time").reset_index(drop=True)

    current_time = 0
    df_results = []
    idle_time = 0

    processes = df.to_dict("records")

    print("NON-PREEMPTIVE SJF Algorithm")
    print("-----------------------------------------------")
    print("Timing Data Of Every Process:")
    print("-----------------------------------------------\n")

    while processes:
        available = [p for p in processes if p["Arrival_Time"] <= current_time]

        if not available:
            next_arrival = min(p["Arrival_Time"] for p in processes)
            print(f"[{current_time}] - - IDLE - - [{next_arrival}]")
            idle_time += next_arrival - current_time
            current_time = next_arrival
            continue

        process = min(available, key=lambda x: x["CPU_Burst_Time"])
        processes.remove(process)

        pid = process["Process_ID"]
        at = int(process["Arrival_Time"])
        bt = int(process["CPU_Burst_Time"])

        start_time = current_time
        end_time = start_time + bt

        wt = start_time - at
        tat = end_time - at

        print(f"[{start_time}] - - {pid} - - [{end_time}]")

        df_results.append({
            "Process_ID": pid,
            "Arrival_Time": at,
            "CPU_Burst_Time": bt,
            "Start_Time": start_time,
            "Completion_Time": end_time,
            "Waiting_Time": wt,
            "Turnaround_Time": tat,
        })

        current_time = end_time

    df_results = pd.DataFrame(df_results)

    print("\n-----------------------------------------------")
    print("Maximum, Total and Average Waiting Time Results: ")
    print("-----------------------------------------------\n")
    print(f"Maximum Waiting Time: {df_results['Waiting_Time'].max()}")
    print(f"Total Waiting Time: {df_results['Waiting_Time'].sum()}")
    print(f"Average Waiting Time: {df_results['Waiting_Time'].mean():.2f}")

    print("\n-----------------------------------------------")
    print("Maximum, Total and Average Turnaround Time Results: ")
    print("-----------------------------------------------\n")
    print(f"Maximum Turnaround Time: {df_results['Turnaround_Time'].max()}")
    print(f"Total Turnaround Time: {df_results['Turnaround_Time'].sum()}")
    print(f"Average Turnaround Time: {df_results['Turnaround_Time'].mean():.2f}")

    print("\n-----------------------------------------------")
    print("Throughput For T=[50, 100, 150, 200]: ")
    print("-----------------------------------------------\n")
    t_values = [50, 100, 150, 200]
    for t in t_values:
        done = (df_results["Completion_Time"] <= t).sum()
        thr = done / t
        print(f"T = {t} -> Completed processes: {done}, Throughput: {thr:.4f}")

    print("\n-----------------------------------------------")
    print("Average CPU Utilization [Context Switch = 0,001 unit.]: ")
    print("-----------------------------------------------\n")
    process_count = len(df_results)
    context_switch_time = (process_count - 1) * 0.001
    total_burst_time = float(df["CPU_Burst_Time"].sum())

    total_time = total_burst_time + idle_time + context_switch_time
    cpu_utilization = total_burst_time / total_time

    print(f"Total CPU Burst Time: {total_burst_time}")
    print(f"Total CPU Idle Time: {idle_time}")
    print(f"Total Context Switch Time: {context_switch_time:.3f}")
    print(f"Total Time: {total_time:.3f}")
    print(f"Average CPU Utilization: {cpu_utilization * 100:.2f}%")

    print("\n-----------------------------------------------")
    print("Toplam Bağlam Değiştirme Sayısı: ")
    print("-----------------------------------------------\n")
    total_context_switches = len(df_results) - 1
    print(f"Total Context Switch Count: {total_context_switches}")

    return df_results
