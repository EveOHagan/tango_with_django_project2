from django.http import HttpResponse
import os,datetime
from multiprocessing import Process

        
def live_server_test(url,user):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    work_dir = os.path.join(BASE_DIR, 'Online')
    os.chdir(work_dir)    
    os.system('python run_tests.py -u '+url+' -s '+user+' -d '+datetime.date.today().strftime("%Y-%m-%d "))    
    
    
def RangoTest(request):
    url = str(request.GET.get('url'))    
    userid = str(request.GET.get('id'))  
    
    p = Process(target=live_server_test, args=(url,userid))
    p.start()
    
    return HttpResponse("OK")
    
def TestProgress(request):
    
    userid = str(request.GET.get('id'))  
    
    result = ''
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    work_dir = os.path.join(BASE_DIR,'Online','Output',userid,'status.txt')
    
    if (os.path.exists(work_dir)):
        result += open(work_dir, 'r').read()        
        
    return HttpResponse(result)
    