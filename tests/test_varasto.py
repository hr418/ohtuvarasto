import os
import sys

# Ensure src is on sys.path so tests can import varasto.py directly
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

import pytest

from varasto import Varasto


def test_init_negative_volume_sets_zero():
    v = Varasto(-5, 2)
    assert v.tilavuus == 0.0


def test_init_negative_starting_saldo_sets_zero():
    v = Varasto(10, -3)
    assert v.saldo == 0.0


def test_init_starting_saldo_exceeds_volume_sets_to_volume():
    v = Varasto(10, 20)
    assert v.saldo == 10


def test_paljonko_mahtuu_and_str():
    v = Varasto(10, 4)
    assert v.paljonko_mahtuu() == 6
    # string contains saldo and tilaa
    s = str(v)
    assert "saldo = 4" in s
    assert "vielä tilaa 6" in s


def test_lisaa_varastoon_negative_no_change():
    v = Varasto(10, 5)
    before = v.saldo
    # negative add should do nothing and function intentionally returns None for negative input
    assert v.lisaa_varastoon(-2) is None
    assert v.saldo == before


def test_lisaa_varastoon_fits_adds():
    v = Varasto(10, 2)
    v.lisaa_varastoon(3)
    assert v.saldo == 5


def test_lisaa_varastoon_more_than_capacity_sets_full():
    v = Varasto(10, 2)
    v.lisaa_varastoon(20)
    assert v.saldo == 10


def test_ota_varastosta_negative_returns_zero_and_no_change():
    v = Varasto(10, 5)
    before = v.saldo
    ret = v.ota_varastosta(-1)
    assert ret == 0.0
    assert v.saldo == before


def test_ota_varastosta_more_than_saldo_returns_all_and_sets_zero():
    v = Varasto(10, 5)
    ret = v.ota_varastosta(20)
    assert ret == 5
    assert v.saldo == 0.0


def test_ota_varastosta_less_reduces_and_returns_maara():
    v = Varasto(10, 5)
    ret = v.ota_varastosta(3)
    assert ret == 3
    assert v.saldo == 2
