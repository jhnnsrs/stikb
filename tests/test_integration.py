import pytest
from stikb.api.schema import create_project


@pytest.mark.integration
def test_create_project(deployed_app):
    x = create_project(name="mikro", entity="jku-anatomy")
    assert x.name, "Was not able to create a cluster"
