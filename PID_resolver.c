//credit to https://stackoverflow.com/questions/14805896/how-do-i-get-the-full-path-for-a-process-on-os-x, to user AlphaMale and DustinB
//I only changed error functionality to avoid printing errors constantly, and also added in check for PID size (shouldn't exceed 5, but wanted to make sure null byte was accounted for)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <libproc.h>

int main (int argc, char* argv[])
{
    int count = 0;
    pid_t pid; int ret;
    char pathbuf[PROC_PIDPATHINFO_MAXSIZE];

    if ( argc > 1 ) {
        if (strlen(argv[1]) > 6)
        {
            printf("Not a valid PID, please enter a valid PID.\n");
            exit(-1);
        }
        pid = (pid_t) atoi(argv[1]);
        
        ret = proc_pidpath (pid, pathbuf, sizeof(pathbuf));
        if ( ret <= 0 ) {
            //fprintf(stderr, "process %d: proc_pidpath ();\n", pid);
            //fprintf(stderr, "    %s\n", strerror(errno));
            count = count + 1; 

        } else {
            printf("PID is %d: %s\n", pid, pathbuf);
        }
    }

    return 0;
}
