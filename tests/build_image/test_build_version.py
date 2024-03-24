"""Tests checking the build version."""

from tests.utils import ImageTagComponents


def test_build_version(
    base_image_reference: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> None:
    """Test for checking the build version of base image.

    :param base_image_reference:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    components: ImageTagComponents = ImageTagComponents.create_from_reference(
        base_image_reference
    )
    assert components.version == image_version
    assert components.python_version == python_version
    assert components.os_variant == os_variant


def test_example_app_singlestage_build_version(
    fast_api_singlestage_image_reference: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> None:
    """Test for checking the build version of single stage image.

    :param fast_api_singlestage_image_reference:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    components: ImageTagComponents = ImageTagComponents.create_from_reference(
        fast_api_singlestage_image_reference
    )
    assert components.version == image_version
    assert components.python_version == python_version
    assert components.os_variant == os_variant


def test_example_app_multistage__build_version(
    fast_api_multistage_image_reference: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> None:
    """Test for checking the build version of multi-stage image.

    :param fast_api_multistage_image_reference:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    components: ImageTagComponents = ImageTagComponents.create_from_reference(
        fast_api_multistage_image_reference
    )
    assert components.version == image_version
    assert components.python_version == python_version
    assert components.os_variant == os_variant


def test_example_app_with_json_logging_build_version(
    fast_api_multistage_with_json_logging_image_reference: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> None:
    """Test for checking the build version of multi-stage image with JSON logging.

    :param fast_api_multistage_with_json_logging_image_reference:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    components: ImageTagComponents = ImageTagComponents.create_from_reference(
        fast_api_multistage_with_json_logging_image_reference
    )
    assert components.version == image_version
    assert components.python_version == python_version
    assert components.os_variant == os_variant
