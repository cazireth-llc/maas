# Copyright 2014 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Tests for the SUSEOS module."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )

str = None

__metaclass__ = type
__all__ = []

from itertools import product

from maastesting.factory import factory
from maastesting.testcase import MAASTestCase
from provisioningserver.drivers.osystem.suse import (
    BOOT_IMAGE_PURPOSE,
    DISTRO_SERIES_CHOICES,
    DISTRO_SERIES_DEFAULT,
    SUSEOS,
    )


class TestSUSEOS(MAASTestCase):

    def test_get_boot_image_purposes(self):
        osystem = SUSEOS()
        archs = [factory.make_name('arch') for _ in range(2)]
        subarchs = [factory.make_name('subarch') for _ in range(2)]
        releases = [factory.make_name('release') for _ in range(2)]
        labels = [factory.make_name('label') for _ in range(2)]
        for arch, subarch, release, label in product(
                archs, subarchs, releases, labels):
            expected = osystem.get_boot_image_purposes(
                arch, subarchs, release, label)
            self.assertIsInstance(expected, list)
            self.assertEqual(expected, [
                BOOT_IMAGE_PURPOSE.XINSTALL,
                ])

    def test_get_supported_releases(self):
        osystem = SUSEOS()
        expected = osystem.get_supported_releases()
        self.assertIsInstance(expected, list)
        self.assertItemsEqual(expected, list(DISTRO_SERIES_CHOICES.keys()))

    def test_get_default_release(self):
        osystem = SUSEOS()
        expected = osystem.get_default_release()
        self.assertEqual(expected, DISTRO_SERIES_DEFAULT)

    def test_format_release_choices(self):
        osystem = SUSEOS()
        releases = osystem.get_supported_releases()
        formatted = osystem.format_release_choices(releases)
        self.assertEqual(DISTRO_SERIES_CHOICES, dict(formatted))
