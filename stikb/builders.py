""" Arkitekt Stikb Builder"""

from arkitekt.healthz import FaktsHealthz
from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
from rath.links.split import SplitLink
from rath.contrib.fakts.links.graphql_ws import FaktsGraphQLWSLink
from rath.contrib.herre.links.auth import HerreAuthLink
from stikb.rath import StikbRathLinkComposition, StikbRath
from stikb.stikb import Stikb
from graphql import OperationType
from herre import Herre
from fakts import Fakts
from stikb.contrib.arkitekt_repository import ArkitektRepository


class ArkitektStikb(Stikb):
    """A composition of Stikb as it
    relates to the Arkitekt project"""

    rath: StikbRath
    repo: ArkitektRepository
    healthz: FaktsHealthz


def build_arkitekt_stikb(
    fakts: Fakts, herre: Herre, fakts_group: str = "stikb"
) -> StikbRath:
    """Builds a StikbRath for use with the Arkitekt project"""
    repo = ArkitektRepository(
        fakts=fakts,
        herre=herre,
        fakts_key="stikb.gateway_url",
    )

    rath = StikbRath(
        link=StikbRathLinkComposition(
            auth=HerreAuthLink(herre=herre),
            split=SplitLink(
                left=FaktsAIOHttpLink(fakts_group=fakts_group, fakts=fakts),
                right=FaktsGraphQLWSLink(fakts_group=fakts_group, fakts=fakts),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        )
    )

    return ArkitektStikb(
        rath=rath,
        repo=repo,
        healthz=FaktsHealthz(fakts_group=fakts_group, fakts=fakts),
    )
