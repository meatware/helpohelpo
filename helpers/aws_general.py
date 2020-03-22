"""General Boto3 convenience module."""

import sys
import logging
import boto3
import botocore.exceptions
from botocore.client import ClientError


LOG = logging.getLogger(__name__)


def boto_session(region):
    """Initialise boto3 session."""

    session = boto3.Session(region_name=region)
    return session


def _add_ec2_tags(region, ec2_list):
    """Add schedule_deletion tag to ec2 instances."""

    ec2_client = boto3.client("ec2", region_name=region)

    if len(ec2_list) > 0:
        ec2_tag_status = {"ec2_tag_statuses": []}
        aws_sd_tag_val = helpo.calc_ndays_fwd(ndays=5)
        for ec2_instance in ec2_list:

            del_tag_status = try_except_status(
                partial(
                    ec2_client.create_tags,
                    Resources=[ec2_instance],
                    Tags=[{"Key": "schedule_deletion", "Value": aws_sd_tag_val}],
                ),
                "Error in del_tag_status: %s",
            )

            ec2_tag_status["ec2_tag_statuses"].append(
                {"ec2_instance": ec2_instance, "del_tag_status": del_tag_status}
            )

        return ec2_tag_status
    return {}


def search_ec2_instances(ec2_client, filter_data):
    """search aws region for ec2 instances to delete."""

    try:
        response = ec2_client.describe_instances(Filters=filter_data)
        return response
    except ClientError as err:
        LOG.warning("%s", str(err))

    return False


def terminate_instance(instance_id, region_name):
    """Terminates ec2 instance by id."""

    ec2 = boto3.resource("ec2", region_name=region_name)

    try:
        ec2.Instance(instance_id).terminate()
    except ClientError as err:
        LOG.warning("%s", str(err))
        if err.response["Error"]["Code"] == "OperationNotPermitted":
            return "<!here|here> Warning! Modify termination protection: " + instance_id
        else:
            return "Uncaught error occured on termination: " + instance_id

    return "Successfully terminated"


def shutdown_instance(instance_id, region_name):
    """Shutdown ec2 instance by id."""

    bo3_int = boto3.Session(region_name=region_name)
    ec2 = bo3_int.resource("ec2", region_name=region_name)

    try:
        ec2.Instance(instance_id).stop()
    except ClientError as err:
        LOG.warning("Shutdown Error: %s", str(err))
        return "Uncaught error occured on shut down: " + instance_id

    return "Successfully shutdown"


def check_bucket_exists(bucket_name):
    """Sanity check whether s3 bucket exists."""

    s3_client = boto3.resource("s3")

    try:
        s3_client.meta.client.head_bucket(Bucket=bucket_name)
    except ClientError:
        LOG.critical("s3 bucket %s does not exist or access denied", bucket_name)
        sys.exit(0)


def upload_logs_s3(bucket_name, log_name):
    """Upload log data to s3 bucket."""

    data = open(log_name, "rb")
    s3_client = boto3.resource("s3")
    try:
        s3_client.Bucket(bucket_name).put_object(Key=log_name, Body=data)

        LOG.info("Uploading log file %s to s3 %s", log_name, bucket_name)

    except Exception as err:
        LOG.warning("Failed to Upload log file %s to s3 %s", log_name, bucket_name)
        LOG.critical("error: %s", err)

    return True


def tagapi_search_tags(client, token):

    try:
        response = client.get_resources(
            PaginationToken=token,
            TagFilters=[{"Key": "schedule_deletion"}],
            ResourcesPerPage=50,
            ResourceTypeFilters=["elasticloadbalancing:loadbalancer",],
        )
        return response
    except ClientError as err:
        LOG.warning("%s", str(err))


def convert_http_status(status):
    """Converts HTTP 200 to OK or dispays error message
    from def try_except_status.
    """

    if status == 200:
        return ": *OK*"

    return ": *FAIL - " + status + "*"


def try_except_status(bo3_client_method, fail_str):
    """Takes a partially applied fuction passed to it
    so that it catches status codes/errors in a generalised way
    """

    try:
        get_status = bo3_client_method
        status = get_status()["ResponseMetadata"]["HTTPStatusCode"]
    except ClientError as err:
        LOG.warning(fail_str, str(err))
        if err.response["Error"]["Code"]:
            status = err.response["Error"]["Code"]
        else:
            status = str(err)
    return status
