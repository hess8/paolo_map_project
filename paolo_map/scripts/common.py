import pickle
import json
import logging
import os
import pickle
import sys
import subprocess
from datetime import datetime
import re


def readFileStrip(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
    else:
        sys.exit("File {} doesn't exist".format(filename))
    return lines

def readFileNoStrip(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = f.readlines()
    else:
        sys.exit("File {} doesn't exist".format(filename))
    return lines

def writeFile(filename,lines):
    with open(filename, 'w') as f:
        f.writelines(lines)

def readJSON(path):
    with open(path, "r") as f:
        return json.load(f)

def writeJSON(path,object):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(object, f, default=str, indent=4)

def readPickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def writePickle(path,object):
    with open(path, 'wb') as f:
        pickle.dump(object,f)

def printLines(filename):
    with open(filename) as file:
      print(file.readlines())

def rmDiacritics(string):
    import unidecode
    return unidecode.unidecode(string)

def rmSingleCharWords(string):
    keep = []
    for word in string.split(' '):
        if len(word) > 1:
            keep.append(word)
    return ' '.join(keep)

def replaceStrs(text,replaceList,newStr):
    for item in replaceList:
        text = text.replace(item,newStr).replace(item.lower(),newStr).replace(item.upper(),newStr).replace(item.capitalize(),newStr)
    return text

def csvToDictionary(path,nColumns):
    '''
    Creates a dictionary from a csv file.
    Returns a dictionary with keys the name of the headers.
    '''
    dict = {}
    csv_data = pd.read_csv(path)
    headersActive = list(csv_data.columns)[:nColumns]
    for header in headersActive:
        dict[header] = list(csv_data[header])
    return dict

def dbFromTag(tag):
    tagDict = {'sd': sdAirport,'our': AirptOurApts, 'aips': AirptOpenAIP, 'xcs': AirptXCS}
    return tagDict[tag]

def getConfirmation(string):
    response = 'None'
    while response.lower() not in ['yy', 'nn']:
        print('\n {}'.format(string))
        response = input('yy/nn ')
        if response.lower() == 'yy':
            return True
        elif response.lower() == 'nn':
            return False

def psql(command, dbname,schemaName):
    psql_command = [
        'psql',
        '-d', dbname,
        '-U', os.getlogin(),
        '-c', command]
    subPopenTry(psql_command)

def tablesToStr(tables,descriptor):
    tableStr = ''
    if tables[0] == "all":
        return tableStr, descriptor
    for table in tables:
        tableStr += f'-t={table}'
        descriptor += f'_{table}'
    return tableStr

def dump(dbName, tables, saveDir, descriptor):
    tableStr,descriptor = tablesToStr(tables,descriptor)
    formatFlag = '-Fc'
    extension = format
    subPopenTry(f'pg_dump --data-only {formatFlag} -d {dbName} {tableStr} > {saveDir}/{dbName}_dump_{descriptor}.custom')

def restoreDump(prevDump, tables, testing):
    tableStr, descriptor = tablesToStr(tables,None)
    if tables[0] != 'all':
        tableStr = '--clean' + tableStr
    dbName = None
    if testing:
        okRestore = True
        dbName = 'sdtests'
    else:
        question = 'You set the dump --restore flag'
        if tableStr == '':
            question += f'\nDo you want to drop the *entire* db {dbName} and restore if from {prevDump}?'
            okRestore = getConfirmation(question) and getConfirmation('Are you sure?')
            # if okRestore: #drop schema and reload

        else:
            question += f'\nDo you want to restore the following tables to {dbName}?'
            for table in tables:
                question += f'\n{table}'
        okRestore = getConfirmation(question) and getConfirmation('Are you sure?')

    if okRestore:
        try:
            os.system(f'pg_restore -d {dbName} {tableStr} {prevDump}')
        except:
            sys.exit('Stop')


def subPopenTry(cmd):
    try:
        if '>' in cmd:
            if isinstance(cmd, str):
                cmd = cmd.replace('  ', ' ').split(' ')
            destination = cmd[-1]
            base_cmd = cmd[:-2]
            with open(destination, "wb") as fh:
                output_lines = watch_proc(subprocess.Popen(base_cmd, stdout=fh, stderr=subprocess.PIPE))
        else:
            output_lines = watch_proc(subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE))
        return output_lines
    except subprocess.CalledProcessError as e:
        sys.exit('Stop: Error output: {} on cmd "{}"'.format(e.stderr, ' '.join(cmd)))
        return e.stderr

def watch_proc(proc):
    output, error = proc.communicate()
    if proc.returncode != 0:
        output, error = proc.communicate()
        raise subprocess.CalledProcessError(proc.returncode, proc.args, output=output, stderr=error)
    elif output:
        return output.splitlines()
    else:
        return []
 # with open("/home/bret/dump.custom", "wb") as fh:  # wb avoids need for text
 #    proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.PIPE)
 #    output, error = proc.communicate()  # probably (None, "")
 #    if proc.returncode != 0:

def flightSource(url):
    sourceID = re.search(r'(\d+)$', url).group(1)
    if 'weglide' in url:
        sourceTag = 'wg'
    elif 'skylines' in url:
        sourceTag = 'sl'
    elif 'online' in url:
        sourceTag = 'ol'
    return f'{sourceTag}_{sourceID}'

def extract_igc_data(file_path):
    """
    Parses an IGC file and extracts flight data into a pandas DataFrame.

    Args:
        file_path (str): The path to the .igc file.

    Returns:
        fixes
    """
    flight = Flight.create_from_file(file_path)
    return flight.fixes


