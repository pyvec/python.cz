# This Dockerfile allows you to run python.cz website easily and without
# issues with dependencies - locally, on your server or in cloud like now.sh.
# That's handy for testing or for demonstration of new feature in a pull request.
#
# For running the website locally:
#
#     docker build -t python.cz .
#     docker run -p 8000:8000 python.cz
#
# ...and open in your browser: http://localhost:8000
#
# Environment variables can be specified too>
#
#     docker run -p 8000:8000 -e GITHUB_TOKEN=token123 python.cz

FROM python:3.7-alpine

RUN python3 -m venv /venv
RUN /venv/bin/pip install gunicorn pipenv
WORKDIR /app
COPY . ./
RUN /venv/bin/pipenv install

EXPOSE 8000

CMD [ \
  "/venv/bin/gunicorn", \
  "--bind", "0.0.0.0:8000", \
  "--workers", "4", \
  "pythoncz:app" \
]
