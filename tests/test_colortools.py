#!/usr/bin/env python

"""Tests for `webtools` package."""

import pytest
import webanalyst.colortools as color

# define some colors
indigo = "#4b0082"
aquamarine = "#7FFFD4"
white = "#ffffff"
favorite_test_color = "#336699"

favorite_test_color_contrast_report = {
    "normal AA": "Pass",
    "normal AAA": "Fail",
    "large AA": "Pass",
    "large AAA": "Pass",
    "graphics UI components": "Pass",
}
all_pass_color_contrast_report = {
    "normal AA": "Pass",
    "normal AAA": "Pass",
    "large AA": "Pass",
    "large AAA": "Pass",
    "graphics UI components": "Pass",
}
all_fail_color_contrast_report = {
    "normal AA": "Fail",
    "normal AAA": "Fail",
    "large AA": "Fail",
    "large AAA": "Fail",
    "graphics UI components": "Fail",
}

@pytest.fixture
def indigo_rgb():
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
    expected = 1.22
    results = color.contrast_ratio(aquamarine, white)
    assert expected == results

def test_passes_conlor_contrast_normal_aa_for_no_pass_aquamarine_white():
    expected = False
    results = color.passes_color_contrast("normal AA", aquamarine, white)
    assert results == expected

def test_passes_normal_aa_for_pass_indigo_white():
    expected = True
    results = color.passes_color_contrast("normal AA",indigo, white)
    assert results == expected

def test_passes_normal_aaa_for_no_pass_336699_white():
    expected = False
    results = color.passes_color_contrast("normal AAA",favorite_test_color, white)
    assert results == expected

def test_get_color_contrast_report_for_favorite_color():
    expected = favorite_test_color_contrast_report
    results = color.get_color_contrast_report(favorite_test_color, white)
    assert results == expected

def test_get_color_contrast_report_for_all_passing():
    expected = all_pass_color_contrast_report
    results = color.get_color_contrast_report(indigo, white)
    assert expected == results

def test_get_color_contrast_report_for_all_failing():
    expected = all_fail_color_contrast_report
    results = color.get_color_contrast_report(aquamarine, white)
    assert expected == results