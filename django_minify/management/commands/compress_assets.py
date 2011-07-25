from optparse import make_option
import os
import time
import hashlib
import base64
import json
from subprocess import call, PIPE

from django.conf import settings
from django.core.management.base import BaseCommand

path = lambda *a: os.path.join(settings.STATIC_ROOT, *a)

class Command(BaseCommand):
    help = ("Compresses css and js assets defined in settings.MINIFY_BUNDLES")
        
    def generate_static_name(self, name, ftype, base=None, shorthash=None):
        sha = hashlib.sha1(open(path('%s-min.%s' % (name, ftype))).read()).digest()
        shorthash = base64.urlsafe_b64encode(sha[0:8]).rstrip('=')
        name, ext = os.path.splitext('%s.%s' % (name, ftype))
        
        return name + '.' +  shorthash + ext

    def handle(self, **options):
        jar_path = (os.path.dirname(__file__), '..', '..', 'bin',
                   'yuicompressor-2.4.4.jar')
        path_to_jar = os.path.realpath(os.path.join(*jar_path))

        v = ''
        if 'verbosity' in options and options['verbosity'] == '2':
            v = '-v'

        names = {}

        for ftype, bundle in settings.MINIFY_BUNDLES.iteritems():
            names[ftype] = {}
            
            for name, files in bundle.iteritems():
                files_all = []
                for fn in files:
                    files_all.append(fn)

                concatted_file = path('%s-all.%s' % (name, ftype,))
                compressed_file = path('%s-min.%s' % (name, ftype,))
                real_files = [path(f.lstrip('/')) for f in files_all]

                # Concats the files.
                call("cat %s > %s" % (' '.join(real_files), concatted_file),
                     shell=True)

                # Compresses the concatenation.
                call("%s -jar %s %s %s -o %s" % (settings.JAVA_BIN,
                     path_to_jar, v, concatted_file, compressed_file),
                     shell=True, stdout=PIPE)
                     
                names[ftype][name] = self.generate_static_name(name, ftype)
                
                staticname = path(names[ftype][name])
                if not os.path.exists(staticname):
                    os.symlink(compressed_file, staticname)
                
        json_enc = json.JSONEncoder(indent=4, sort_keys=True)
        open(os.path.join(settings.ROOT_PATH, 'names.json'), 'w').write(json_enc.encode(names))
