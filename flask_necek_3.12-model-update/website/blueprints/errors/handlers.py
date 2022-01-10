from flask import Blueprint, render_template

errors = Blueprint ('errors', __name__, url_prefix='/errors')

@errors.app_errorhandler(404)
def error_404(error):
    # add your render_template() function for an error 404 page
    return render_template(),404

@errors.app_errorhandler(403)
def error_403(error):
    # add your render_template() function for an error 403 page
    return render_template(),403

@errors.app_errorhandler(500)
def error_500(error):
    # add your render_template() function for an error 500 page
    return render_template(),500