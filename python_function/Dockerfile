# As mentioned in AWS docs
FROM public.ecr.aws/lambda/python:3.10

# Copy and install requirements, needed environment variable set by AWS: LAMBDA_TASK_ROOT=/var/task
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]