#!/usr/local/bin/python
"""Gallery generation script, based on:
http://tympanus.net/codrops/2011/07/05/fullscreen-slideshow-with-html5-audio/
"""
import os, datetime, json, pprint, EXIF
# see http://zoia.org/blog/2006/08/13/extracting-xmp-metadata-using-python/
import xmppic
xmppic.verify_installation()
from PIL import Image, ImageFile

def pretty_exif(exif):
  display = [str(exif[k]) for k in ('Image Model',) if k in exif]
  lens = []
  if 'EXIF Tag 0xA434' in exif:
    lens.append(str(exif['EXIF Tag 0xA434']))
  if 'EXIF FocalLength' in exif:
    ratio = exif['EXIF FocalLength'].values[0]
    lens.append(('%.0f' % (float(ratio.num)/ratio.den)).strip() + 'mm')
  display.append(' @ '.join(lens))
  exposure = []
  if 'EXIF ExposureTime' in exif:
    exposure.append(str(exif['EXIF ExposureTime']))
  if 'EXIF FNumber' in exif:
    ratio = exif['EXIF FNumber'].values[0]
    exposure.append('f/' + ('%2g' % (float(ratio.num)/ratio.den)).strip())
  display.append(' sec at '.join(exposure))
  if 'EXIF ISOSpeedRatings' in exif:
    display.append('ISO ' + str(exif['EXIF ISOSpeedRatings']))
  return ', '.join(display)

tmpl = '''<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Oswald:400,700">
<link rel="stylesheet" type="text/css" href="js/vegas/jquery.vegas.css">
<link rel="stylesheet" type="text/css" href="js/jscrollpane/jquery.jscrollpane.css">
<link rel="stylesheet" type="text/css" href="css/styles.css">
<link rel="stylesheet" type="text/css" href="photoswipe.css">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
<script src="js/jquery.easing.js"></script>
<script src="js/vegas/jquery.vegas.js"></script>
<script src="js/jscrollpane/jquery.jscrollpane.min.js"></script>
<script src="js/klass.min.js"></script>
<script src="js/gallery.js"></script>
<script src="code.photoswipe.jquery-3.0.5.min.js"></script>
<script>
meta = {json}
</script>
</head>

<body>
  <div id="title">
    <h1>{title}</h1>
    <p id="description"></p>
    <p id="details">Copyright &copy;{year}&nbsp;<a href="http://majid.info/blog/">Fazal Majid.</a> All rights reserved. &mdash; <span id="info"></span></p>
  </div>
  <div id="thumbnails">
    <ul>
{photos}
    </ul>
  </div>
  <div id="pause"><a href="#">Paused</a></div>
</body>
</html>
'''

tn_tmpl = '''      <li><a href="img/{img}"><img src="thumbnails/{img}" alt="{title}" title="{desc}" data-valign="top"></a></li>
'''
imgs = dict()
for img in os.listdir('img'):
  if img.endswith('.jpg'):
    f = open('img/' + img, 'rb')
    exif = EXIF.process_file(f)
    f.close()
    imgs[img] = {str(k): str(v) for k, v in exif.items()}
    imgs[img].update(xmppic.parse('img/' + img))
    imgs[img]['display'] = pretty_exif(exif)

try:
  os.makedirs('thumbnails')
except OSError:
  pass
for img in imgs:
  if os.path.exists('thumbnails/' + img): continue
  i = Image.open('img/' + img)
  i.thumbnail((2500, 100), Image.ANTIALIAS)
  tf = open('thumbnails/' + img, 'wb')
  i.save(tf, quality=75, optimize=1)
  tf.close()

def by_date(x):
  return x[1].get('createdate')  
photos = ''.join(tn_tmpl.format(img=img, title=meta.get('title', img),
                                desc=meta.get('description', ''))
                 for img, meta in sorted(
                   imgs.items(), key=by_date, reverse=True))
f = open('index.html', 'w')
print >> f, tmpl.format(
  title='Afsheen', photos=photos,
  json=json.dumps({img:imgs[img]['display'] for img in imgs}, indent=2),
  year=datetime.date.today().year)
f.close()
