import os, csv, json, sys

OUTPUT = 'WAD2_Checkpoint1'
CSV_FILE = 'WAD2repos.csv'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, OUTPUT)
MAIL_SERVER = '@student.gla.ac.uk'

URL_LIST = []
USERID = []
PAIRS = []

def find_cheaters(url, userid):
    for i, item in enumerate(URL_LIST):
        if url == item:
            PAIRS.append([userid, USERID[i]])

    URL_LIST.append(url)
    USERID.append(userid)

def get_url(user_id):
    for i, list_id in enumerate(USERID):
        if list_id == user_id:
            return URL_LIST[i]

if __name__ == "__main__":

    with open(CSV_FILE, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            userid=row[0]
            url=row[1]
            find_cheaters(str(url), str(userid))

    print('Cheaters: ')
    print(PAIRS)
    # print USERID
    # print URL_LIST
    # print not_found
#[Errno 10054] An existing connection was forcibly closed by the remote host
#[Errno 10053] An established connection was aborted by the software in your host machine

    out_str = 'STUDENT,PASSED,FAILED,TIMEOUT,ERRNO,COMMITS,ATTACHMENT1,ATTACHMENT2,URL\n'
    for dirName, subdirList, fileList in os.walk(OUTPUT_DIR):
        userid = dirName.split('\\')[-1]
        if userid != OUTPUT:
            print('UserID: %s' % userid)
            url_id = get_url(userid)
            print(url_id)

            commits = 0
            report_list = ''
            passed = 0
            failed = 69
            err_timeout = 0
            errno = 0
            for fname in fileList:
                if fname == "console_output.txt":
                    with open(os.path.join(dirName, fname)) as data_file:
                        data = data_file.read()
                        if "timeout" in data:
                            err_timeout = 1

                if fname == "report_errors.txt":
                    with open(os.path.join(dirName, fname)) as data_file:
                        data = data_file.read()
                        if "Errno" in data:
                            errno = 1

                if fname != "commits.txt":
                    if fname != "console_output.txt":
                        report_list += os.path.join(dirName, fname) + ','
                else:
                    with open(os.path.join(dirName, fname)) as f:
                        content = f.readlines()
                        content = [c.rstrip('\n') for c in content]
                        content = [c.rstrip('\r') for c in content]
                        #print(content)
                        commits = int(content[0])
                        print("Commits: " + str(commits))

                if fname.endswith('json'):
                    with open(os.path.join(dirName, fname)) as data_file:
                        data = json.load(data_file)

                    passed = str(data).count('True')
                    failed = str(data).count('False')

            out_str += str(userid) + MAIL_SERVER + ',' + str(passed) + ',' + str(failed) + ',' + str(err_timeout) + ',' + str(errno) + ',' + str(commits) + ',' + report_list + str(url_id) + ',' + '\n'

    with open(os.path.join(BASE_DIR, 'results_mail.csv'), "w+") as fo:
        fo.write(out_str)

    print("File has been saved to: " + os.path.join(BASE_DIR, 'results_mail.csv'))

    print("Done!")
    print("")
    print("")
