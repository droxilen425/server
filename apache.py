import os
import argparse
import subprocess

def configure_apache(ip, port, directory, server_name):
    apache_conf_path = "/data/data/com.termux/files/usr/etc/apache2/httpd.conf"
    php_module_path = "/data/data/com.termux/files/usr/libexec/apache2/libphp.so"
    
    # Read the existing configuration file
    with open(apache_conf_path, 'r') as file:
        conf = file.readlines()

    # Flags to check if the directives exist
    listen_set = False
    docroot_set = False
    directory_set = False
    server_name_set = False
    php_module_set = False
    php_handler_set = False

    # Modify the configuration lines
    for i, line in enumerate(conf):
        if line.startswith("Listen"):
            conf[i] = f"Listen {ip}:{port}\n"
            listen_set = True
        if line.startswith("DocumentRoot"):
            conf[i] = f'DocumentRoot "{directory}"\n'
            docroot_set = True
        if line.startswith("<Directory"):
            conf[i] = f'<Directory "{directory}">\n'
            directory_set = True
        if line.startswith("ServerName"):
            conf[i] = f'ServerName {server_name}\n'
            server_name_set = True
        if "libphp.so" in line:
            conf[i] = f'LoadModule php_module {php_module_path}\n'
            php_module_set = True
        if line.startswith("<FilesMatch \.php$>"):
            php_handler_set = True

    # If directives are not found, add them
    if not listen_set:
        conf.insert(0, f"Listen {ip}:{port}\n")
    if not docroot_set:
        conf.append(f'DocumentRoot "{directory}"\n')
    if not directory_set:
        conf.append(f'<Directory "{directory}">\n</Directory>\n')
    if not server_name_set:
        conf.append(f'ServerName {server_name}\n')
    if not php_module_set:
        conf.append(f'LoadModule php_module {php_module_path}\n')
    if not php_handler_set:
        conf.append(
            "<FilesMatch \\.php$>\n"
            "    SetHandler application/x-httpd-php\n"
            "</FilesMatch>\n"
        )

    # Write the modified configuration back to the file
    with open(apache_conf_path, 'w') as file:
        file.writelines(conf)

    # Restart Apache server
    subprocess.run(["apachectl", "restart"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure and start Apache server.")
    parser.add_argument("--ip", type=str, default="0.0.0.0", help="IP address to serve on (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on (default: 8080)")
    parser.add_argument("--dir", type=str, default="/data/data/com.termux/files/usr/share/apache2/default-site/htdocs", help="Root directory (default: /data/data/com.termux/files/usr/share/apache2/default-site/htdocs)")
    parser.add_argument("--server_name", type=str, default="127.0.0.1", help="Server name (default: 127.0.0.1)")

    args = parser.parse_args()

    configure_apache(args.ip, args.port, args.dir, args.server_name)
