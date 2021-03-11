import jinja2
import os
import time
import requests

from skinnywms.data.fs import Availability
from skinnywms.plot.magics import Plotter

from skinnywms.plot.magics import Styler
import skinnywms
from skinnywms.server import WMSServer

from flask import Flask, request, Response, render_template, send_file, jsonify
from IPython.lib import backgroundjobs as bg

jobs = bg.BackgroundJobManager()
application = Flask(__name__)


loader = jinja2.ChoiceLoader(
    [
        application.jinja_loader,
        jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(skinnywms.__file__), "templates")
        ),
    ]
)

application.jinja_loader = loader


svr = WMSServer(Availability("./docs/examples/test.grib"), Plotter(), Styler())


@application.route("/wms", methods=["GET"])
def wms():

    return svr.process(
        request,
        Response=Response,
        send_file=send_file,
        render_template=render_template,
        reraise=True,
    )


@application.route("/status", methods=["GET"])
def status():
    return jsonify(
        dict(
            pid=os.getpid(),
        )
    )


def _task(port):
    print("Start task", port)
    try:
        application.run(host="localhost", port=port)
    except Exception as e:
        print(e)
    print("End task", port)


class State:

    job = None
    url = None


STATE = State()


def start_wms():

    if STATE.job is not None and STATE.url is not None:
        if STATE.job.status == STATE.job.stat_running:
            return STATE.url
        jobs.flush()
        STATE.job = STATE.url = None

    for port in range(5000, 10000):
        STATE.job = jobs.new(_task, port)
        while STATE.job.status is STATE.job.stat_created:
            time.sleep(0.1)

        n = 0
        while n < 3:
            status = f"http://localhost:{port}/status"
            try:
                r = requests.get(status)
                r.raise_for_status()
                if r.json()["pid"] == os.getpid():
                    STATE.url = f"http://localhost:{port}/wms"
                    return STATE.url
            except requests.exceptions.HTTPError as e:
                print(status, e)
                break
            except requests.exceptions.ConnectionError as e:
                print(status, e)
                time.sleep(1)
                n += 1

    assert False, "Cannot allocate a port"
