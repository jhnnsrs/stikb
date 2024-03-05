""" The Stikb Rath packages (GraphQL Client)"""

from pydantic import Field
from rath import rath
import contextvars
from rath.links.auth import AuthTokenLink
from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.file import FileExtraction
from rath.links.split import SplitLink
from typing import Optional, Type
import traceback

from stikb.errrors import NoStikbRathInContextError

current_stikb_rath: contextvars.ContextVar[
    Optional["StikbRath"]
] = contextvars.ContextVar("current_stikb_rath", default=None)


def get_current_stikb_rath() -> "StikbRath":
    """Get Current StikbRath

    Returns
    -------
    StikbRath
        The current StikbRath

    Raises
    ------
    NoStikbRathInContextError
        If there is no StikbRath in context
    """

    x = current_stikb_rath.get()

    if x is None:
        raise NoStikbRathInContextError("No StikbRath in context")

    return x


class StikbRathLinkComposition(TypedComposedLink):
    """OmeroArk Rath Link Composition

    This is a composition of links that are used by the OmeroArkRath. It is a subclass of
    TypedComposedLink that adds some default links to convert files and array to support
    the graphql multipart request spec."""

    fileextraction: FileExtraction = Field(default_factory=FileExtraction)
    dicting: DictingLink = Field(default_factory=DictingLink)
    auth: AuthTokenLink
    split: SplitLink


class StikbRath(rath.Rath):
    """OmeroAArk Rath

    Mikro Rath is the GraphQL client for omero_ark It is a thin wrapper around Rath
    that provides some default links and a context manager to set the current
    client. (This allows you to use the `mikro_nextrath.current` function to get the
    current client, within the context of mikro app).

    This is a subclass of Rath that adds some default links to convert files and array to support
    the graphql multipart request spec."""

    link: StikbRathLinkComposition

    async def __aenter__(self: "StikbRath") -> "StikbRath":
        """Enters the context manager and sets the current client to this client"""
        await super().__aenter__()
        current_stikb_rath.set(self)
        return self

    async def __aexit__(
        self,
        exc_type: Type[Exception],
        exc_val: str,
        exc_tb: traceback.TracebackException,
    ) -> None:
        """Exits the context manager and sets the current client to None"""
        await super().__aexit__(exc_type, exc_val, exc_tb)
        current_stikb_rath.set(None)
