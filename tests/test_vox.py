"""Vox tests"""

import builtins
import stat
import os
from xontrib.voxapi import Vox

from tools import skip_if_on_conda


@skip_if_on_conda
def test_crud(xonsh_builtins, tmpdir):
    """
    Creates a virtual environment, gets it, enumerates it, and then deletes it.
    """
    xonsh_builtins.__xonsh_env__['VIRTUALENV_HOME'] = str(tmpdir)
    vox = Vox()
    vox.create('spam')
    assert stat.S_ISDIR(tmpdir.join('spam').stat().mode)

    env, bin = vox['spam']
    assert env == str(tmpdir.join('spam'))
    assert os.path.isdir(bin)

    assert 'spam' in vox

    del vox['spam']

    assert not tmpdir.join('spam').check()


@skip_if_on_conda
def test_activate(xonsh_builtins, tmpdir):
    """
    Creates a virtual environment, gets it, enumerates it, and then deletes it.
    """
    xonsh_builtins.__xonsh_env__['VIRTUALENV_HOME'] = str(tmpdir)
    # I consider the case that the user doesn't have a PATH set to be unreasonable
    xonsh_builtins.__xonsh_env__.setdefault('PATH', [])
    vox = Vox()
    vox.create('spam')
    vox.activate('spam')
    assert xonsh_builtins.__xonsh_env__['VIRTUAL_ENV'] == vox['spam'].env
    vox.deactivate()
    assert 'VIRTUAL_ENV' not in xonsh_builtins.__xonsh_env__


@skip_if_on_conda
def test_path(xonsh_builtins, tmpdir):
    """
    Test to make sure Vox properly activates and deactivates by examining $PATH
    """
    xonsh_builtins.__xonsh_env__['VIRTUALENV_HOME'] = str(tmpdir)
    # I consider the case that the user doesn't have a PATH set to be unreasonable
    xonsh_builtins.__xonsh_env__.setdefault('PATH', [])

    oldpath = list(xonsh_builtins.__xonsh_env__['PATH'])
    vox = Vox()
    vox.create('eggs')

    vox.activate('eggs')
    
    assert oldpath != xonsh_builtins.__xonsh_env__['PATH']
    
    vox.deactivate()
    
    assert oldpath == xonsh_builtins.__xonsh_env__['PATH']
