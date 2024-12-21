import asyncio
from src.binance_service import BinanceService
import pytest

def env_update(env:bool):
    env = "Prod" if env else "Test"
    return env

@pytest.fixture()
def test_evn():
    return "Test"

@pytest.fixture()
def prod_env():
    return "Prod"



@pytest.fixture(scope="function")  # Use scope="module" to apply the fixture to all tests in the module and ixture to function, which ensures it's applied to each test function individually.
def mock_create_client_async(mocker):
    # Mock the _create_client_async method for all tests
    mock_async_client = "mocked_async_client"
    mocker.patch.object(BinanceService, '_create_client_async', return_value=mock_async_client)
    return mock_async_client
# Test Scenario 1: Test that a new instance of BinanceService is created when no instance exists for the given account_id and production_environment combination.
@pytest.mark.asyncio
async def test_create_new_instance_when_none_exists(mock_create_client_async):

    account_id = "test_account_1"
    production_environment =False
    env = env_update(production_environment)
    instance = await BinanceService.create_async(account_id, production_environment)
    assert instance is not None
    assert (account_id, env) in BinanceService._instances

# Test Scenario 2: Test creating instances with different account IDs to ensure unique instances are created for each account ID and production environment combination.
@pytest.mark.asyncio
async def test_create_instances_with_different_account_ids(mock_create_client_async):
    account_id_1 = "test_account_1"
    account_id_2 = "test_account_2"
    production_environment = False
    env = env_update(production_environment)
    instance_1 = await BinanceService.create_async(account_id_1, production_environment)
    instance_2 = await BinanceService.create_async(account_id_2, production_environment)
    assert instance_1 is not instance_2
    assert (account_id_1, env) in BinanceService._instances
    assert (account_id_2, env) in BinanceService._instances

# Test Scenario 3: Test creating instances with the same account_id but different production_environment values to ensure separate instances are created and stored in the _instances dictionary.
@pytest.mark.asyncio
async def test_create_instances_with_same_account_id_different_env(mock_create_client_async):
    account_id = "test_account_1"

    test_env = env_update(False)
    prod_env = env_update(True)

    instance_1 = await BinanceService.create_async(account_id, False)
    instance_2 = await BinanceService.create_async(account_id, True)
    assert instance_1 is not instance_2
    assert (account_id, test_env) in BinanceService._instances
    assert (account_id, prod_env) in BinanceService._instances

# Test Scenario 4: Test that calling create_async with the same account_id and production_environment returns the same instance.
@pytest.mark.asyncio
async def test_create_async_returns_same_instance(mock_create_client_async):
    account_id = "test_account_1"
    production_environment = False

    instance_1 = await BinanceService.create_async(account_id, production_environment)
    instance_2 = await BinanceService.create_async(account_id, production_environment)
    assert instance_1 is instance_2

# Test Scenario 5: Test if the method handles exceptions when creating an async client fails.
# @pytest.mark.asyncio
# async def test_create_async_handles_exceptions(mocker):
#     # mocker.patch('asyncio.sleep', side_effect=Exception("Async client creation failed"))
#     account_id = "test_account_1"
#     production_environment = False
#     with pytest.raises(Exception, match="Async client creation failed"):
#         await BinanceService.create_async(account_id, production_environment)

# Test Scenario 6: Test that a new instance of BinanceService is created and stored in _instances when no instance exists for the given key.
@pytest.mark.asyncio
async def test_create_new_instance_stored_in_instances(mock_create_client_async):
    account_id = "test_account_3"
    production_environment = True
    env = env_update(production_environment)
    instance = await BinanceService.create_async(account_id, production_environment)
    assert instance is not None
    assert (account_id, env) in BinanceService._instances

# # Test Scenario 7: Test the performance of creating multiple instances of BinanceService asynchronously to ensure the method handles concurrent requests efficiently without significant delays or resource bottlenecks.
# @pytest.mark.asyncio
# async def test_performance_of_creating_multiple_instances():
#     account_ids = [f"test_account_{i}" for i in range(10)]
#     production_environment = False
#     tasks = [BinanceService.create_async(account_id, production_environment) for account_id in account_ids]
#     instances = await asyncio.gather(*tasks)
#     assert len(instances) == len(account_ids)
#     for account_id in account_ids:
#         assert (account_id, production_environment) in BinanceService._instances

# Test Scenario 8: Validate that the method handles invalid account_id inputs gracefully, ensuring no instance is created and appropriate exceptions are raised.
@pytest.mark.asyncio
async def test_create_async_with_invalid_account_id():
    invalid_account_id = None  # or any invalid type like an integer
    production_environment = False
    with pytest.raises(ValueError):
        await BinanceService.create_async(invalid_account_id, production_environment)

@pytest.mark.asyncio
async def test_create_async_with_invalid_environment():
    account_id = "test_account_1"
    invalid_environment = None  # or any invalid type like an integer
    production_environment = False
    with pytest.raises(TypeError):
        await BinanceService.create_async(account_id, invalid_environment)