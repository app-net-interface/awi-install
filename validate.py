from src.cmd import run_cmd

def validate_tools():
    print("Checking presence of required tools")
    ok, _ = run_cmd("kubectl")
    if not ok:
        print("kubectl binary not found. Aborting.")
        exit(1)
    print("kubectl confirmed.")

    ok, _ = run_cmd("aws help")
    if not ok:
        print(
            "aws cli not found. Aborting."
        )
        exit(1)
    print("aws cli confirmed.")   

    ok, _ = run_cmd("make --help")
    if not ok:
        print(
            "make not found. Aborting."
        )
        exit(1)
    print("make confirmed.")   

    ok, _ = run_cmd("go help")
    if not ok:
        print(
            "go not found. Aborting."
        )
        exit(1)
    print("go confirmed.")   


