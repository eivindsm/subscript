"""Test that casegen_upcars is installed and launched with given demo cases"""
import subprocess
import shutil
from pathlib import Path

import pandas as pd

import opm.io

import pytest

from subscript.casegen_upcars import casegen_upcars

TESTDATA = "testdata_casegen_upcars"
DATADIR = Path(__file__).absolute().parent / TESTDATA


@pytest.mark.integration
def test_installed():
    """Test that the endpoint is installed, use -h as it required one parameter"""
    assert subprocess.check_output(["casegen_upcars", "-h"])


def test_demo_small_scale(tmpdir, mocker):
    """Test casegen_upcars on demo_small_scale.yaml"""
    tmpdir.chdir()
    shutil.copytree(DATADIR, TESTDATA)
    tmpdir.join(TESTDATA).chdir()

    base_name = "TEST_SMALL"
    mocker.patch(
        "sys.argv",
        [
            "casegen_upcars",
            "demo_small_scale.yaml",
            "--et",
            "dump_value.tmpl",
            "--base",
            base_name,
        ],
    )
    casegen_upcars.main()

    # check that all output files are generated
    for pre, suf in zip(
        ["", "fipnum_", "gridinc_", "satnum_", "swat_"],
        [".DATA", ".INC", ".GRDECL", ".INC", ".INC"],
    ):
        assert Path(pre + base_name + suf).exists()
        if suf != ".DATA":
            assert opm.io.Parser().parse(pre + base_name + suf)

    # check some key parameters in output file
    data_frame = pd.read_csv(base_name + ".DATA", index_col=0)
    assert data_frame.Values["nx"] == 53
    assert data_frame.Values["ny"] == 53
    assert data_frame.Values["nz"] == 50
    assert data_frame.Values["lx"] == 4.15
    assert data_frame.Values["ly"] == 4.15
    assert data_frame.Values["lz"] == 1.03
    assert data_frame.Values["poro"] == 0.0912


def test_demo_small_scale_with_vugs(tmpdir, mocker):
    """Test casegen_upcars on demo_small_scale.yaml with random vugs"""
    tmpdir.chdir()
    shutil.copytree(DATADIR, TESTDATA)
    tmpdir.join(TESTDATA).chdir()

    base_name = "TEST_SMALL_WITH_VUGS"
    mocker.patch(
        "sys.argv",
        [
            "casegen_upcars",
            "demo_small_scale.yaml",
            "--et",
            "dump_value.tmpl",
            "--vug2Volume",
            "0.1",
            "0.1",
            "--base",
            base_name,
        ],
    )
    casegen_upcars.main()

    # check that all output files are generated
    for pre, suf in zip(
        ["", "fipnum_", "gridinc_", "satnum_", "swat_"],
        [".DATA", ".INC", ".GRDECL", ".INC", ".INC"],
    ):
        assert Path(pre + base_name + suf).exists()
        if suf != ".DATA":
            assert opm.io.Parser().parse(pre + base_name + suf)

    # check some key parameters in output file
    data_frame = pd.read_csv(base_name + ".DATA", index_col=0)
    assert data_frame.Values["nx"] == 53
    assert data_frame.Values["ny"] == 53
    assert data_frame.Values["nz"] == 50
    assert data_frame.Values["lx"] == 4.15
    assert data_frame.Values["ly"] == 4.15
    assert data_frame.Values["lz"] == 1.03
    assert data_frame.Values["poro"] == 0.1732


def test_demo_large_scale(tmpdir, mocker):
    """Test casegen_upcars on demo_large_scale.yaml"""
    tmpdir.chdir()
    shutil.copytree(DATADIR, TESTDATA)
    tmpdir.join(TESTDATA).chdir()

    base_name = "TEST_LARGE"
    mocker.patch(
        "sys.argv",
        [
            "casegen_upcars",
            "demo_large_scale.yaml",
            "--et",
            "dump_value.tmpl",
            "--base",
            base_name,
        ],
    )
    casegen_upcars.main()

    # check that all output files are generated
    for pre, suf in zip(
        ["", "fipnum_", "gridinc_", "satnum_", "swat_"],
        [".DATA", ".INC", ".GRDECL", ".INC", ".INC"],
    ):
        assert Path(pre + base_name + suf).exists()
        if suf != ".DATA":
            assert opm.io.Parser().parse(str(pre + base_name + suf))

    # check some key parameters in output file
    data_frame = pd.read_csv(base_name + ".DATA", index_col=0)
    assert data_frame.Values["nx"] == 77
    assert data_frame.Values["ny"] == 72
    assert data_frame.Values["nz"] == 27
    assert data_frame.Values["lx"] == 7700.0
    assert data_frame.Values["ly"] == 7200.0
    assert data_frame.Values["lz"] == 355.0
    assert data_frame.Values["poro"] == 0.1711


def test_demo_large_scale_with_coordinate_transformation(tmpdir, mocker):
    """Test casegen_upcars on demo_large_scale.yaml with coordinate transformation"""
    tmpdir.chdir()
    shutil.copytree(DATADIR, TESTDATA)
    tmpdir.join(TESTDATA).chdir()

    base_name = "TEST_LARGE_WITH_TRANFORMATION"
    mocker.patch(
        "sys.argv",
        [
            "casegen_upcars",
            "demo_large_scale.yaml",
            "--et",
            "dump_value.tmpl",
            "--originX",
            "1000.0",
            "--originY",
            "2000.0",
            "--rotation",
            "15",
            "--base",
            base_name,
        ],
    )
    casegen_upcars.main()

    # check that all output files are generated
    for pre, suf in zip(
        ["", "fipnum_", "gridinc_", "satnum_", "swat_"],
        [".DATA", ".INC", ".GRDECL", ".INC", ".INC"],
    ):
        assert Path(pre + base_name + suf).exists()
        if suf != ".DATA":
            assert opm.io.Parser().parse(str(pre + base_name + suf))

    # check some key parameters in output file
    data_frame = pd.read_csv(base_name + ".DATA", index_col=0)
    assert data_frame.Values["nx"] == 77
    assert data_frame.Values["ny"] == 72
    assert data_frame.Values["nz"] == 27
    assert data_frame.Values["lx"] == 7700.0
    assert data_frame.Values["ly"] == 7200.0
    assert data_frame.Values["lz"] == 355.0
    assert data_frame.Values["poro"] == 0.1711
    assert data_frame.Values["originX"] == 1000.0
    assert data_frame.Values["originY"] == 2000.0
    assert data_frame.Values["rotation"] == 15.0
