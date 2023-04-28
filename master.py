import sys
import subprocess
from termcolor import colored
import atexit


def cleanup():
    for process in processes:
        process.kill()


atexit.register(cleanup)


tokens = []
with open("./tokens.txt", "r") as f:
    for line in f.readlines():
        if not line or line == "":
            continue
        tokens.append(line.replace('\n', '').strip())

print(colored("DM Sender starting...", "magenta"))

processes = []
used_tokens = []
while len(tokens) > 0:
    token = tokens[0]
    tokens.pop(0)
    used_tokens.append(token)
    try:
        processes.append(subprocess.Popen([sys.executable, "bot.py", token, str(len(processes) + 1)]))
    except Exception as e:
        pass

exit_codes = [p.wait() for p in processes]

with open("./used_tokens.txt", "a") as f:
    f.truncate(0)
    for token in used_tokens:
        f.write(f"{token}\n")

print(colored("All bots finished running", "magenta"))
