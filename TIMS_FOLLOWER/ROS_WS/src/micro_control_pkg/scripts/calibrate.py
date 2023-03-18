from sensapex import UMP
ump = UMP.get_ump()
dev_ids = ump.list_devices()

device = ump.get_device(dev_ids[0])

# device
device.calibrate_zero_position()
