# Welcome to KG Clicker

More to come on this in the future. The goal of this project is to create an easy to use and reliable screen clicker for the mobile game Kingdom Guard as I didn't like other options that I was finding.

It is also worth pointing out that nothing here is specific to Kingdom Guard other than function names and some task flows. My goal is to keep this as generic as possible so if other use cases / games pop up in the future, this can be applied there as well.

NOTE: Currently this is only setup and designed to work with a Pixel 3. If you have a device with the same screen dimensions (~1088x2150) then it might work, otherwise there is significant configuration that needs to happen to add more supported devices. That being said, it is designed to be able to work with a multitude of devices. If there is eventual demand (highly unlikely), then a "device setup" script might could be worked out.


## Requirements

 - VNC Server for your device
	 - Currently this does everything through VNC but but things have been factored in a way that other connection options are possible such as desktop screen capturing for a emulator like Blue Stacks
	 - DroidVNC seems to be a decent VNC server for Android that doesn't require root
 - Python dependencies
	 - cv2
	 - pillow
	 - numpy
	 - vncdotool
	 - apscheduler
	 - pypyr