from tests.utils import ImageTagComponents


def test_build_version(
    base_image_reference: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> None:
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
    components: ImageTagComponents = ImageTagComponents.create_from_reference(
        fast_api_multistage_with_json_logging_image_reference
    )
    assert components.version == image_version
    assert components.python_version == python_version
    assert components.os_variant == os_variant
