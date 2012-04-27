#! /usr/bin/env python
# -*-  coding: utf-8 -*-
from json import loads
import sys
import os
from time import sleep
pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.abspath(pathname))
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from applicationinstance import ApplicationInstance


from places.models import Place, Description
#from utils.cache import kes
#from utils.xml2dict import fromstring
DEVELOPER_KEY = 'AIzaSyAd8evO6SwmuE3RoBdaROzLoNGesc386Vg'
GOOGLE_TRANSLATE_URL = 'https://www.googleapis.com/language/translate/v2'
import logging
log = logging.getLogger('genel')
import httplib2
httplib2.debuglevel = 4

from configuration import configuration



import urllib
import urllib2






class TranslationMachine:
    """
    google translation machine
    """
    def __init__(self):
        self.auto_langs = configuration('auto_trans_langs').split(',')


#        self.run()

    def translator(self, query, target, source=None):
        try:
            values = [('key' , DEVELOPER_KEY),
                    ('target' , target),
                    ('q',query[0]),
                    ('q',query[1]),
            ]
            if source:
                values.append(('source',source))
            headers={'X-HTTP-Method-Override':'GET',}
            data = urllib.urlencode(values)
#            print data
            req = urllib2.Request(GOOGLE_TRANSLATE_URL, data, headers)
            response = urllib2.urlopen(req)
            sonuc =  loads(response.read())['data']['translations']
#            print 'sonuc',sonuc
            return sonuc
        except:
            log.exception('unexpected error')


    def run(self):
        for p in Place.objects.filter(translated=False, published=True, active=True):
            log.info('mekan: %s' % p)
            self.translate_place(p)
#            self.update_place_status(p)
            p.get_translation_list(reset=True)
            p.translated = True
            p.save()
            sleep(5)

#    def reTranslate(self):
#        '''yayindaki evlerin auto cevirilerini yeniden yapar.'''
#        for p in Place.objects.filter(translated=False, published=True, active=True):
#            for d in p.descriptions.filter(auto=True):
#                translation = self.translator([p.title,p.description.replace('\n','<br>')],d.lang)
#                d.text = translation[1]['translatedText'].replace('<br>','\n')
#                d.title = translation[0]['translatedText']
#                d.save()

    def translate_place(self,p):
        log.info('CEVRiLECEK: %s ' % p)
#        already_translated_langs = [l for l in p.get_translation_list(reset=True)]
        for l in self.auto_langs:
#            if l not in already_translated_langs:
            d, new = Description.objects.get_or_create(place=p, lang=l)
            if not(new or d.auto):
                continue
            translation = self.translator([p.title,p.description.replace('\n','<br>')],l)
            if translation:
                d.text = translation[1]['translatedText'].replace('<br>','\n')
                d.title = translation[0]['translatedText']
                d.auto = True
                d.save()
            elif new:
                d.delete()


#    def update_place_status(self, p):
#        translated_langs = p.get_translation_list(reset=True)
#        if translated_langs: #TODO: en az bir dil oldugu icin bu herzaman True oluyor.
#            status = p.translation_status
#            p.translation_status = 20
#            if all([ l in translated_langs for l in self.auto_langs ] ):
#                p.translation_status = 30
#            if status != p.translation_status :
#                p.save()
















if __name__ == '__main__':
    o = None
    inst = None
    try:
        inst = ApplicationInstance( '/tmp/gtranslate.pid' )

        o = TranslationMachine()
        o.run()
        if inst:
            inst.exitApplication()
    except SystemExit:
        if inst:
            inst.exitApplication()
        pass
    except:
        if inst:
            inst.exitApplication()
        log.exception('beklenmeyen hata')

