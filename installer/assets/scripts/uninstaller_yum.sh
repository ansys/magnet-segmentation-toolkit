while true; do
    read -p "Require sudo permission to uninstall this package. Do you want to continue?(Y/N): " user_selection
    if [ "$user_selection" = "Y" ] || [ "$user_selection" = "N" ]; then
        break
    fi
    clear
done
printf "\n"
if [ "$user_selection" = "Y" ]; then
    #Check sudo
    sudo -v >/dev/null 2>&1
    root_check=$?
    if [ $root_check -eq 0 ]; then
        echo "Uninstalling Ansys Magnet Segmentation Toolkit......."
        sleep 2
        sudo yum remove -y ansys_magnet_segmentation_toolkit.x86_64
        sudo sed -i '/# Add alias for Ansys Magnet Segmentation Toolkit/d' ~/.bashrc
        sudo sed -i  '/alias  ansys_magnet_segmentation_toolkit/d' ~/.bashrc
        printf "\nUninstalled successfully...\n"
    else
        echo "You don't have access to sudo. Please try again..."
    fi
else
    # Script aborted by user
    printf "Aborting....\nUser permission denied.... \n\n"
    echo "Ansys Magnet Segmentation Toolkit package requires sudo access to uninstall."
fi