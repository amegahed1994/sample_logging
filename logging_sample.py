def log_error(error_msg):
    def query_metadata(endpoint_suffix):
        import requests

        return requests.get(
            "http://metadata/computeMetadata/v1/{}".format(endpoint_suffix),
            headers={"Metadata-Flavor": "Google"},
        ).text

    from google.cloud import logging

    resource = logging.Resource(
        type="gce_instance",
        labels={
            "project_id": query_metadata("project/project-id"),
            "instance_id": query_metadata("instance/id"),
            "zone": query_metadata("instance/zone").split("/")[3],
        },
    )

    logger = logging.Client().logger("telephonie-etl-programmes")

    logger.log_struct(
        {"message": error_msg, "tag": ERROR_TAG},
        resource=resource,
        severity="ERROR",
    )


log_error("test1")
log_error("test2")
