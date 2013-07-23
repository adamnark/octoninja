from  simulator_engine import Simulator
from glob import glob
from threading import Thread

# get all the xml files from gpx/
# for each file, load a new simulator
    # init(filename, imei_pool[filename[0]])

def getFileNames():
    return glob("gpx\\*.gpx")
    
def validate(filenames):
    for file in filenames:
        first_char = file[4]
        num = int(first_char) 
        if num < 0 or num > 8:
            raise Exception("filename should start with a number between 0 and 8")
        
def main():
    filenames = getFileNames()
    validate(filenames)
    simulators = [Simulator(filename, int(filename[4])) for filename in filenames]
    threads = []
    for sim in simulators:
        t = Thread(target=sim.start)
        t.start()    
        threads.append(t)
    
    for t in threads:
        t.join()
        
if __name__ == '__main__': 
    main()
