from subprocess import Popen, PIPE, TimeoutExpired
import csv, json, sys, os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 30*60 # in seconds (minutes * 60 seconds)

def run_tests(url, userid, deadline):

    dir_student = os.path.join(BASE_DIR, "output", userid)
    if not os.path.exists(dir_student):
        os.makedirs(dir_student)

    args = ['python', 'run_tests.py', '-u', url, '-s', userid, '-d', deadline]
    print("Running: " + ' python' + ' run_tests.py ' + ' -u ' + url + ' -s ' + userid + ' -d ' + deadline)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    try:
        out, err = proc.communicate(timeout=TIMEOUT)
    except:# TimeoutExpired:
        out = "tests timeout after " + str(TIMEOUT) + " seconds"
        err = "tests timeout after " + str(TIMEOUT) + " seconds"

    exitcode = proc.returncode
    #print "***** Output *****"
    #print out
    #print "***** Error *****"
    #print err
    #print "***** Exit Code *****"
    #print exitcode
    #print "***** EOF *****"

    with open(os.path.join(dir_student, 'console_output.txt'), 'w') as fp:
        fp.write("While running: " + ' python' + ' run_tests.py ' + ' -u ' + url + ' -s ' + userid + ' -d ' + deadline + ", I got...")
        fp.write('\n\n\nSTDOUT =====================================================\n')
        try:
            fp.write(out.decode())
        except:
            fp.write(str(out))
        
        fp.write('\n\n\nSTDERR =====================================================\n')
        try:
            fp.write(err.decode())
        except:
            fp.write(str(err))
        
        fp.write('\n\n\nEXITCODE =====================================================\n')
        fp.write(str(exitcode))
        fp.write('\n\n\n===================================================== EOF\n')

if __name__ == "__main__":
    userid='alisa'
    url='https://github.com/candrakupang/mytango'
    run_tests(str(url), str(userid), "2018-07-13")
    
    '''
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="git repository where tests should run")
    parser.add_argument("-s", "--student", help="student number")
    parser.add_argument("-d", "--deadline", help="deadline")
    args = parser.parse_args()

    if args.url is not None and args.student is not None and args.deadline is not None:        
        run_tests(args.url, args.student, args.deadline)        
    else:
        raise BaseException("url, student number and deadline are required!!. Type 'python main_script.py -h' for further help")

'''