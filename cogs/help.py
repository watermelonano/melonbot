from cogs import tips, account, stats, rain, admin, useroptions, favorites, giveaway
from discord.ext import commands
from discord.ext.commands import Bot, Context
from util.env import Env
from util.discord.messages import Messages
from util.discord.paginator import Paginator, Page, CannotPaginate, Entry
from version import __version__

import config
import logging

COMMANDS = {
    'ACCOUNT': {
        'header': 'Account Commands',
        'info': 'Accounts that help you manage your Graham account',
        'cmd_list': [
            account.REGISTER_INFO,
            account.BALANCE_INFO,
            account.SEND_INFO,
            account.SENDMAX_INFO
        ]
    },
    'TIP': {
        'header': 'Tipping Commands',
        'info': 'The different ways you are able to tip with this bot',
        'cmd_list': [
            tips.TIP_INFO,
            tips.TIPSPLIT_INFO,
            tips.TIPRANDOM_INFO,
            rain.RAIN_INFO,
            favorites.TIPFAVORITES_INFO
        ]
    },
    'GIVEAWAY': {
        'header': 'Giveaway Commands',
        'info': 'How to create and participate in giveaways',
        'cmd_list': [
            giveaway.START_GIVEAWAY_INFO,
            giveaway.TICKET_INFO,
            giveaway.TICKETSTATUS_INFO,
            giveaway.TIPGIVEAWAY_INFO,
            giveaway.GIVEAWAYSTATS_INFO
        ]
    },
    'STATS': {
        'header': 'Statistics Commands',
        'info': 'The different statistics related to tips within the bot.',
        'cmd_list': [
            stats.TIPSTATS_INFO,
            stats.TOPTIPS_INFO,
            stats.LEADERBOARD_INFO,
            stats.LEGACYBOARD_INFO,
            giveaway.WINNERS_INFO
        ]
    },
    'USER_OPTIONS': {
        'header': 'User Options Commands',
        'info': 'Various user-specific options.',
        'cmd_list': [
            useroptions.MUTE_INFO,
            useroptions.UNMUTE_INFO,
            favorites.ADD_FAVORITE_INFO,
            favorites.REMOVE_FAVORITE_INFO,
            favorites.FAVORITES_INFO
        ]
    },
}

ADMIN_COMMANDS = {
    'ADMIN': {
        'header': 'ADMIN Commands',
        'info': 'The different commands admin can use to manage the bot.',
        'cmd_list': [
            admin.PAUSE_INFO,
            admin.RESUME_INFO,
            admin.FREEZE_INFO,
            admin.DEFROST_INFO,
            admin.FROZEN_INFO,
            admin.TIPBAN_INFO,
            admin.TIPUNBAN_INFO,
            admin.TIPBANNED_INFO,
            admin.STATSBAN_INFO,
            admin.STATSUNBAN_INFO,
            admin.STATSBANNED_INFO
        ]
    }
}

class HelpCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger()

    async def cog_before_invoke(self, ctx: Context):
        ctx.error = False
        # Only allow tip commands in public channels
        msg = ctx.message
        # Determine if user is admin
        ctx.god = msg.author.id in config.Config.instance().get_admin_ids()
        if not ctx.god:
            ctx.admin = False
            for g in self.bot.guilds:
                member = g.get_member(msg.author.id)
                if member is not None:
                    for role in member.roles:
                        if role.id in config.Config.instance().get_admin_roles():
                            ctx.admin = True
                            break
                if ctx.admin:
                    break
        else:
            ctx.admin = True

    def get_entries(self, commands: list) -> list:
        entries = []
        for cmd in commands:
            entries.append(Entry(f"{config.Config.instance().command_prefix}{cmd.triggers[0]}", cmd.details))
        return entries

    def get_help_pages(self, cmd_dict: dict, adminhelp: bool = False) -> list:
        """Builds paginated help menu"""
        pages = []
        # Overview
        author=f"Graham v{__version__} ({'BANANO' if Env.banano() else 'WATERMELONANO'}) edition"
        title="Command Overview"
        description=("Use `{0}help command` for more information about a specific command " +
                " or go to the next page").format(config.Config.instance().command_prefix)
        entries = []
        for k, cmd_list in cmd_dict.items():
            for cmd in cmd_dict[k]['cmd_list']:
                entries.append(Entry(f"{config.Config.instance().command_prefix}{cmd.triggers[0]}", cmd.overview))
        if adminhelp:
            entries.append(Entry(f"{config.Config.instance().command_prefix}adminhelp", "View the full list of admin commands"))
        pages.append(Page(entries=entries, title=title,author=author, description=description))
        # Build detail pages
        for group, details in cmd_dict.items():
            author=cmd_dict[group]['header']
            description=cmd_dict[group]['info']
            entries = self.get_entries(cmd_dict[group]['cmd_list'])
            pages.append(Page(entries=entries, author=author,description=description))
        # Info
        entries = [Entry(f"{config.Config.instance().command_prefix}{tips.TIPAUTHOR_INFO.triggers[0]}", tips.TIPAUTHOR_INFO.details)]
        author=f"Graham v{__version__} for {Env.currency_name()}"
        heart = '\U0001F49B' if Env.banano() else '\U0001F499'
        description = "This bot is completely free, open source, and MIT licnesed"
        description+= f"\n\nMade with {heart} for the **BANANO** and **WATERMELONANO** communities"
        description+= f"\nHangout with some awesome people at https://chat.banano.cc"
        description+= f"\nMy Discord: **@bbedward#9246**"
        description+= f"\nMy Reddit: **/u/bbedward**"
        description+= f"\nMy Twitter: **@theRealBbedward**"
        description+= f"\n\nGraham GitHub: https://github.com/bbedward/Graham_Nano_Tip_Bot"
        pages.append(Page(entries=entries, author=author,description=description))
        return pages

    @commands.command()
    async def help(self, ctx: Context):
        """Show help menu or show info about a specific command"""
        msg = ctx.message
        # If they spplied an argument post usage for a specific command if applicable
        content = msg.content.split(' ')
        if len(content) > 1:
            arg = content[1].strip().lower()
            found = False
            for key, cmd in COMMANDS.items():
                for c in cmd['cmd_list']:
                    if arg in c.triggers:
                        found = True
                        await Messages.send_usage_dm(msg.author, c)
            if not found:
                await Messages.send_error_dm(msg.author, f'No such command: "**{arg}**"')
        else:
            try:
                pages = Paginator(self.bot, message=msg, page_list=self.get_help_pages(COMMANDS, adminhelp=ctx.admin),as_dm=True)
                await pages.paginate(start_page=1)
            except CannotPaginate as e:
                self.logger.exception('Exception in paginator')

    @commands.command()
    async def adminhelp(self, ctx: Context):
        """Show help menu or show info about a specific command"""
        if not ctx.admin:
            return
        msg = ctx.message
        # If they spplied an argument post usage for a specific command if applicable
        content = msg.content.split(' ')
        if len(content) > 1:
            arg = content[1].strip().lower()
            found = False
            for key, cmd in ADMIN_COMMANDS.items():
                for c in cmd['cmd_list']:
                    if arg in c.triggers:
                        found = True
                        await Messages.send_usage_dm(msg.author, c)
            if not found:
                await Messages.send_error_dm(msg.author, f'No such command: "**{arg}**"')
        else:
            try:
                pages = Paginator(self.bot, message=msg, page_list=self.get_help_pages(ADMIN_COMMANDS),as_dm=True)
                await pages.paginate(start_page=1)
            except CannotPaginate as e:
                self.logger.exception('Exception in paginator')
