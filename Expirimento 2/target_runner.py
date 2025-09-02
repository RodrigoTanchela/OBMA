#!/usr/bin/env python3
###############################################################################
# This script is the command that is executed every run.
# PARAMETERS:
# argv[1] is the candidate configuration number
# argv[2] is the instance ID
# argv[3] is the seed
# argv[4] is the instance name
# The rest (argv[5:]) are parameters to the run
###############################################################################

import datetime
import os.path
import subprocess
import sys

exe = "./OBMA"


def get_param(name):
    for param in conf_params:
        if name in param:
            return param[param.index(':')+1:]
    return None

def parse_output(out):
    out = str(out).strip()
    out = out.split('\n')
    for line in out:
        if 'found best objective' in line:
            result = line[line.index('=') + 2:]
            return float(result) * (-1)
    return 999999

if len(sys.argv) < 5:
    print("\nUsage: ./target-runner.py <configuration_id> <instance_id> <seed> <instance_path_name> <list of parameters>\n")
    sys.exit(1)

# --- Parâmetros de linha de comando ---
configuration_id = sys.argv[1]
instance_id = sys.argv[2]
seed = sys.argv[3]
instance = sys.argv[4]
conf_params = sys.argv[5:]

fixed_params = "1"
if instance.find("MDG-a") != -1:
    instance_tipo = "MDG-a"
elif instance.find("MDG-b") != -1:
    instance_tipo = "MDG-b"
elif instance.find("MDG-c") != -1:
    instance_tipo = "MDG-c"
else:
    "ERRO: valor não encontrado"

if instance_tipo.find("MDG-a") != -1:
    tempo_execucao = "10"
elif instance_tipo.find("MDG-b") != -1:
    tempo_execucao = "20"
else:
    tempo_execucao = "30"


NP = get_param('NP')
PS = get_param('PS')
alpha = get_param('alpha')
T = get_param('T')
max_iter = get_param('max_iter')
scale_factor = get_param('scale_factor')
is_obl = get_param('is_obl')


exe = os.path.expanduser(exe)
command = f'{exe} {instance} {instance_tipo} {tempo_execucao} {fixed_params} {NP} {PS} {alpha} {T} {max_iter} {scale_factor} {is_obl}'


out_file = f"c{configuration_id}-{instance_id}{seed}.stdout"
err_file = f"c{configuration_id}-{instance_id}{seed}.stderr"

def target_runner_error(msg):
    now = datetime.datetime.now()
    print(str(now) + " error: " + msg)
    sys.exit(1)

def check_executable(fpath):
    fpath = os.path.expanduser(fpath)
    if not os.path.isfile(fpath):
        target_runner_error(str(fpath) + " not found")
    if not os.access(fpath, os.X_OK):
        target_runner_error(str(fpath) + " is not executable")

check_executable(exe)

outf = open(out_file, "w")
errf = open(err_file, "w")
return_code = subprocess.call(command, stdout=outf, stderr=errf, shell=True)
outf.close()
errf.close()

if return_code != 0:
    target_runner_error("command returned code " + str(return_code))

if not os.path.isfile(out_file):
    target_runner_error("output file " + out_file  + " not found.")

cost = parse_output(open(out_file).read())
print(cost)

os.remove(out_file)
os.remove(err_file)
sys.exit(0)
