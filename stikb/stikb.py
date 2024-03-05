"""The Stikb (Client) Composition packages"""

from koil.composition import Composition
from .rath import StikbRath


class Stikb(Composition):
    """The Stikb (Client) Composition

    This composition is the main entry point for the stikb client.
    and is used to build a client for a stikb instance, that can be
    used to execute graphql operations and retrieve the dask client
    from a connected dask gateway trough the repository.

    """

    rath: StikbRath
