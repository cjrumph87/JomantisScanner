#!/usr/bin/env python3
import sys
import re #imports regex objects
import PySimpleGUI as sg
import nmap
global checker
checker = 0

def operating_system(file, sep=" "):
    o_list = []
    dict = {}
    for line in file.readlines():
        list = line.split(" ")
        pattern = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        if "Running:" in list:
            os = " ".join(list[1:])
            os = os.strip("\n")
            dict.update({ip:os})
            if os not in o_list:
                o_list.append(os)
        try:
            if re.match(pattern, list[4]):
                ip = list[4]
                ip = ip.strip("\n")
            else:
                continue
        except:
            continue

    global history
    history = []

    for item in o_list:
        print(item)
        history.append("\n"+item)
        for key, value in dict.items():
            if item == value:
                print(key)
                history.append(key)
        print("")

def get_ips(file):
    print("List of IPs:")

    global history
    history = []

    for line in file.readlines():
        list = line.split(" ")
        pattern = (r"(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$)")
        try:
            if re.match(pattern, list[4]) and "Nmap" in list:
                ip = list[4]
                print(ip.strip("\n"))
                history.append(ip.strip("\n"))
            elif "Nmap" and "scan" in list:
                ip = (list[5].replace(")","").replace("(",""))
                print(ip.strip("\n"))
                history.append(ip.strip("\n"))
        except:
            continue

def get_services(file):
    print("Getting services of machines with open ports.")
    num = 0
    counter = 0

    global history
    history = []

    for line in file.readlines():
        list = line.split(" ")
        pattern = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        if "STATE" in list:
            print("\nMachine #" + str(num))
            print("IP = " + ip.strip("\n"))
            history.append("\nMachine #" + str(num))
            history.append("IP = " + ip.strip("\n"))
        if ("open" in list or "filtered" in list) and "closed" not in list and "1000" not in list:
            print(line.strip("\n"))
            history.append(line.strip("\n"))
            counter = counter + 1
        try:
            if re.match(pattern, list[4]):
                ip = list[4]
            else:
                continue
        except:
            continue
        num = num + 1
    if counter == 0:
        print("No machines have open ports.")

def get_mac(file):
    print("List of Mac Address's")

    global history
    history = []

    for line in file.readlines():
        list = line.split(" ")
        pattern = (r"(^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$)")
        #print(list)
        if "MAC" in list:
            mac= list[2]
            print(mac)
            history.append(mac)

def start_pop_up():
    sg.theme('Dark Grey 13')

    layout = [[sg.Text("Please type the filename or select browse: ", font=("courier", 12))],
                [sg.Input(), sg.FileBrowse()],
                [sg.OK(), sg.Cancel()]]
    window = sg.Window('Nmap File Name', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        global file_name
        file_name = values[0]
        window.close()
        global file
        file = open(file_name)
    window.close()

def do_nmap():
    global file
    file = open('nmap.txt', 'w+')
    print("Nmap Starting")
    nmScan = nmap.PortScanner()
    print("Performing nmap scan on : "+str(ip_range))
    file.writelines(nmScan.scan(ip_range, '21-443'))

def operation_selection():
    sg.theme('Dark Grey 13')

    layout = [[sg.Text("Which operation to perform:\n Enter 'os' to list Operating Systems.\n Enter 'ip' to list IP Addresses"
                       "\n Enter 'sv' to list Open Ports & Services.\n Enter 'mc' to list MAC Addresses.")],
              [sg.Input()],
              [sg.OK(), sg.Cancel()]]

    window = sg.Window('Choose an operation to perform', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        global aug
        aug = values[0]
        window.close()

def save_output():
    sg.theme('Dark Grey 13')

    layout = [[sg.Text("Do you wish to save output to file? \n Type 'yes' or 'no'")],
              [sg.Input()],
              [sg.OK(), sg.Cancel()]]

    window = sg.Window('Save Results', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        window.close()
        if values[0].title() == "yes".title():
            sg.theme('Dark Grey 13')

            layout = [[sg.Text("Please enter a file name: ")],
                    [sg.Input()],
                    [sg.OK(), sg.Cancel()]]

            window = sg.Window('Create New File', layout)
            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED:
                    break
                window.close()
                file=open(values[0], 'w')
                file.write("\n".join(history))
                file.close()
                print("\nSaving Output to: "+values[0])
        elif values[0].title() == "no".title():
                print("\nNot Saving Output.")
        else:
                print("\nInvalid Response\n Closing program.")


def main():
    start_pop_up() #first window to select file or enter ip address

    #do_nmap() #runs an nmap scan if ip address was given

    operation_selection() #second window to select augment
    sys.argv = [sys.argv[0], aug]

    if sys.argv[1] == "os": #functional
        operating_system(file)
    if sys.argv[1] == "ip": #functional
        get_ips(file)
    if sys.argv[1] == "sv": #functional
        get_services(file)
    if sys.argv[1] == "mc": #functional
        get_mac(file)

    #print("\n".join(history))
    save_output() #gives option and means to save output to file

    file.close()

if __name__ == "__main__":
    main()