from tests.utils import (
    ImageTagComponents,
    create_version_tag_for_example_images,
)


def test_fast_api_multistage_build_versions(
    fast_api_multistage_image,
    fast_api_multistage_with_json_logging_image,
    version,
) -> None:
    production_image_components: ImageTagComponents = (
        ImageTagComponents.create_from_tag(fast_api_multistage_image)
    )
    production_image_version_tag = create_version_tag_for_example_images(
        version, "production-image"
    )
    assert production_image_components.version == production_image_version_tag

    production_image_json_logging_components: ImageTagComponents = (
        ImageTagComponents.create_from_tag(
            fast_api_multistage_with_json_logging_image
        )
    )
    production_image_json_logging_version_tag = (
        create_version_tag_for_example_images(
            version, "production-image-with-json-logging"
        )
    )
    assert (
        production_image_json_logging_components.version
        == production_image_json_logging_version_tag
    )
