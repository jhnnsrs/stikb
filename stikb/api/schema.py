from pydantic import Field, BaseModel
from enum import Enum
from typing_extensions import Literal
from typing import Tuple, Optional, List
from rath.scalars import ID
from stikb.funcs import execute, aexecute
from stikb.rath import StikbRath
from stikb.traits import WandbBearer


class EnsureIntegrationMutationEnsureintegration(BaseModel):
    typename: Optional[Literal["WandBIntegration"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID

    class Config:
        """A config class"""

        frozen = True


class EnsureIntegrationMutation(BaseModel):
    ensure_integration: EnsureIntegrationMutationEnsureintegration = Field(
        alias="ensureIntegration"
    )

    class Arguments(BaseModel):
        token: str

    class Meta:
        document = "mutation EnsureIntegration($token: String!) {\n  ensureIntegration(input: {token: $token}) {\n    id\n  }\n}"


class CreateProjectMutationCreateproject(WandbBearer, BaseModel):
    typename: Optional[Literal["Project"]] = Field(alias="__typename", exclude=True)
    id: str
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateProjectMutation(BaseModel):
    create_project: CreateProjectMutationCreateproject = Field(alias="createProject")

    class Arguments(BaseModel):
        name: str
        entity: str

    class Meta:
        document = "mutation CreateProject($name: String!, $entity: String!) {\n  createProject(input: {name: $name, entity: $entity}) {\n    id\n    name\n  }\n}"


class ProjectsQueryProjects(WandbBearer, BaseModel):
    typename: Optional[Literal["Project"]] = Field(alias="__typename", exclude=True)
    id: str
    name: str

    class Config:
        """A config class"""

        frozen = True


class ProjectsQuery(BaseModel):
    projects: Tuple[ProjectsQueryProjects, ...]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "query Projects {\n  projects {\n    id\n    name\n  }\n}"


async def aensure_integration(
    token: str, rath: Optional[StikbRath] = None
) -> EnsureIntegrationMutationEnsureintegration:
    """EnsureIntegration



    Arguments:
        token (str): token
        rath (stikb.rath.StikbRath, optional): The stikb rath client

    Returns:
        EnsureIntegrationMutationEnsureintegration"""
    return (
        await aexecute(EnsureIntegrationMutation, {"token": token}, rath=rath)
    ).ensure_integration


def ensure_integration(
    token: str, rath: Optional[StikbRath] = None
) -> EnsureIntegrationMutationEnsureintegration:
    """EnsureIntegration



    Arguments:
        token (str): token
        rath (stikb.rath.StikbRath, optional): The stikb rath client

    Returns:
        EnsureIntegrationMutationEnsureintegration"""
    return execute(
        EnsureIntegrationMutation, {"token": token}, rath=rath
    ).ensure_integration


async def acreate_project(
    name: str, entity: str, rath: Optional[StikbRath] = None
) -> CreateProjectMutationCreateproject:
    """CreateProject



    Arguments:
        name (str): name
        entity (str): entity
        rath (stikb.rath.StikbRath, optional): The stikb rath client

    Returns:
        CreateProjectMutationCreateproject"""
    return (
        await aexecute(
            CreateProjectMutation, {"name": name, "entity": entity}, rath=rath
        )
    ).create_project


def create_project(
    name: str, entity: str, rath: Optional[StikbRath] = None
) -> CreateProjectMutationCreateproject:
    """CreateProject



    Arguments:
        name (str): name
        entity (str): entity
        rath (stikb.rath.StikbRath, optional): The stikb rath client

    Returns:
        CreateProjectMutationCreateproject"""
    return execute(
        CreateProjectMutation, {"name": name, "entity": entity}, rath=rath
    ).create_project


async def aprojects(rath: Optional[StikbRath] = None) -> List[ProjectsQueryProjects]:
    """Projects



    Arguments:
        rath (stikb.rath.StikbRath, optional): The stikb rath client

    Returns:
        List[ProjectsQueryProjects]"""
    return (await aexecute(ProjectsQuery, {}, rath=rath)).projects


def projects(rath: Optional[StikbRath] = None) -> List[ProjectsQueryProjects]:
    """Projects



    Arguments:
        rath (stikb.rath.StikbRath, optional): The stikb rath client

    Returns:
        List[ProjectsQueryProjects]"""
    return execute(ProjectsQuery, {}, rath=rath).projects
