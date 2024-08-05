#!/bin/bash

# Title: Installation script
# Author: Pelochus
# Date: 2024-08-04
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
    update_system
    install_packages
    info "Installation completed!"
    info "Run GUI with ./pprz-py-plotter"
}

# Run!
main