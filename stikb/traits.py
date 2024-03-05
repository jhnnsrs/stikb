"""
Traits for omero_ark


Traits are mixins that are added to every graphql type that exists on the mikro schema.
We use them to add functionality to the graphql types that extend from the base type.

Every GraphQL Model on Mikro gets a identifier and shrinking methods to ensure the compatibliity
with arkitekt. This is done by adding the identifier and the shrinking methods to the graphql type.
If you want to add your own traits to the graphql type, you can do so by adding them in the graphql
.config.yaml file.

"""

from pydantic import BaseModel
from typing import TYPE_CHECKING
from rath.turms.utils import get_attributes_or_error
from koil import unkoil
import webbrowser
from wandb.wandb_run import Run
import wandb

if TYPE_CHECKING:
    pass


class WandbBearer(BaseModel):
    """Client Bearer Trait

    Implements both identifier and shrinking methods.
    Also Implements the data attribute


    """

    async def ainit(self) -> Run:
        """Get the wandb client.

        This is a synchronous version of the aget_gateway method.

        Usage:
            >>> gateway = cluster.get_gateway()
            >>> gateway.get_client()

        Parameters
        ----------
        asynchronous : bool, optional
            Whether to create the gateway asynchronously, by default False


        Returns
        -------
        cluster: GatewayCluster
                The dask gateway for the representation.
        """

        id = get_attributes_or_error(self, "name")
        return wandb.init(project=id)

    def init(self) -> Run:
        """Get the dask client for the representation.

        This is a synchronous version of the aget_gateway method.

        Usage:
            >>> gateway = cluster.get_gateway()
            >>> gateway.get_client()


        Returns
        -------
        cluster: GatewayCluster
                The dask gateway for the representation.
        """

        return unkoil(self.ainit)
