from __future__ import annotations

from ton_core import Address

from tests.constants import STORAGE_CONTRACT_ADDRESS
from tonutils.contracts.storage import (
    get_available_balance_get_method,
    get_provider_info_get_method,
    get_providers_get_method,
    get_storage_info_get_method,
)


class TestGetStorageInfo:
    async def test_structure(self, client):
        stack = await get_storage_info_get_method(client, STORAGE_CONTRACT_ADDRESS)
        assert len(stack) == 5
        torrent_hash, file_size, chunk_size, owner_address, merkle_hash = stack
        assert isinstance(torrent_hash, int)
        assert torrent_hash > 0
        assert isinstance(file_size, int)
        assert file_size > 0
        assert isinstance(chunk_size, int)
        assert chunk_size > 0
        assert isinstance(owner_address, Address)
        assert isinstance(merkle_hash, int)
        assert merkle_hash > 0

    async def test_chunk_fits_file(self, client):
        stack = await get_storage_info_get_method(client, STORAGE_CONTRACT_ADDRESS)
        assert stack[2] <= stack[1]


class TestGetAvailableBalance:
    async def test_returns_non_negative_int(self, client):
        result = await get_available_balance_get_method(client, STORAGE_CONTRACT_ADDRESS)
        assert isinstance(result, int)
        assert result >= 0


class TestGetProviders:
    async def test_structure(self, client):
        stack = await get_providers_get_method(client, STORAGE_CONTRACT_ADDRESS)
        assert len(stack) == 2
        providers, available_balance = stack
        assert isinstance(providers, list)
        assert isinstance(available_balance, int)
        assert available_balance >= 0

    async def test_provider_structure(self, client):
        providers, _ = await get_providers_get_method(client, STORAGE_CONTRACT_ADDRESS)
        assert len(providers) > 0
        for provider in providers:
            assert len(provider) == 6
            assert all(isinstance(value, int) for value in provider)
            key, rate_per_mb_day, payment_max_span, _, _, _ = provider
            assert key > 0
            assert rate_per_mb_day > 0
            assert payment_max_span > 0


class TestGetProviderInfo:
    async def test_structure(self, client):
        providers, _ = await get_providers_get_method(client, STORAGE_CONTRACT_ADDRESS)
        key = providers[0][0]
        stack = await get_provider_info_get_method(client, STORAGE_CONTRACT_ADDRESS, key.to_bytes(32, "big"))
        assert len(stack) == 6
        assert all(isinstance(value, int) for value in stack)

    async def test_matches_get_providers(self, client):
        providers, _ = await get_providers_get_method(client, STORAGE_CONTRACT_ADDRESS)
        key, rate_per_mb_day, payment_max_span, _, _, _ = providers[0]
        stack = await get_provider_info_get_method(client, STORAGE_CONTRACT_ADDRESS, key.to_bytes(32, "big"))
        assert stack[3] == payment_max_span
        assert stack[4] == rate_per_mb_day
