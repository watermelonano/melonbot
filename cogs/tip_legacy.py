from discord.ext import commands
from discord.ext.commands import Bot, Context
from util.discord.channel import ChannelUtil
from util.discord.messages import Messages
from db.models.user import User
import config

class TipLegacyCog(commands.Cog):
    """Just show information about the new tip command for WATERMELONANO bot"""
    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx: Context):
        ctx.error = False
        msg = ctx.message
        if ChannelUtil.is_private(msg.channel):
            ctx.error = True
            return
        # See if user exists in DB
        user = await User.get_user(msg.author)
        if user is None:
            ctx.error = True
            await Messages.send_error_dm(msg.author, f"You should create an account with me first, send me `{config.Config.instance().command_prefix}help` to get started.")
            return

    @commands.command(aliases=['t', 'rain', 'tipsplit', 'tipfavorites', 'tiprandom'])
    async def tip(self, ctx: Context):
        if ctx.error:
            return
        msg = ctx.message

        await Messages.send_error_dm(
            member=msg.author,
            message=f"**WARNING** Tip units are in whole WATERMELONANO!"
        )
