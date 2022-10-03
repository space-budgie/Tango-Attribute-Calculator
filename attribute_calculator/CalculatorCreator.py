# Tango imports
from tango import Util, DevState
from tango.server import Device, command

# Local imports
from attribute_calculator.AttributeCalculator import AttributeCalculator
#from AttributeCalculator import AttributeCalculator

import sys

class CalculatorCreator(Device):
  """A Tango device that creates/deletes AttributeCalculator devices with a specified name."""

  @command(dtype_in=str, doc_in="Create a AttributeCalculator device with a specified name.",
           dtype_out=str, doc_out="Error/success message")
  def CreateDevice(self, device_name):
    # Check for forbidden characters
    if "/" in device_name:
      msg = "Character '/' not allowed in device name."
      self.error_stream(msg)
      return msg
   
    # The name is OK to add
    try:
      Util.instance().create_device("AttributeCalculator", self.location + device_name)
      msg = f"Created device {device_name}."
      self.info_stream(msg)
      return msg
    except Exception as e:
      msg = f"Could not create device {device_name}."
      self.error_stream(msg + "\n" + str(e))
      return msg

  @command(dtype_in=str, doc_in="Delete a AttributeCalculator device with a specified name.",
           dtype_out=str, doc_out="Error/success message")
  def DeleteDevice(self, device_name):
    # Check for forbidden characters
    if "/" in device_name:
      msg = "Character '/' not allowed in device name."
      self.error_stream(msg)
      return msg

    # Delete device
    try:
      Util.instance().delete_device("AttributeCalculator", self.location + device_name)
      msg = f"Deleted device {device_name}."
      self.info_stream(msg)
      return msg
    except Exception as e:
      msg = f"Could not delete device {device_name}."
      self.error_stream(msg + "\n" + str(e))
      return msg

  def init_device(self):
    try:
      Device.init_device(self)
     
      # Store the device location. This is the location where we will add newly created devices to.
      # This creates devices where calculatorcreator is
      # name = self.get_name()
      # last_slash_location = name.rfind('/') # Get the index of the last '/' character
      # self.location = name[:last_slash_location+1]
      self.location = "attributecalculator/calculators/" # for safety we hardcode it. This way devices can't be created or deleted anywhere else.
    except Exception as e:
      self.error_stream("Could not init device." + "\n" + str(e))
      self.set_state(DevState.FAULT)
    else:
      self.set_state(DevState.ON)

def run():
  # Add the AttributeCalculator device to the util instance database, so that the CalulatorCreator device knows how to create one.
  util = Util(sys.argv)
  util.add_class(AttributeCalculator.TangoClassClass, AttributeCalculator)

  CalculatorCreator.run_server()

if __name__=="__main__":
  run()
