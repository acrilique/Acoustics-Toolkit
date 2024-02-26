# Author: Lluc Simó (GitHub: acrilique), 2024
# Description: This script is a helper sheet for acoustics students.

import math
import sys
import os

def spectrum_dict_from_cliuser():
    num_bands = int(input("Enter the number of frequency bands: "))
    spectrum = {}
    for i in range(num_bands):
        band = int(input("Enter the frequency of the band in Hz: "))
        power = float(input("Enter the power in dB SPL: "))
        spectrum[band] = power
    return spectrum

def a_weighting(spectrum_dict):
    a_weighted_spectrum = {}
    for band, power in spectrum_dict.items():
        ra = (12194**2 * band**4) / ((band**2 + 20.6**2) * math.sqrt((band**2 + 107.7**2) * (band**2 + 737.9**2)) * (band**2 + 12194**2))
        a_weighted_spectrum[band] = 20 * math.log10(ra) + 2.0 + power
    return a_weighted_spectrum 

def c_weighting(spectrum_dict):
    c_weighted_spectrum = {}
    for band, power in spectrum_dict.items():
        rc = (12194**2 * band**2) / ((band**2 + 20.6**2) * (band**2 + 12194**2))
        c_weighted_spectrum[band] = 20 * math.log10(rc) + 0.06 + power
    return c_weighted_spectrum

def save_spectrum_csv(spectrum_dict, filename):
    with open(filename, "w") as file:
        for band, power in spectrum_dict.items():
            file.write(f"{band},{power}\n")

def spectrum_dict_from_csv(filename):
    spectrum = {}
    with open(filename, "r") as file:
        for line in file:
            band, power = line.strip().split(",")
            spectrum[int(band)] = float(power)
    return spectrum

def ask_save_spectrum(spectrum_dict, spectrums):
    save = input("Do you want to save the weighted spectrum to a file? (y/n)")
    if save.lower() == "y":
        filename = input("Enter the filename: ")
        save_spectrum_csv(a_weighted_spectrum, filename)
    save = input("Do you want to add the weighted spectrum to the working session? (y/n)")
    if save.lower() == "y":
        spectrums.append(a_weighted_spectrum)

def main():

    spectrums = []
    print("What do you want to do?")
    print("1. Add a new spectrum")
    print("2. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        choice = 0

    if choice == 1:

        spectrums.append(spectrum_dict_from_cliuser())
        
        print("WARNING: All the decibel values will show all floating point decimal\nplaces, but in acoustics we never use more than 1 decimal place.")        
        print(str(len(spectrums))+ " spectrum(s) added.")
        print("__________________________________________________________")
        print("What do you want to do?")
        print("1. Add a new spectrum")
        print("2. Visualize 1 or more spectra")
        print("3. Calculate the A-weighting of a spectrum")
        print("4. Calculate the C-weighting of a spectrum")
        print("5 (or anything else). Exit")

        while choice == 1 or choice == 2 or choice == 3 or choice == 4:
            
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                choice = 0 # this'll be like an error code

            match choice:
                case 1:
                    spectrums.append(spectrum_dict_from_cliuser())
                case 2:
                    nums = input("Enter the indices (starting from 0) of the spectra you want to visualize, separated by commas: ")
                    indices = [int(i) for i in nums.split(",")]
                    for index in indices:
                        print("SPECTRUM "+str(index)+"  "+str(spectrums[index]))
                case 3:
                    index = 0
                    try:
                        index = int(input("Enter the index (starting from 0) of the spectrum you want to calculate the A-weighting: "))
                    except ValueError:
                        index = 0
                    a_weighted_spectrum = a_weighting(spectrums[index])
                    print(a_weighted_spectrum)
                    ask_save_spectrum(a_weighted_spectrum, spectrums)
                case 4:
                    try:
                        index = int(input("Enter the index (starting from 0) of the spectrum you want to calculate the C-weighting: "))
                    except ValueError:
                        index = 0
                    c_weighted_spectrum = c_weighting(spectrums[index])
                    print(c_weighted_spectrum)
                    ask_save_spectrum(c_weighted_spectrum, spectrums)

    print("Goodbye!")
    quit()

if __name__ == "__main__":
    
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130) 
