import serial
import sys

def read(port):
  return port.readline().strip()

def write(port, string):
  port.write(string + "\r\n")
  return port.readline().strip()


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage: sudo python setup_lora_mote.py /dev/ttyACM0"
    print "check sudo dmesg to figure out the correct device to use"
    print "Expect a 'success' message as an output"
    exit(0)

  dev = sys.argv[1]
  port = serial.Serial(dev, 57600)

  port.timeout = 8
  port.xonxoff = False
  port.rtscts = False
  port.dsrdtr = False
  port.writeTimeout = 0

  write(port, 'sys reset')
  write(port, 'mac set devaddr 00000022')
  write(port, 'mac set deveui 1234123412341237')

  write(port, 'mac set appeui 1234123412341234')
  write(port, 'mac set appkey 12341234123412341234123412341234')
  write(port, 'mac set adr off')
  write(port, 'mac set sync 34')
  write(port, 'mac set rx2 8 923300000')

  # configure sub-band 7
  for ch in range(0,72):
    write(port, 'mac set ch status %d %s'%(ch,
      'on' if ch in range(49,51+1) else 'off'))
  write(port, 'mac save')
  write(port, 'mac join otaa')
  response = read(port)
  if response == 'accepted':
    print "Success"
  else:
    print "Failed to join gateway over otaa"
