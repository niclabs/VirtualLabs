import os

path = os.path.dirname(os.path.realpath(__file__))

from kvm_models import connection as conn
from lab.lab_db_controller import LabDBController


connection = conn.Connection()
laboratory_loader = LabDBController()


def list_available_labs():
    return laboratory_loader.list_labs_names()
