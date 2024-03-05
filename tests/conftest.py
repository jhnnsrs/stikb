import pytest
from stikb.deployed import DeployedStikb, deployed
from typing import Iterator
from koil import unkoil
import logging
import os
from stikb.api.schema import ensure_integration
API_TOKEN = os.environ["API_TOKEN"]


@pytest.fixture(scope="session")
def deployed_app() -> Iterator[DeployedStikb]:
    """A deployed stikb"""
    app = deployed()
    app.deployment.down_on_exit = True
    with app:
        
        logging.warning("Deploying app")
        app.deployment.down()
        app.deployment.up()

        logging.warning("Deployed app. Waiting for healthz")
        app.deployment.wait_for_healthz()
        logging.warning("Deployment is healthy")

        
        x = ensure_integration(token=API_TOKEN)

        yield app

        logging.warning("Tearing down Deployment")
