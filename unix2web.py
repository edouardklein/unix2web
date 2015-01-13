from __future__ import print_function
"""Run a UNIX filter on an uploaded file, download the result

Code on https://github.com/edouardklein/unix2web/

    This file is part of unix2web.

    unix2web is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with unix2web.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'Edouard Klein <edou -at- rdklein.fr>'

import os
from flask import Flask, request, Response, jsonify
import logging
logging.basicConfig(filename='/tmp/debug.log', level=logging.DEBUG)
from subprocess import Popen, PIPE

app = Flask(__name__)

# Back port of the with TemporaryDirectory()... syntax from
# https://stackoverflow.com/questions/19296146/with-tempfile-temporarydirectory
# Thanks.
import warnings as _warnings
import os as _os
from tempfile import mkdtemp, mkstemp

class TemporaryDirectory(object):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.
    """

    def __init__(self, suffix="", prefix="tmp", dir=None):
        self._closed = False
        self.name = None # Handle mkdtemp raising an exception
        self.name = mkdtemp(suffix, prefix, dir)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def cleanup(self, _warn=False):
        if self.name and not self._closed:
            try:
                self._rmtree(self.name)
            except (TypeError, AttributeError) as ex:
                # Issue #10188: Emit a warning on stderr
                # if the directory could not be cleaned
                # up due to missing globals
                if "None" not in str(ex):
                    raise
                print("ERROR: {!r} while cleaning up {!r}".format(ex, self,),file=_sys.stderr)
                return
            self._closed = True
            if _warn:
                self._warn("Implicitly cleaning up {!r}".format(self),
                           ResourceWarning)

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def __del__(self):
        # Issue a ResourceWarning if implicit cleanup needed
        self.cleanup(_warn=True)

    # XXX (ncoghlan): The following code attempts to make
    # this class tolerant of the module nulling out process
    # that happens during CPython interpreter shutdown
    # Alas, it doesn't actually manage it. See issue #10188
    _listdir = staticmethod(_os.listdir)
    _path_join = staticmethod(_os.path.join)
    _isdir = staticmethod(_os.path.isdir)
    _islink = staticmethod(_os.path.islink)
    _remove = staticmethod(_os.remove)
    _rmdir = staticmethod(_os.rmdir)
    _warn = _warnings.warn

    def _rmtree(self, path):
        # Essentially a stripped down version of shutil.rmtree.  We can't
        # use globals because they may be None'ed out at shutdown.
        for name in self._listdir(path):
            fullname = self._path_join(path, name)
            try:
                isdir = self._isdir(fullname) and not self._islink(fullname)
            except OSError:
                isdir = False
            if isdir:
                self._rmtree(fullname)
            else:
                try:
                    self._remove(fullname)
                except OSError:
                    pass
        try:
            self._rmdir(path)
        except OSError:
            pass
#End of Backport


@app.route('/tmp/<file>')
def get_output(file):
    logging.debug('GET on file '+file)
    return open('/tmp/'+file, 'r').read()  # Not platform independent FIXME.

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    logging.debug('Request on /')
    if request.method == 'POST':
        logging.debug('POST')
        file = request.files['file']
        if file:
            with TemporaryDirectory() as tmpdir:
                logging.debug('saving on '+os.path.join(tmpdir, 'input'))
                file.save(os.path.join(tmpdir, 'input'))
                (_,output_file_name) = mkstemp()
                p = Popen("(date>&2; sed s/the web/UNIX/gI <input)>"+output_file_name, shell=True, cwd=tmpdir, stderr=PIPE)
                (_,stderr) = p.communicate()
                logging.debug('Got stderr : '+stderr)
                return jsonify(stderr=stderr, outputfile_url=output_file_name)
    logging.debug('GET')
    return open("/var/www/unix2web/index.html", 'r').read()

@app.route('/index.css')
def wrapper():
    resp = Response(response=open('/var/www/unix2web/index.css', 'r').read(),
                    status=200,
                    mimetype="text/css")
    return resp

if __name__ == '__main__':
    app.run()
