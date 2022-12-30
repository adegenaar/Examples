""" GUI """

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

# create the root window
root = ttkb.Window(themename="darkly")

# create the widgets
volt_meter = ttkb.Meter(root, bootstyle=SUCCESS, subtextstyle=SUCCESS, textright="V")
volt_meter.pack(side=LEFT, padx=5, pady=10)
volt_meter.configure(subtext="Volts")

amp_meter = ttkb.Meter(root, bootstyle=WARNING, subtextstyle=WARNING, textright="A")
amp_meter.pack(side=LEFT, padx=5, pady=10)
amp_meter.configure(subtext="Amps")

# amountused is the current value of the meter
# amounttotal is max limit of the meter
volt_meter.configure(amountused=50, amounttotal=60)
amp_meter.configure(amountused=3, amounttotal=5)
root.mainloop()
