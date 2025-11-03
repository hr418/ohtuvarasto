import unittest
import pytest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 1)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)


# --- pytest-style tests merged in ---


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
    # negative add should do nothing and returns None
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
