import sys
import os
import string
import math
import urllib2

GDpath = "/home/rovin/GDSync/"
if not os.path.exists(GDpath):
  os.makedirs(GDpath)

def WaitForInput():
  result = dict()
  result['valid'] = False
  s = raw_input(">> ");
  l = s.split()
  while ' ' in l:
    l.remove(' ')
  if len(l) < 1:
    return result
  if l[0] == "ls":
    result['valid'] = True
    result['command'] = "ls"
  elif l[0] == 'x':
    result['valid'] = True
    result['command'] = 'x'
  elif l[0] == 'lsl':
    result['valid'] = True
    result['command'] = "lsl"
  elif l[0] == 'dl' and len(l) == 2:
    result['valid'] = True
    result['command'] = 'dl'
    result['arg'] = int(l[1])
  return result

def ListFiles(service):
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  """
  for i in result:
    print i
    print
    print
  """
  allfiledetails = list()
  for i in result:
    filedetails = dict()
    for k, v in i.items():
      if k == u"ownerNames":
        filedetails['ownerNames'] = v
      elif k == u"title":
        filedetails['title'] = v
      elif k == u"modifiedDate":
        filedetails['modifiedDate'] = v
      elif k == u"id":
        filedetails['fileId'] = v
      elif k == u'exportLinks':
        filedetails['kind'] = 'doc'
        links = []
        for k1, v1 in v.items():
          links.append(v1)
        filedetails['downloadLinks'] = links
        """
        elif k == u'downloadUrl':
          filedetails['kind'] = 'other1'
          links = [].append(v)
          filedetails['downloadLinks'] = links
        """
      elif k == u'webContentLink':
        filedetails['kind'] = 'other2'
        links = [].append(v)
        filedetails['downloadLinks'] = i.get(u'webContentLink')
    if 'kind' not in filedetails:
      filedetails['kind'] = 'unspecified'
    if 'downloadLinks' not in filedetails:
      filedetails['downloadLinks'] = []
    allfiledetails.append(filedetails)
  
  return allfiledetails

def DownloadFile(service, filename, fileid, filekind, filelinks):
  print "Downloading file ", filename
  if filekind == 'doc':
    resp, content = service._http.request(filelinks[1])
    f1 = open(GDpath + filename, 'wb')
    f1.write(content)
    f1.close()
    """
    s = urllib2.urlopen(filelinks[1])
    content = s.read()
    s.close()
    d = open(GDpath + "gg2", 'wb')
    d.write(content)
    d.close()
    """
  elif filekind == 'other2' or filekind == 'other1':
    """
    resp, content = service._http.request(filelinks[0])
    f1 = open(GDpath + filename, 'wb')
    f1.write(content)
    f1.close()
    """
    temp = os.system("wget " + str(filelinks[0]))
    f1 = open(GDpath + filename, 'wb')
    f1.write(temp)
    f1.close()

  return True


