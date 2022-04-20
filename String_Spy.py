#!/usr/bin/python2
#String_Spy is written in python2 so that it will work easily on MacOS

# Code written by AsaurusRex 

# BSD 4-Clause License
# Copyright (c) 2020, asaurusrex
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
   
# 3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#    This product includes software developed by AsaurusRex.
# 4. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

import subprocess
import os.path 
import time
import argparse
import sys
import platform
#import threading

def Get_Processes(path_to_compiled_binary, OS):

    process_info_list = list()
    output = subprocess.check_output(['/bin/ps', '-eo', 'pid,user'])

    output = str(output)
    

    output_list = output.split("\\n")

    output_list.pop(0)
    

    for entry in output_list:
        
        try:
            if entry != "":
                entry = entry.strip()
                secondary_list = entry.split(" ")
                
                if secondary_list[0] != "'":
                    PID = secondary_list[0]
                    user = secondary_list[1]

                    if OS == "Darwin":
                        PID_output = subprocess.check_output(['{}'.format(path_to_compiled_binary), '{}'.format(PID.strip())])
                        PID_output = str(PID_output)[:-3] #need to remove a trailing newline
                       
                        if "PID is" in PID_output:
                            process_path = PID_output.split(":")[1].strip()
                            #print(process_path)
                            useful_info = PID + ", " + user + ", " + process_path
                            process_info_list.append(useful_info)
                            
                    elif OS == "Linux":
                        PID_output = subprocess.check_output(['/bin/readlink' , '/proc/{}/exe'.format(PID.strip())])
                        PID_output = str(PID_output)
                        process_path = PID_output
                        useful_info = PID + ", " + user + ", " + process_path
                        process_info_list.append(useful_info)

        except subprocess.CalledProcessError as e:
            print("Unable to open process with PID: {0} due to {1}".format(PID.strip(), e))
            pass


    return process_info_list

def Check_Process_Strings(PID, user, process_path, log_file, string_file):
    try:
        count = 0
        string_output = subprocess.check_output(['/usr/bin/strings', '{}'.format(process_path)])
        string_output = str(string_output)

        with open('{}'.format(string_file), 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line != "":
                line_list = line.split(" ")
                string = line_list[0] #string defined here
                kill_option = line_list[1] #kill option

            if '{}'.format(string) in string_output: 
    
                if count < 1:
                    current_time = time.strftime('%l:%M%p %z on %b %d, %Y')
                    count = count + 1
                    print ("Found suspect process!" + " " +  current_time + ":" + " " + PID + " " + user + " " + process_path +  "; " + "String matched: " + string)

                    if kill_option == "kill":
                        kill_output = subprocess.check_output(['/bin/kill', '-9', '{}'.format(PID)])
                        print("Process should be killed now.")
                    #only log if has not been logged within the hour
                    if os.path.exists('{}'.format(log_file)) == True:
                        with open('{}'.format(log_file), 'r') as f:
                            lines = f.readlines()
                        for line in lines:
                            if process_path in line:
                                line = line.strip()
                                hour = line[0:1]
                                compare_time = current_time.strip()
                                old_hour = compare_time[0:1]
                                if hour == old_hour:
                                    return

                    with open('{}'.format(log_file), 'a') as f:
                        f.write(current_time + ":" + " " + PID + " " + user + " " + process_path + "; " + "String matched: " + string)
                        f.write("\n")

    except subprocess.CalledProcessError as e:
        print("Failed to read process {0} due to {1}".format(process_path, e))
        pass

    return

def main(path_to_compiled_binary, log_file, string_file):

    #check OS: Darwin = Mac, Linux = Linux
    OS = str(platform.system())
    

    while True:

        process_info_list = Get_Processes(path_to_compiled_binary, OS) #list which will have PID, user, and process path information we need.

        #we will show example using 3 threads - can always expand to more threads depending on the number of strings you want to search
        length_processes = len(process_info_list)
        #print(length_processes)
        
        for i in range(length_processes):
            
            element = process_info_list[i]
            element = element.strip()
            if element != "":
                particular_process_list = element.split(",")
                PID = particular_process_list[0]
                PID = PID.strip()

                user = particular_process_list[1]
                user = user.strip()

                process_path = particular_process_list[2]
                process_path = process_path.strip()
                Check_Process_Strings(PID, user, process_path, log_file, string_file)
                

''' THIS IMPLEMENTATION CAN CAUSE ERRORS, BUT COULD PROVIDE A FRAMEWORK TO INTRODUCE MULTITHREADING LATER
                #thread 3
                if i % 3 == 0:
                    #set up thread
                    t3 = threading.Thread(target=Check_Process_Strings, args=(PID, user, process_path, log_file, string_file,))
                    
                    #start thread
                    t3.start()

                #thread 1
                elif i % 3 == 1:
                    #set up thread
                    t1 = threading.Thread(target=Check_Process_Strings, args=(PID, user, process_path, log_file, string_file,))
                    
                    #start thread
                    t1.start()

                #thread 2
                elif i % 3 == 2:
                    #set up thread
                    t2 = threading.Thread(target=Check_Process_Strings, args=(PID, user, process_path, log_file, string_file,))
                    
                    #start thread
                    t2.start()

            #wait for threads to finish?       
            # t3.join()
            # t1.join()
            # t2.join()
            
                    
                  
'''
                
                






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="String Spy searches all running processes on MacOS and kills/logs any process which contains a string of your choice.")
    parser.add_argument('-path', action='store', dest="path_to_compiled_binary", default="", help="Provide the full path to the compiled PID_resolver code. See PID_resolver.c for source code. Sometimes errors if you do not provide full path")
    parser.add_argument('-o', action='store', dest="output", default="String_Spy_log.txt", help="Provide the full path where you want your log file to be placed.")
    #parser.add_argument('-kill', action='store', dest="kill", default="no", help="Decide whether or not you want to kill the process which contains your chosen string. Your options are yes or no. The default is no.")
    parser.add_argument('-string_file', action='store', dest="string_file", default="", help="Provide the path to a file which contains which strings you want to monitor for, and whether you want to kill a process with that string. E.g. \"my_string kill\" or if you wish to only log the process, then just \"my_string log\".  Each new string should be a on new line.")
    args = parser.parse_args()

    #check args
    if args.path_to_compiled_binary == "":
        print("You must provide the path to the compiled PID_resolver binary, or else this code will not work.")
        parser.print_help()
        sys.exit()

    if os.path.exists(args.path_to_compiled_binary) != True:
        print("Please try again, apparently your provided compiled binary does not exist on your system.")
        parser.print_help()
        sys.exit()

    if len(args.output) > 1024 or len(args.path_to_compiled_binary) > 1024:
        print("One of your provided arguments has too long of a path, please use a normal path.")
        parser.print_help()  
        sys.exit()


    # if str(args.kill) != "yes" and str(args.kill) != "no":
    #     print("Please choose yes or no for your kill option.  E.g. -kill yes")
    #     parser.print_help()
    #     sys.exit()

    if str(args.string_file) == "":
        print("You must provide the path to the strings_file, or else this code will not work.")
        parser.print_help()
        sys.exit()

    if os.path.exists(args.string_file) != True:
        print("Please try again, apparently your provided strings_file does not exist on your system.")
        parser.print_help()
        sys.exit()

    main(str(args.path_to_compiled_binary), str(args.output), str(args.string_file))

