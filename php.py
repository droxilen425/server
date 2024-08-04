import os
import argparse
import subprocess

def start_php_server(port, directory):
    os.chdir(directory)
    command = f"php -S 0.0.0.0:{port}"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a PHP server.")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on (default: 8000)")
    parser.add_argument("--dir", type=str, default=".", help="Root directory (default: current directory)")

    args = parser.parse_args()

    start_php_server(args.port, args.dir)
