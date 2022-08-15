import pytest
from django.db import IntegrityError

from application.apps.user.exceptions import CPFAlreadyInUse
from application.apps.user.managers import UserManager


def test_shouldnt_create_user_due_integrity_error(mocker):
    mocked_model = mocker.MagicMock()
    mocked_model.return_value.save.side_effect = IntegrityError

    manager = UserManager()
    manager.model = mocked_model

    with pytest.raises(CPFAlreadyInUse):
        manager.create_user('acpf', 'apassword')


def test_create_user(mocker):
    mocked_model = mocker.MagicMock()
    mocked_save_model = mocker.MagicMock()
    mocked_model.return_value.save = mocked_save_model

    manager = UserManager()
    manager.model = mocked_model

    manager.create_user('acpf', 'apassword')

    mocked_save_model.assert_called_once()
