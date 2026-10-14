import subprocess
import sys

def run_check(args, cwd, timeout=5):
    try:
        result = subprocess.run(
            args, cwd=cwd, timeout=timeout,
            capture_output=True, text=True,
            shell=False, check=False)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "code": None}
    return {"status": "finished",
            "code": result.returncode,
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-2000:]}

result = run_check(
    [sys.executable, "-c", "print(2 + 3)"], ".")
assert result["status"] == "finished"
assert result["code"] == 0
assert result["stdout"].strip() == "5"
print('Проверка запуска пройдена')
