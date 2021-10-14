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

def Run_Scan(path_to_compiled_binary, log_file, kill_option):
    output = subprocess.check_output(['/bin/ps', '-eo', 'pid,user'])

    output = str(output)

    output_list = output.split("\n")

    output_list.pop(0)
    #print(output_list)

    for entry in output_list:
        try:
            if entry != "":
                entry = entry.strip()
                secondary_list = entry.split(" ")
                
                PID = secondary_list[0]
                user = secondary_list[1]

                PID_output = subprocess.check_output(['{}'.format(path_to_compiled_binary), '{}'.format(PID.strip())])
                PID_output = str(PID_output)
                
                if "PID is" in PID_output:
                    process_path = PID_output.split(":")[1].strip()
                    #print(process_path)
                    string_output = subprocess.check_output(['/usr/bin/strings', '{}'.format(process_path)])
                    string_output = str(string_output)

                    if "/Mythic/agent_code" in string_output:  #****EDIT THIS LINE TO CHANGE THE STRING YOU ARE SEARCHING FOR****
                        print("Found ya Mythic! In Process {0} at PID {1}".format(process_path, PID))

                        current_time = time.strftime('%l:%M%p %z on %b %d, %Y')

                        with open('{}'.format(log_file), 'a') as f:
                            f.write(current_time + ":" + " " + PID + " " + user + " " + process_path)
                            f.write("\n")

                        if kill_option == "yes":
                            kill_output = subprocess.check_output(['/bin/kill', '-9', '{}'.format(PID)])
                            print("Process should be killed now.")
        
        except ValueError as e:
            pass

    return

def main(path_to_compiled_binary, output, kill_option):

    while True:
        Run_Scan(path_to_compiled_binary, output, kill_option)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="String Killer searches all running processes on MacOS and kills/logs any process which contains a string of your choice.")
    parser.add_argument('-path', action='store', dest="path_to_compiled_binary", default="", help="Provide the full path to the compiled PID_resolver code. See PID_resolver.c for source code. Sometimes errors if you do not provide full path")
    parser.add_argument('-o', action='store', dest="output", default="StringKiller_log.txt", help="Provide the full path where you want your log file to be placed.")
    parser.add_argument('-kill', action='store', dest="kill", default="no", help="Decide whether or not you want to kill the process which contains your chosen string. Your options are yes or no. The default is no.")
    args = parser.parse_args()

    #check args
    if args.path_to_compiled_binary == "":
        print("You must provide the path to the compiled PID_resolver binary, or else this code will not work.")
        sys.exit()

    if os.path.exists(args.path_to_compiled_binary) != True:
        print("Please try again, apparently your provided compiled binary does not exist on your system.")
        sys.exit()

    if len(args.output) > 1024 or len(args.path_to_compiled_binary) > 1024:
        print("One of your provided arguments has too long of a path, please use a normal path.")
        sys.exit()

    if str(args.kill) != "yes" and str(args.kill) != "no":
        print("Please choose yes or no for your kill option.  E.g. -kill yes")
        sys.exit()


    main(str(args.path_to_compiled_binary), str(args.output), str(args.kill))
#print(output_list)
