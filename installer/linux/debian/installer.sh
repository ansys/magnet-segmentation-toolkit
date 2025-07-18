#! /bin/bash
clear
printf """Installation started.....\n"""
missing_deps=()
dependencies_available=true
# check zlib
ls /usr/local/lib/libz.so >/dev/null 2>&1
ret=$?
if [ $ret -eq 0 ]; then
    :
else
    missing_deps+=("zlib")
    dependencies_available=false
fi
# check other dependencies
arr=("wget" "gnome" "libffi-dev" "libssl-dev" "build-essential" "libsqlite3-dev" "libxcb-xinerama0")
for x in "${arr[@]}"; do
    c="dpkg -s $x >/dev/null 2>&1"
    eval $c
    ret=$?
    if [ $ret -eq 0 ]; then
        :
    else
        missing_deps+=("$x")
        dependencies_available=false
    fi
done
if [ $dependencies_available = true ]; then
    dpkg -x ./magnet_segmentation_toolkit.deb ${HOME}/.local
    ./postInstallScript.sh
    available=$(cat ~/.bashrc | grep -zoP "# Add alias for Ansys Magnet Segmentation Toolkit \nalias magnet_segmentation_toolkit=~/.local/opt/magnet_segmentation_toolkit/magnet_segmentation_toolkit" | wc -l)
    echo $available
    if [ $available -lt 1 ]
    then
        echo -e "# Add alias for Ansys Magnet Segmentation Toolkit \nalias magnet_segmentation_toolkit=~/.local/opt/magnet_segmentation_toolkit/magnet_segmentation_toolkit" >> ~/.bashrc
    fi
    printf "\nInstallation successful. \nIt is suggested to restart your machine to begin using the software....\n"
else
    echo "Missing dependencies..."
    while true; do
        read -p "Require sudo permission to install dependencies. Do you want to install?(Y/N): " user_selection
        if [ "$user_selection" = "Y" ] || [ "$user_selection" = "N" ]; then
            break
        fi
        clear
    done
    printf "\n"
    if [ "$user_selection" = "Y" ]; then
        sudo -v >/dev/null 2>&1
        root_check=$?
        if [ $root_check -eq 0 ]; then
            install_script="sudo apt-get update -y; "
            install_zlib=false
            for x in "${missing_deps[@]}"; do
                if [ $x == "zlib" ]; then
                    install_zlib=true
                else
                    install_script="$install_script sudo apt-get install $x -y;"
                fi
            done
            if [ $install_zlib = true ]; then
                install_script="$install_script rm -rf ansys-prereq/ ; mkdir -p ansys-prereq; cd ansys-prereq; wget https://zlib.net/current/zlib.tar.gz; tar xvzf zlib.tar.gz; cd zlib-*; make clean; ./configure; make; sudo make install; cd ../..; rm -rf ansys-prereq;"
            fi

            dependencies_available=true
            eval $install_script
            # Confirmation
            # check zlib
            ls /usr/local/lib/libz.so >/dev/null 2>&1
            ret=$?
            if [ $ret -eq 0 ]; then
                :
            else
                missing_deps+=("zlib")
                dependencies_available=false
            fi
            # check other dependencies
            arr=("wget" "gnome" "libffi-dev" "libssl-dev" "build-essential" "libsqlite3-dev" "libxcb-xinerama0")
            for x in "${arr[@]}"; do
                c="dpkg -s $x >/dev/null 2>&1"
                eval $c
                ret=$?
                if [ $ret -eq 0 ]; then
                    :
                else
                    missing_deps+=("$x")
                    dependencies_available=false
                fi
            done
            if [ $dependencies_available = false ]; then
                echo "Unable to install dependencies. Check above logs and try again..."
            else
                dpkg -x ./magnet_segmentation_toolkit.deb ${HOME}/.local
                ./postInstallScript.sh
                available=$(cat ~/.bashrc | grep -zoP "# Add alias for Ansys Magnet Segmentation Toolkit \nalias magnet_segmentation_toolkit=~/.local/opt/magnet_segmentation_toolkit/magnet_segmentation_toolkit" | wc -l)
                echo $available
                if [ $available -lt 1 ]
                then
                    echo -e "# Add alias for Ansys Magnet Segmentation Toolkit \nalias magnet_segmentation_toolkit=~/.local/opt/magnet_segmentation_toolkit/magnet_segmentation_toolkit" >> ~/.bashrc
                fi
                printf "\nInstallation successful. \nIt is suggested to restart your machine to begin using the software....\n"
            fi
        else
            echo "You don't have access to sudo. Please try again..."
        fi
    else
        printf "Install below mentioned dependencies to proceed installation.... \n"
        for x in "${missing_deps[@]}"; do
            echo "$x"
        done
        printf "Dependencies installation required sudo access.\n"
        echo -e '\e]8;;https://installer.docs.pyansys.com/version/stable/installer.html\aFollow prerequisites in this link\e]8;;\a'
    fi
fi