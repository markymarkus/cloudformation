import os
import logging
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

def main():
    xray_recorder.begin_segment('this')
    xray_recorder.begin_subsegment('that')

    input_var = os.environ['INPUTVAR']

    statusCode = 200
# magic number for testing Step Function error handling
    if int(input_var) > 100:
        raise ValueError

    ret = {
        "statusCode": statusCode,
        "headers": {"Content-Type": "application/json"},
        "body": {"hello": "hello"}
    }
    logger.info("RETURN: \r" + str(ret))
    
    xray_recorder.end_subsegment()
    xray_recorder.end_segment()

    return ret

if __name__ == "__main__":
    main()
