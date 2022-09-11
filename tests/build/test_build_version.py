def test_build_version(docker_client, images, version) -> None:
    assert images.uvicorn_gunicorn_poetry_image.endswith(version)
    assert images.fast_api_multistage_production_image.endswith(version)
    assert images.fast_api_multistage_production_image_json_logging.endswith(version)
    assert images.fast_api_multistage_development_image.endswith(version)
    assert images.fast_api_singlestage_image.endswith(version)
