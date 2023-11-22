# Author:  Etienne Dubois, FR4RX
# Date:    November 22, 2023

## The goal of this program is to allow the use of the Malahit DSP SDR receiver with Simon Brown's SDR Console software,
## by syncing the frequency of OmniRig RIG2 (Malahit via USB) with RIG1 (SDR Console - CW Skimmer option).
## 
## This method is valid at the current date (nov. 2023), with SDR Console version 3.3 beta build 3131.
## Future updates might include built-it support for the Malahit SDR, rendering this trick obsolete.
## 
## The idea behind this trick is that, while the normal CAT control of SDR Console tracks any change in tuned frequency,
## the 'CW Skimmer' option on the other hand provides another CAT control that only tracks changes in center frequency.
## The Malahit needs to stay fixed on the center frequency used by SDR Console, so the software can allow the user
## to independently tune to any signal in the visible spectrum, without the Malahit jumping to that tuned frequency.
## The Malahit needs to only change its frequency in sync with any change of center frequency on SDR Console instead.
## 
## Note that you won't be able to use the CW Skimmer software alongside this trick,
## as changing frequency in CW Skimmer will make the Malahit follow, which is unwanted here.
## 
## To configure everything, first make sure the Malahit is plugged in via USB and drivers are installed properly.
## 
## In SDR Console, go to the radio definitions, click on the 'Search' button, under the 'SoftRock' entry click on 'XTAL'.
## Enter any frequency you want (I used 1MHz), as this will not matter with what we are doing here.
## Then, under 'Default soundcard' select 'Malahit IQ' (the USB soundcard I/Q output of the Malahit SDR).
## Validate, then select the newly added 'XTAL <frequency>' radio, choose 192 kHz as the 'Bandwidth' and click 'Start'.
## You should be able to see the same spectrum show up in SDR Console as the one on the Malahit screen.
## If the spectrum is too high or low, go under the 'View' tab, and adjust the 'Scale Low/High' under 'Spectrum'.
## 
## With SDR Console now operational, go to the 'View' tab, and click on 'Select' under 'More options...'.
## You will see 'CW Skimmer' in the list, tick the checkbox to enable it, validate and restart SDR Console as requested.
#
## Now go back to the 'View' tab, and click on 'CW Skimmer' under 'More options...' to the far right,
## assuming you already have a virtual serial port software installed and configured (I used VSP Manager),
## select the serial port you want to use and tick the checkbox next to it.
## An 'Output device' has to be selected, but will not be used for what we are trying to do here,
## so select an unused/muted sound card (I used a virtual audio cable), I/Q data will be sent to it.
## Check the 'Enable' box at the top to enable the 'CW Skimmer' option.
## 
## After these preliminary steps all done, configure OmniRig with RIG1 linked to the 'CW Skimmer' option,
## and RIG2 linked to the Malahit SDR CAT control.
## 
## Here are the settings I used for SDR Console:
## - Rig type:  TS-2000
## - Port:  the other side of the serial port pair configured in 'CW Skimmer' above
## - Baud rate:  19200
## - Data bits:  8
## - Parity:  None
## - Stop bits:  1
## - RTS:  High
## - DTR:  High
## - Poll int., ms:  200
## - Timeout, ms:  100
## 
## Here are the settings I used for the Malahit SDR:
## - Rig type:  TS-480
## - Port:  check your device manager to find what COM port the Malahit uses
## - Baud rate:  19200
## - Data bits:  8
## - Parity:  None
## - Stop bits:  1
## - RTS:  High
## - DTR:  High
## - Poll int., ms:  500
## - Timeout, ms:  4000
## 
## Everything should now be configured properly.
## 
## To run this program, you need to have Python installed on your system (I used Python 3.8.0).
## This script requires the installation of the package 'pywin32', so open a terminal window (cmd),
## and run the following command: 
##   python -m pip install pywin32
## 
## After the installation is completed, you should now be ready to run this program!


import win32com.client  # python -m pip install pywin32
import time


print("Program started (press Ctrl+C to exit, or close the console window)", end="\n\n")

omnirig = win32com.client.Dispatch("Omnirig.OmnirigX")
time.sleep(0.5)

rig1 = omnirig.Rig1
rig2 = omnirig.Rig2

print("Connected to Omni-Rig", end="\n\n")

if rig1.FreqA == rig2.FreqA:
    print(f"Frequencies already in sync at  >  {rig1.FreqA:,}".replace(',', '.'), end="\n\n")

newfreq = None
loop = True

while loop:
    try:
        if rig1.FreqA != rig2.FreqA and newfreq != rig1.FreqA:
            print(f"Syncing frequency to  >  {rig1.FreqA:,}".replace(',', '.'), end="\n\n")
            
            newfreq = rig1.FreqA
            rig2.FreqA = rig1.FreqA
        
        time.sleep(0.1)
    
    except KeyboardInterrupt:
        loop = False

print("Program ended", end="\n\n")
