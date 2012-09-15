# -*- coding:  iso-8859-1 -*-
"""
Modified 2012-06-03 by Fazal Majid

xmppic.py:  an XMP Image parser.
date:     2006-07-12
Roberto Zoia (roberto@zoia.org)

Parses JPEG images with XMP metadata (More information
about XMP can be found at http://www.adobe.com/products/xmp/).

xmppic.py is a minor hack of the rdfpic.py (v1.1) plugin
for PyBlosxom.  (rdfpic.py was developed by Roberto De Almeida,
and parses JPEG images with metadata inserted using rdfpic, 
http://jigsaw.w3.org/rdfpic).

xmppic.py has been used to extract metadata inserted by PixVUE
(http://www.pixvue.com) in more than 4000 jpeg images with good
results.


Usage:
  import xmppic

  if xmppic.verify_installation():
    data = xmppic.parse("testimage.jpg")
    print data
  
"""


def verify_installation():
  # Try to import libxml2
  try:
    import libxml2
    
  except ImportError:
    print "I could not find the libxml2 module."
    print
    return 0

  # Is PIL installed?
  try:
    import Image

    # Let's check if it was patched.
    import JpegImagePlugin
    if not hasattr(JpegImagePlugin, 'COM'):
      print "You need to patch your Image (Python Imaging Library) module."
      print "Take a look at:"
      print 
      print "  http://groups.yahoo.com/group/python-list/message/110144"
      print
      return 0
    
  except ImportError:
    print "I could not find the Image (Python Imaging Library) module."
    print
    return 0

  return 1


import time
import os
import libxml2
import Image


def purgerdf(rdf):
  """
  Purga los caracteres marcianos del texto.
  A parserdf no le gustan los \x00, y es lo
  que está en la primera de la data de la imagen.
  """
  rdf.replace("\x00", "")  
  rdf0 = rdf[rdf.find('<?'):]
  return rdf0.strip()
  
def parserdf(rdf):
  xml = libxml2.parseDoc(rdf)
  
  ctxt = xml.xpathNewContext()
  ctxt.xpathRegisterNs('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
  ctxt.xpathRegisterNs('technical', 'http://www.w3.org/2000/PhotoRDF/technical-1-0#')
  #ctxt.xpathRegisterNs('dc', 'http://www.w3.org/2000/PhotoRDF/dc-1-0#')
  ctxt.xpathRegisterNs('dc', 'http://purl.org/dc/elements/1.1/')
  ctxt.xpathRegisterNs('aux', 'http://ns.adobe.com/exif/1.0/aux/')
  ctxt.xpathRegisterNs('xmp', 'http://ns.adobe.com/xap/1.0/')
  ctxt.xpathRegisterNs('photoshop', 'http://ns.adobe.com/photoshop/1.0/')
  ctxt.xpathRegisterNs('content', 'http://sophia.inria.fr/~enerbonn/rdfpiclang#')

  metadata = {}
  for item in ctxt.xpathEval('//rdf:Description'):
    created = item.prop('CreateDate')
    if created:
      metadata['createdate'] = created
    #import code
    #code.interact(local=locals())
  for item in ctxt.xpathEval('//rdf:Description/*'):
    # ¿quién me garantiza que los tags están en minúsculas?
    metadata[item.name.lower()] = item.content

  return metadata


def parse(filename):
  """
  Parses the image for XMP metadata.  Returns the data
  as a dictionary if data is found, None otherwise.
  """
  im = Image.open(filename)
  
  # Read metadata.
  try:
    rdf = im.app['APP1']   # APP1 as described by Adobe for XMP
  except (KeyError, AttributeError):
    return None   # no tags, return an empty dictionary
  rdf = purgerdf(rdf)
  
  if not rdf.isspace() and len(rdf)>1:
    metadata = parserdf(rdf)
    for k in metadata.keys():
      metadata[k] = metadata[k].replace("\n","").strip()
    return metadata
  else:
    return None
