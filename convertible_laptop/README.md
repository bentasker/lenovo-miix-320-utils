# Auto Touchscreen Rotation

This uses `watch_tablet` to keep track of when the tablet is detached from the keyboard and then kicks off an automatic rotation script

```sh
sudo pacman -S xorg-xinput onboard
sudo usermod -a -G input $USER
yay -S detect-tablet-mode-git
cp watch_tablet.yml ~/.config/
cp auto_rotate.py ~/bin
```

Launch `onboard-settings` and then navigate to Keyboard. Change the input event source dropdown to GTK.

Add an entry to `~/.xinitrc` or add a startup app to your desktop environment, to run `watch_tablet`
