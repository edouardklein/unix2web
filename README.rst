================
unix2web
================
----------
Expose a UNIX filter on a web page
----------

Purpose
=============

You have an UNIX filter that does one job and do it well. For example it converts a .doc file to PDF :
    doc2pdf < file.doc >file.pdf

This tool lets you host a nice web page where people can upload the input file and download the output file. This is
useful if UNIX-disabled people need to use your filter.

In a matter of minutes you can make an unix script available to the world on e.g. an AWS EC2 instance.

Installation
=============

We assume you have a UNIX-like server where your filter works (this tool does not handle the installation of your filter
or its dependencies).

Clone the repo somewhere :

    git clone https://github.com/edouardklein/unix2web/

Change the index.html file to your liking (most notably the title and description).

Modify unix2web.wsgi if you want the webapp to live somewhere else than /var/www/unix2web/ (not useful if you intend
to only run one filter on the server).

Same procedure for 100web2unix.conf

Same procedure for unix2web.py

Review the install.sh file, modify if necessary, then upload all the files on your server and run install.sh
    scp -i private_key.pem *.* login@example.com:/tmp/
    ssh -i private_key.pem login@example.com 'cd /tmp/ && sudo sh install.sh'


Example use cases
=========

Converting .doc to .pdf from anywhere.

Compiling LaTeX files.

I'd be happy to hear about your uses. If you deploy this, please send me a word.

Security
========

Security is hard, so we did not do it beyond the obvious (not using the user's filename).

Easy to DDoS (just send a big file).

No password protection.

We advise to deploy this behind a hard-to-find, non-indexable URL and to share the link wisely.


Bugs and Todo
============

Near future
----------

This probably scales badly (untested).

The error output comes all at once, would be nice if, for long processes, it came as it appears server-side.

Security is bad. At least we should check input size and kill long processes.

Output files are not cleaned up (easily doable with a cron-job, though).

Distant future
-------------

Parsing the --help string à la docopt and automatically creating an interface for the options would be wonderful.

Author
======
See http://rdklein.fr

License
=======

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

