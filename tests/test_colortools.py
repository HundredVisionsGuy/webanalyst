#!/usr/bin/env python

"""Tests for `webtools` package."""

import pytest
import webanalyst.colortools as color


@pytest.fixture
def indigo_rgb():
    indigo = "#4b0082"
    indigo_rgb = color.hex_to_rgb(indigo)
    return indigo_rgb

def test_hex_to_decimal_for_bc():
    bc_hex = "bc"
    expected = 188
    results = color.hex_to_decimal(bc_hex)
    assert expected == results

def test_hex_to_decimal_for_CB():
    cb_hex = "CB"
    expected = 203
    results = color.hex_to_decimal(cb_hex)
    assert expected == results

def test_rgb_to_hex_for_black():
    results = color.rgb_to_hex(0, 0, 0)
    expected = "#000000"
    assert results == expected


def test_rgb_to_hex_for_white():
    results = color.rgb_to_hex(255, 255, 255)
    expected = "#ffffff"
    assert results == expected


def test_rgb_to_hex_for_336699():
    results = color.rgb_to_hex(51, 102, 153)
    expected = "#336699"
    assert results == expected


def test_rgb_to_hex_for_string_336699():
    results = color.rgb_to_hex("rgb(51,102,153)")
    expected = "#336699"
    assert results == expected

def test_is_hex_for_no_hash():
    assert color.is_hex("336699") == False

def test_is_hex_for_valid_hex():
    assert color.is_hex("#336699")

def test_is_hex_for_invalid_not_hex_digit():
    assert not color.is_hex("#3366lh")

def test_contrast_ratio_for_inverted_indigo_white(indigo_rgb):
    expected = 12.95
    results = color.contrast_ratio("#4B0082", "#ffffff")
    assert expected == results

def test_contrast_ratio_for_aquamarine_and_white():
    aquamarine = "#7FFFD4"
    white = "#ffffff"
    expected = 1.22
    results = color.contrast_ratio(aquamarine, white)
    assert expected == results