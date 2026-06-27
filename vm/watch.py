import subprocess
# from var import project_root
project_root = "/home/mathieu/projects/Quartzine"


def watch():
    result = subprocess.run(
        [
            "bpftrace", "-o", "result.txt",
            f"{project_root}/vm/watch.bt",
            subprocess.getoutput("pidof qemu-system-x86_64").split()[0],
        ],
        capture_output=True, check=True, text=True
    )

    print("RC:", result.returncode)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)


watch()
