#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime
import time

RESULTS_FILE = "obma_resultado.txt"
TRIALS_PER_INSTANCE = 10  # Executar cada instância 10 vezes


def run_single_instance(cmd, instance_num, trial_num, total_instances):
    start_time = datetime.now()
    print(
        f"\n▶ Executando Instância {instance_num}/{total_instances} - Trial {trial_num}/{TRIALS_PER_INSTANCE}:\n{cmd}",
        flush=True)

    with open(RESULTS_FILE, 'a', buffering=1) as f:
        f.write(f"\n{'=' * 80}\n")
        f.write(
            f"Instância {instance_num}/{total_instances} | Trial {trial_num}/{TRIALS_PER_INSTANCE} | {cmd} | INICIO | {start_time}\n")
        f.write(f"{'=' * 80}\n")

        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            trial_output = []

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break

                if output:
                    output = output.strip()
                    print(output, flush=True)
                    f.write(f"{datetime.now()} | {output}\n")
                    trial_output.append(output)

            returncode = process.poll()
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extrai resultados importantes
            best_cost = "N/A"
            for line in reversed(trial_output):
                if "best_cost" in line:
                    best_cost = line.split("best_cost = ")[1].split(",")[0]
                    break

            status = "SUCESSO" if returncode == 0 else f"ERRO {returncode}"
            f.write(
                f"\nInstância {instance_num}/{total_instances} | Trial {trial_num}/{TRIALS_PER_INSTANCE} | {status} | "
                f"Duração: {duration:.2f}s | Melhor Custo: {best_cost} | {end_time}\n")
            f.write(f"{'=' * 80}\n\n")

            return {
                'status': returncode == 0,
                'duration': duration,
                'best_cost': best_cost
            }

        except Exception as e:
            end_time = datetime.now()
            f.write(f"\nERRO: {str(e)}\n")
            f.write(f"Instância {instance_num} | Trial {trial_num} | EXCEÇÃO | {end_time}\n")
            f.write(f"{'=' * 80}\n")
            print(f"⚠️ EXCEÇÃO Trial {trial_num}: {e}", flush=True)
            return {
                'status': False,
                'duration': 0,
                'best_cost': "ERRO"
            }


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 run_obma.py comandos.txt")
        sys.exit(1)

    input_file = sys.argv[1]

    # Reinicia o arquivo de resultados
    with open(RESULTS_FILE, 'w') as f:
        f.write(f"Relatorio de Execucao OBMA - {datetime.now()}\n")
        f.write(f"Configuração: {TRIALS_PER_INSTANCE} trials por instância\n")
        f.write("=" * 80 + "\n")

    # Lê comandos
    with open(input_file) as f:
        instances = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    total_instances = len(instances)
    results = []

    # Executa cada instância TRIALS_PER_INSTANCE vezes
    for instance_num, cmd in enumerate(instances, 1):
        instance_results = []
        for trial_num in range(1, TRIALS_PER_INSTANCE + 1):
            result = run_single_instance(cmd, instance_num, trial_num, total_instances)
            instance_results.append(result)
            time.sleep(1)  # Pequena pausa entre trials

        results.append(instance_results)

    # Resumo final
    with open(RESULTS_FILE, 'a') as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write("RESUMO FINAL POR INSTÂNCIA\n")
        f.write("=" * 80 + "\n")

        for i, instance_results in enumerate(results, 1):
            successes = sum(1 for r in instance_results if r['status'])
            avg_duration = sum(r['duration'] for r in instance_results) / TRIALS_PER_INSTANCE
            best_results = [r['best_cost'] for r in instance_results if
                            r['best_cost'] != "N/A" and r['best_cost'] != "ERRO"]

            f.write(f"\nInstância {i}:\n")
            f.write(f"  - Sucessos: {successes}/{TRIALS_PER_INSTANCE}\n")
            f.write(f"  - Duração média: {avg_duration:.2f}s\n")
            if best_results:
                f.write(f"  - Melhores custos obtidos:\n")
                for cost in best_results:
                    f.write(f"    → {cost}\n")
            f.write("-" * 60 + "\n")

    print(f"\n✅ Execução completa - {total_instances} instâncias, {TRIALS_PER_INSTANCE} trials cada", flush=True)


if __name__ == "__main__":
    main()