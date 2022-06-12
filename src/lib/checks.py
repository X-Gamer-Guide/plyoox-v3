from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from lib.enums import PlyooxModule
from lib.errors import ModuleDisabled, OwnerOnly
from translation import _

if TYPE_CHECKING:
    from main import Plyoox
    from cache import CacheManager


def owner_only_check(interaction: discord.Interaction) -> None:
    """Raise an error if the user is not the owner of the bot."""
    bot: Plyoox = interaction.client  # type: ignore

    if interaction.user.id != bot.owner_id:
        raise OwnerOnly

    return True


async def module_enabled_check(interaction: discord.Interaction, module: PlyooxModule) -> None:
    """Raise an error if the module is not enabled."""
    manager: CacheManager = interaction.client.cache  # type: ignore
    guild = interaction.guild
    lc = interaction.locale
    cache = None

    if module == PlyooxModule.Leveling:
        cache = await manager.get_leveling(guild.id)

    if not cache or not cache.active:
        raise ModuleDisabled(_(lc, "errors.module_disabled", module=str(module.name)))

    return True


def module_active(module: PlyooxModule):
    return discord.app_commands.check(lambda i: module_enabled_check(i, module))


def owner_only():
    return discord.app_commands.check(owner_only_check)
