from __future__ import annotations

import typing as t

from ton_core import AddressLike, BinaryLike, PublicKey

from tonutils.clients.protocol import ClientProtocol
from tonutils.contracts.protocol import ContractProtocol


async def get_storage_info_get_method(
    client: ClientProtocol,
    address: AddressLike,
) -> list[t.Any]:
    """Call ``get_storage_info`` on a TON Storage contract.

    :param client: TON client.
    :param address: Storage contract address.
    :return: List of [torrent_hash, file_size, chunk_size, owner_address, merkle_hash].
    """
    return await client.run_get_method(
        address=address,
        method_name="get_storage_info",
    )


class GetStorageInfoGetMethod(ContractProtocol[t.Any]):
    """Mixin for the ``get_storage_info`` get-method."""

    async def get_storage_info(self) -> list[t.Any]:
        """Return bag parameters (hash, size, chunk size, owner, merkle root)."""
        return await get_storage_info_get_method(
            client=self.client,
            address=self.address,
        )


async def get_providers_get_method(
    client: ClientProtocol,
    address: AddressLike,
) -> list[t.Any]:
    """Call ``get_providers`` on a TON Storage contract.

    :param client: TON client.
    :param address: Storage contract address.
    :return: List of [providers, available_balance], where every provider is
        [key, rate_per_mb_day, payment_max_span, last_proof_time, next_proof_byte, nonce].
    """
    return await client.run_get_method(
        address=address,
        method_name="get_providers",
    )


class GetProvidersGetMethod(ContractProtocol[t.Any]):
    """Mixin for the ``get_providers`` get-method."""

    async def get_providers(self) -> list[t.Any]:
        """Return all active providers together with the available balance."""
        return await get_providers_get_method(
            client=self.client,
            address=self.address,
        )


async def get_provider_info_get_method(
    client: ClientProtocol,
    address: AddressLike,
    key: PublicKey | BinaryLike,
) -> list[t.Any]:
    """Call ``get_provider_info`` on a TON Storage contract.

    The contract throws exit code 404 if the provider is not hired.

    :param client: TON client.
    :param address: Storage contract address.
    :param key: Provider public key.
    :return: List of [nonce, last_proof_time, next_proof_byte, payment_max_span,
        rate_per_mb_day, available_balance].
    """
    public_key = key if isinstance(key, PublicKey) else PublicKey(key)
    return await client.run_get_method(
        address=address,
        method_name="get_provider_info",
        stack=[public_key.as_int],
    )


class GetProviderInfoGetMethod(ContractProtocol[t.Any]):
    """Mixin for the ``get_provider_info`` get-method."""

    async def get_provider_info(self, key: PublicKey | BinaryLike) -> list[t.Any]:
        """Return terms and proof state of a single provider.

        :param key: Provider public key.
        :return: List of provider terms and proof state values.
        """
        return await get_provider_info_get_method(
            client=self.client,
            address=self.address,
            key=key,
        )


async def get_available_balance_get_method(
    client: ClientProtocol,
    address: AddressLike,
) -> int:
    """Call ``get_available_balance`` on a TON Storage contract.

    :param client: TON client.
    :param address: Storage contract address.
    :return: Balance available for provider rewards in nanotons.
    """
    r = await client.run_get_method(
        address=address,
        method_name="get_available_balance",
    )
    return int(r[0])


class GetAvailableBalanceGetMethod(ContractProtocol[t.Any]):
    """Mixin for the ``get_available_balance`` get-method."""

    async def get_available_balance(self) -> int:
        """Return balance available for provider rewards in nanotons."""
        return await get_available_balance_get_method(
            client=self.client,
            address=self.address,
        )
