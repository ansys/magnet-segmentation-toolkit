echo "Uninstalling Magnet Segmentation Toolkit......."
sleep 3

rm -rf ${HOME}/.local/share/applications/magnet_segmentation_toolkit.desktop
rm -rf ${HOME}/.local/usr/share/doc/magnet_segmentation_toolkit

rm -rf ${HOME}/.local/opt/magnet_segmentation_toolkit

sed -i '/# Add alias for Ansys Magnet Segmentation Toolkit/d' ~/.bashrc
sed -i  '/alias  ansys_magnet_segmentation_toolkit/d' ~/.bashrc