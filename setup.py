from __future__ import print_function

# This setups the pipeline
import os
import sys
import subprocess
import io
import gzip
import shutil

sys.dont_write_bytecode = True


devnull = open(os.path.devnull, "w")
setup_dir = os.path.dirname(os.path.realpath(__file__))
current_step = 0



def error(msg):
    print("Setup failed: ", msg)
    print("Please fix the errors and then rerun this file")
    sys.exit(0)


def print_step(title):
    global current_step
    current_step += 1
    print("\n\n[", str(current_step).zfill(2), "] ", title)


def exec_python_file(pth):
    basedir = os.path.dirname(os.path.abspath(os.path.join(setup_dir, pth))) + "/"
    print("\tRunning script:", pth)
    pth = os.path.basename(pth)
    os.chdir(basedir)
    try:
        output = subprocess.check_output([sys.executable, "-B", pth], stderr=sys.stderr)
    except subprocess.CalledProcessError as msg:
        print("Python script didn't return properly!")
        error("Failed to execute '" + pth + "'")

    except Exception as msg:
        print("Python script error:", msg)
        error("Error during script execution")


def extract_gz_files(pth):
    pth = os.path.join(setup_dir, pth)
    files = os.listdir(pth)
    for f in files:
        fullpath = os.path.join(pth, f)
        if os.path.isfile(fullpath) and f.endswith(".gz"):
            print("\tExtracting .gz file:", f)

            try:
                with open(fullpath[:-3], 'wb') as dest, gzip.open(fullpath, 'rb') as src:
                    shutil.copyfileobj(src, dest)
            except Exception as msg:
                error("Failed to extract file '" + f + "': " + str(msg))

def check_repo_complete():

    # Check if the render target submodule exists
    if not os.path.isfile(os.path.join(setup_dir, "Code/RenderTarget/RenderTarget.py")):
        print("-" * 79)
        print("  You didn't checkout the RenderTarget submodule!")
        print("  Please checkout the whole repository, and also make sure you ")
        print("  did 'git submodule init' and 'git submodule update' if you use")
        print("  a command line client!")
        print("-" * 79)
        error("RenderTarget submodule missing")


print("\nRender Pipeline Setup 1.0\n")
print("-" * 79)

print_step("Checking if the repo is complete ..")
check_repo_complete()

print_step("Compiling the native code .. (This might take a while!)")
exec_python_file("Native/Scripts/setup_native.py")

print_step("Generating normal quantization textures ..")
exec_python_file("Data/NormalQuantization/generate.py")

print_step("Extracting .gz files ...")
extract_gz_files("Data/BuiltinModels/")

print_step("Filtering default cubemap ..")
exec_python_file("Data/DefaultCubemap/filter.py")

# Further setup code follows here

# Write install flag
with open(os.path.join(setup_dir, "Data/install.flag"), "w") as handle:
    handle.write("1")

print("\n\n-- Setup finished sucessfully! --")
