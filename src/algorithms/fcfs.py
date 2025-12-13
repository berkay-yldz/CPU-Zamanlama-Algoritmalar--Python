import pandas as pd

def fcfs(df):

    df = df.sort_values(by="Arrival_Time").reset_index(drop=True)

    current_time = 0
    idle_time = 0
    results = []

    print("F C F S  Algorithm")
    print("-----------------------------------------------")
    print("Timing Data Of Every Process: ")
    print("-----------------------------------------------\n")

    for index, row in df.iterrows():
        at = row["Arrival_Time"]
        bt = row["CPU_Burst_Time"]
        pid = row["Process_ID"]

        # in case CPU goes idle:
        if current_time < at:
            idle_length = at - current_time
            idle_time += idle_length
            print(f"[{current_time}] | | IDLE | | [{at}]")
            current_time = at

        start_time = current_time
        end_time = start_time + bt
        current_time = end_time
        wt = start_time - at
        tat = end_time - at

        results.append(
            {
                "Process_ID": pid,
                "Arrival_Time": at,
                "CPU_Burst_Time": bt,
                "Start_Time": start_time,
                "Completion_Time": end_time,
                "Waiting_Time": wt,
                "Turnaround_Time": tat,
            }
        )

        print(f"[{start_time}] - - {pid} - - [{end_time}]")

    df_results = pd.DataFrame(results)

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
        p_count = (df_results["Completion_Time"] <= t).sum()
        print(f"T = {t} -> Completed processes: {p_count}")

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
    print(f"Total Context Switch Count:{total_context_switches}")
    return df_results


if __name__ == "__main__":
    case1 = pd.read_csv("data/case1.csv")
    case2 = pd.read_csv("data/case2.csv")

    fcfs(case1)
    print(
        """\n////////////////////////////////////////////////////////////////////////////////////
        ////////////////////////////////////////////////////////////////////////////////////
                ////////////////////////////////////////////////////////////////////////////////////\n"""
    )
    fcfs(case2)
