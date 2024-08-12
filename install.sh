#!/bin/bash

# Title: Installation script
# Author: Pelochus
# Date: 2024-08-04
# Version: 1.1
# Description: Installation script for pprz-py-plotter on Ubuntu/Debian

# Quit on error
set -e

info() {
    echo "[INFO] $1"
}

update_system() {
    sudo apt-get update
}

install_packages() {
    PACKAGES="python3-full python3-numpy python3-matplotlib python3-lxml python3-pyqt5 -y"
    info "Installing packages: $PACKAGES"
    sudo apt-get install -y $PACKAGES
}

main() {
    info "This script will install pprz-py-plotter on your Ubuntu/Debian machine."
    info "The repository for this project will be downloaded on your current directory."
    info "If you want to install it in another directory, please cd into that directory before running this script."
    info "Do you want to continue? (y/n)"

    read -r response
    
    if [ "$response" != "y" ]; then
        info "Installation aborted!"
        exit 1
    fi
    
    update_system
    install_packages

    git clone https://github.com/Swarm-Systems-Lab/pprz-py-plotter.git

    info "Installation completed!"
    info "cd into pprz-py-plotter directory and run GUI with ./pprz-py-plotter"
}

# Run!
main