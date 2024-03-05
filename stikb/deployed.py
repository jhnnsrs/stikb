"""A deployed stikb instance package"""

from dokker import mirror, Deployment
import os
from koil.composition import Composition
from rath.links.auth import ComposedAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from stikb.stikb import Stikb
from stikb.rath import (
    StikbRath,
    SplitLink,
    StikbRathLinkComposition,
)
from graphql import OperationType

test_path = os.path.join(os.path.dirname(__file__), "deployments", "test")


def build_deployment() -> Deployment:
    """Builds a deploymen of stikb for testing

    This will return a deployment of stikb that is ready to be used for testing.
    It will have a health check that will check the graphql endpoint.

    Returns
    -------
    Deployment
        The deployment of stikb (dokker.Deployment)


    """
    setup = mirror(test_path)
    setup.add_health_check(
        url="http://localhost:7766/graphql",
        service="stikb",
        timeout=5,
        max_retries=10,
    )
    return setup


async def token_loader() -> str:
    """Returns a token as defined in the static_token setting for stikb"""
    return "demo"


def build_deployed_stikb() -> Stikb:
    """Build a client for a  deployed stikb instance

    This will return a client for a deployed stikb instance. It will use the
    static_token setting for authentication.

    """

    y = StikbRath(
        link=StikbRathLinkComposition(
            auth=ComposedAuthLink(
                token_loader=token_loader,
                token_refresher=token_loader,
            ),
            split=SplitLink(
                left=AIOHttpLink(endpoint_url="http://localhost:7766/graphql"),
                right=GraphQLWSLink(ws_endpoint_url="ws://localhost:7766/graphql"),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        ),
    )

    omero_ark = Stikb(rath=y)
    return omero_ark


class DeployedStikb(Composition):
    """A deployed stikb instance

    THis is a composition of both a deployment of stikb-server
    (and stikb-gateway) and a client for that deployment. It is
    the fastest way to get a fully functioning stikb instance,
    ready for testing.


    """

    deployment: Deployment
    stikb: Stikb


def deployed() -> DeployedStikb:
    """Create a deployed stikb

    A deployed stikb is a composition of a deployment of the
    stikb server and a stikb client.
    This means a fully functioning stikb instance will be spun up when
    the context manager is entered.

    To inspect the deployment, use the `deployment` attribute.
    To interact with the stikb, use the `stikb` attribute.


    Returns
    -------
    DeployedStikb
        The deployed stikb instance (Composition)
    """
    return DeployedStikb(
        deployment=build_deployment(),
        stikb=build_deployed_stikb(),
    )
