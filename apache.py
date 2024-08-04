import os
import argparse
import subprocess

def configure_apache(ip, port, directory):
    apache_conf_path = "/data/data/com.termux/files/usr/etc/apache2/httpd.conf"
    
    # Read the existing configuration file
    with open(apache_conf_path, 'r') as file:
        conf = file.readlines()

    # Modify the configuration lines
    for i, line in enumerate(conf):
        if line.startswith("Listen"):
            conf[i] = f"Listen {ip}:{port}\n"
        if line.startswith("DocumentRoot"):
            conf[i] = f'DocumentRoot "{directory}"\n'
        if line.startswith("<Directory"):
            conf[i] = f'<Directory "{directory}">\n'

    # Write the modified configuration back to the file
    with open(apache_conf_path, 'w') as file:
        file.writelines(conf)

    # Start Apache server
    subprocess.run(["apachectl", "restart"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure and start Apache server.")
    parser.add_argument("--ip", type=str, default="0.0.0.0", help="IP address to serve on (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on (default: 8080)")
    parser.add_argument("--dir", type=str, default="/data/data/com.termux/files/usr/share/apache2/default-site/htdocs", help="Root directory (default: /data/data/com.termux/files/usr/share/apache2/default-site/htdocs)")

    args = parser.parse_args()

    configure_apache(args.ip, args.port, args.dir)
