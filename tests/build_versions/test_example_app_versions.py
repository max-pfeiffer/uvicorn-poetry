from tests.utils import (
    ImageTagComponents,
    create_version_tag_for_example_images,
)


def test_fast_api_multistage_build_versions(
    fast_api_multistage_production_image,
    fast_api_multistage_production_image_json_logging,
    fast_api_multistage_development_image,
    version,
) -> None:
    production_image_components: ImageTagComponents = (
        ImageTagComponents.create_from_tag(fast_api_multistage_production_image)
    )
    production_image_version_tag = create_version_tag_for_example_images(
        version, "production-image"
    )
    assert production_image_components.version == production_image_version_tag

    production_image_json_logging_components: ImageTagComponents = (
        ImageTagComponents.create_from_tag(
            fast_api_multistage_production_image_json_logging
        )
    )
    production_image_json_logging_version_tag = (
        create_version_tag_for_example_images(
            version, "production-image-json-logging"
        )
    )
    assert (
        production_image_json_logging_components.version
        == production_image_json_logging_version_tag
    )

    development_image_components: ImageTagComponents = (
        ImageTagComponents.create_from_tag(
            fast_api_multistage_development_image
        )
    )
    development_image_version_tag = create_version_tag_for_example_images(
        version, "development-image"
    )
    assert development_image_components.version == development_image_version_tag


def test_fast_api_singlestage_image_version(
    fast_api_singlestage_image, version
):
    development_image_components: ImageTagComponents = (
        ImageTagComponents.create_from_tag(fast_api_singlestage_image)
    )
    assert development_image_components.version == version
