from pathlib import Path
import os
import subprocess


if __name__ == '__main__':
    root_dir = Path(__file__).parent.absolute()
    good = root_dir / "good"
    bad  = root_dir / "bad"
    to_be_tested = root_dir.parent / "interpreter.py"
    cool_path = root_dir / "cool.exe"
    print("testing //good ......")

    passed_good = 0
    passed_bad  = 0
    failed_good = 0
    failed_bad  = 0
    failed_file_good = []
    failed_file_bad  = []
    # for f in  good.iterdir():
    #     if f.suffix == ".cl":
    #         print(f)
    #         print("================================================================")
    #         in_file = str(f)[:-2]+"INPUT"
    #         out_file = str(f)[:-2]+"OUT"
    #         sam_file = str(f)[:-2]+"OUTPUT"
    #         subprocess.run(["py", str(to_be_tested), str(f)+"-type"],
    #                 stdin  = open(in_file, "r"),
    #                 stdout = open(out_file, "w+"))
    #         subprocess.run([str(cool_path) , str(f)],
    #                 stdin  = open(in_file, "r"),
    #                 stdout = open(sam_file, "w+"))
    #         result = subprocess.run(["fc", out_file, sam_file], capture_output=True)
    #         print("================")
    #         if "FC: no differences encountered" in str(result.stdout):
    #             print("PASS")
    #             passed_good += 1
    #         else:
    #             print("FAIL")
    #             print(result.stdout)
    #             failed_good += 1
    #             failed_file_good.append(f)
    #         print("================================================================\n\n")

    print("testing //bad ......")
    for f in  bad.iterdir():
        if f.suffix == ".cl":
            out_file = str(f)[:-2]+"OUT"
            sam_file = str(f)[:-2]+"OUTPUT"
            subprocess.run(["py", str(to_be_tested), str(f)+"-type"],
                    stdout = open(out_file, "w+"))
            subprocess.run([str(cool_path) , str(f)],
                    stdout = open(sam_file, "w+"))
            result = subprocess.run(["fc", out_file, sam_file], capture_output=True)
            print("================")
            if "FC: no differences encountered" in str(result.stdout):
                print("PASS")
                passed_bad += 1
            else:
                print("FAIL")
                failed_bad += 1
                failed_file_bad.append(f)
            print("================================================================\n\n")

    print("================================================================\n")
    print("===================       TEST    SUMMARY       ================\n")
    print("================================================================\n")
    print("Good test cases: ")
    print("\t PASS: %d" % (passed_good))
    print("\t FAIL: %d" % (failed_good))
    for f in failed_file_good:
        print(f)
    print("================================================================\n")
    print("Bad test cases: ")
    print("\t PASS: %d" % (passed_bad))
    print("\t FAIL: %d" % (failed_bad))
    for f in failed_file_bad:
        print(f)
