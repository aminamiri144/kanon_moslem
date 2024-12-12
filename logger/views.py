from logger.models import Logger


def log(log_type, text, decs):
    log = Logger()
    log.type = log_type
    log.text = text
    log.decs = decs
    log.save()
