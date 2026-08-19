from __future__ import annotations

import typing as t

from ton_core import (
    Address,
    BagID,
    Binary,
    ContractVersion,
    PublicKey,
    StorageData,
    StorageProvider,
)

from tonutils.contracts.base import BaseContract
from tonutils.contracts.storage.methods import (
    GetAvailableBalanceGetMethod,
    GetProviderInfoGetMethod,
    GetProvidersGetMethod,
    GetStorageInfoGetMethod,
)


class StorageContract(
    BaseContract[StorageData],
    GetStorageInfoGetMethod,
    GetProvidersGetMethod,
    GetProviderInfoGetMethod,
    GetAvailableBalanceGetMethod,
):
    """TON Storage contract holding a single bag."""

    _data_model = StorageData
    VERSION = ContractVersion.StorageContract

    @property
    def torrent_hash(self) -> BagID:
        """Bag identifier stored by this contract."""
        return self.state_data.torrent_hash

    @property
    def owner_address(self) -> Address:
        """Address that pays for the storage."""
        return t.cast("Address", self.state_data.owner_address)

    @property
    def file_size(self) -> int:
        """Bag size in bytes."""
        return self.state_data.file_size

    @property
    def chunk_size(self) -> int:
        """Piece size in bytes."""
        return self.state_data.chunk_size

    @property
    def merkle_hash(self) -> Binary:
        """Root hash of the bag merkle tree."""
        return self.state_data.merkle_hash

    @property
    def providers(self) -> dict[PublicKey, StorageProvider]:
        """Active providers keyed by public key."""
        return t.cast("dict[PublicKey, StorageProvider]", self.state_data.providers)

    @property
    def key_len(self) -> int:
        """Merkle proof depth, 0 until the first provider is hired."""
        return self.state_data.key_len
