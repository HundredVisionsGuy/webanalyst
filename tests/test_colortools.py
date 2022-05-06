#!/usr/bin/env python

"""Tests for `webtools` package."""

import pytest
from webanalyst import colortools as color

# define some colors
indigo = "#4b0082"
aquamarine = "#7FFFD4"
white = "#ffffff"
favorite_test_color = "#336699"
hsl_string_1 = "hsl(355, 96%, 46%)"
hsl_string_1_as_rgb_str = "rgb(230, 5, 23)"
hsl_string_1_as_rgb = (230, 5, 23)
hsl_string_1_as_hex = "#E60517"
hsla_string_1 = "hsla(355, 96%, 46%, 1.0)"
hsla_string_1_as_rgba = "rgba(230, 5, 23, 1.0)"

favorite_test_color_contrast_report = {
    "Normal AA": "Pass",
    "Normal AAA": "Fail",
    "Large AA": "Pass",
    "Large AAA": "Pass",
    "Graphics UI components": "Pass",
}
all_pass_color_contrast_report = {
    "Normal AA": "Pass",
    "Normal AAA": "Pass",
    "Large AA": "Pass",
    "Large AAA": "Pass",
    "Graphics UI components": "Pass",
}
all_fail_color_contrast_report = {
    "Normal AA": "Fail",
    "Normal AAA": "Fail",
    "Large AA": "Fail",
    "Large AAA": "Fail",
    "Graphics UI components": "Fail",
}


@pytest.fixture
def indigo_rgb():
    indigo_rgb = color.hex_to_rgb(indigo)
    return indigo_rgb


def test_get_hsl_from_string():
    results = color.get_hsl_from_string(hsl_string_1)
    expected = (355, 96, 46)
    assert results == expected


def test_hsl_to_rgb():
    results = color.hsl_to_rgb((355, 96, 46))
    expected = hsl_string_1_as_rgb
    assert results == expected


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
    assert not color.is_hex("336699")


def test_is_hex_for_valid_hex():
    assert color.is_hex("#336699")


def test_is_hex_for_invalid_not_hex_digit():
    assert not color.is_hex("#3366lh")


def test_is_hex_for_alpha_channel():
    assert color.is_hex("#33aa0088")


def test_is_hex_for_3_codes():
    assert color.is_hex("#369")


def test_is_hex_for_invalid_number_digits():
    assert not color.is_hex("#4469")


def test_contrast_ratio_for_inverted_indigo_white(indigo_rgb):
    expected = 12.95
    results = color.contrast_ratio("#4B0082", "#ffffff")
    assert expected == results


def test_contrast_ratio_for_aquamarine_and_white():
    expected = 1.22
    results = color.contrast_ratio(aquamarine, white)
    assert expected == results


def test_passes_color_contrast_normal_aa_for_no_pass_aquamarine_white():
    expected = False
    results = color.passes_color_contrast("Normal AA", aquamarine, white)
    assert results == expected


def test_passes_normal_aa_for_pass_indigo_white():
    expected = True
    results = color.passes_color_contrast("Normal AA", indigo, white)
    assert results == expected


def test_passes_normal_aaa_for_no_pass_336699_white():
    expected = False
    results = color.passes_color_contrast("Normal AAA", favorite_test_color, white)
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


def test_has_alpha_channel_for_hex_code_with_alpha():
    expected = True
    results = color.has_alpha_channel("#33669966")
    assert expected == results


def test_has_alpha_channel_for_hex_code_without_alpha():
    expected = False
    results = color.has_alpha_channel("#336699")
    assert expected == results


def test_is_rgb_for_non_rgb():
    value = "hsla(0, 0, 0, 0)"
    results = color.is_rgb(value)
    expected = False
    assert results == expected


def test_is_rgb_for_rgb():
    value = "rgb(255, 0, 124)"
    results = color.is_rgb(value)
    expected = True
    assert results == expected


def test_is_rgb_for_rgba():
    value = "rgba(255, 0, 0, 0.2)"
    results = color.is_rgb(value)
    expected = True
    assert results == expected
