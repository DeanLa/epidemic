import os
from threading import Thread

from bokeh.embed import server_document
from bokeh.server.server import Server
from flask import Flask, render_template, request
from tornado.ioloop import IOLoop

from .models import Disease, Report
from dashboard.runner import bkapp


# def bk_worker():
#     server = Server({'/dashboard2': bkapp}, io_loop=IOLoop(),
#                     allow_websocket_origin=["localhost:5000", "127.0.0.1:5000"])
#     server.start()
#     server.io_loop.start()
#
#
# Thread(target=bk_worker).start()


def init_app(app: Flask):
    @app.route('/index')
    @app.route('/')
    def dashboard():
        # script = server_document('http://localhost:5006/dashboard')
        script = "Hello World"
        return render_template('index.html', script=script)

    @app.route('/show_disease')
    def give_me():
        d = request.args.get('d')
        return "1"

    @app.route('/d/<string:disease>/')
    def disease_by_name(disease):
        disease_dict = Disease.get_disease_dict()
        id_ = disease_dict[disease.lower()]
        return disease_by_id(id_)
        # df = Report.get_reports_df(id_).tail(20)
        # styled = df.style.render()
        # return render_template('raw_data.html', df=styled)

    @app.route('/id/<disease>/')
    def disease_by_id(disease):
        df = Report.get_reports_df(disease).tail(20)
        if df.empty:
            return 404
        df = (df
                  .assign(date=lambda x: x.date.dt.date)
                  .loc[:, ['date', 'total']])

        styled = df.style.render(index=False)
        return render_template('raw_data.html', df=styled)

    @app.route('/draw/<string:disease>/')
    def draw_by_id(disease):
        df = Report.get_reports_df(disease).tail(20)
        df = (df
                  .assign(date=lambda x: x.date.dt.date)
                  .loc[:, ['date', 'total']])
        return render_template('raw_data.html', df=df)

    @app.route('/demo')
    def demo_chart():
        return render_template('demo.html', chart_link='https://demo.bokehplots.com/apps/crossfilter')

    @app.errorhandler(404)
    def not_found(error):
        return "Sorry This is a custom 404 <br> {}".format(error), 404
