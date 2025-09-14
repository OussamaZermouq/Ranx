import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from get_account_json import load_json, write_to_json, check_user_exist
from fetch_api import (
    fetch_last_MMR_registered,
    get_puuid,
    fetch_user,
    get_rr,
    get_level,
    fetch_last_MMR_registered_v3,
)
from fetch_api_skins import fetch_skin_item, fetch_user_daily_skins
import py_hot_reload


# TODO: add a command add_command so that people can add accounts to the database (DONE)
# TODO: add a rr in tier in from of the rank eg: (Gold 1 : 20/100) (DONE)
# TODO: try to find a way to check if a player is in a game (NOT POSSIBLE EXCEPT WHEN USING ANOTHER API)

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix="/", intents=intents)
client = discord.Client(intents=intents)
load_dotenv()
token = os.getenv("Discord_bot_Token")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


ranks = {
    "Unranked": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991750/unranked_resized_ockn8p.png",
    "Unrated": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991750/unranked_resized_ockn8p.png",
    "Iron_1": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991746/Iron_1_vqs27k.png",
    "Iron_2": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991746/Iron_1_vqs27k.png",
    "Iron_3": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991746/Iron_3_mmx7z2.png",
    "Bronze_1": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Bronze_1_edicla.png",
    "Bronze_2": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Bronze_2_giycz1.png",
    "Bronze_3": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Bronze_3_c2defs.png",
    "Silver_1": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991750/Silver_1_psp73w.png",
    "Silver_2": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991751/Silver_2_o9fcpe.png",
    "Silver_3": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991749/Silver_3_f7do3j.png",
    "Gold_1": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Gold_1_ynm6mm.png",
    "Gold_2": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Gold_2_atnbed.png",
    "Gold_3": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991743/Gold_3_kkhr2j.png",
    "Platinum_1": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991747/Platinum_1_rxwnde.png",
    "Platinum_2": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991749/Platinum_2_yl6xgx.png",
    "Platinum_3": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991750/Platinum_3_xsny4k.png",
    "Diamond_1": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Diamond_1_ouakms.png",
    "Diamond_2": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Diamond_2_ms9aro.png",
    "Diamond_3": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Diamond_3_pcmjma.png",
    "Ascendant_1": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Ascendant_1_goeftw.png",
    "Ascendant_2": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Ascendant_2_ev9ues.png",
    "Ascendant_3": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991742/Ascendant_3_lyj4oa.png",
    "Immortal_1": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991743/Immortal_1_sjqkas.png",
    "Immortal_2": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991743/Immortal_1_sjqkas.png",
    "Immortal_3": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991743/Immortal_3_jcgrem.png",
    "Radiant": "https://res.cloudinary.com/dlnxxztxa/image/upload/v1755991749/Radiant_jngvo6.png",
}


@bot.tree.command(
    name="rank", description="Check a player's rank using the username and the tag."
)
async def slash_command(interaction: discord.Interaction, username: str, tag: str):
    account_data = fetch_user(username, tag)
    if account_data is None:
        embed_account_error = discord.Embed(
            description=f"Either the information you have entered are incorrect or there is an issue with the API. Try again later.",
            color=0xFC1808,
        )
        await interaction.response.send_message(
            embed=embed_account_error, ephemeral=True
        )
    else:
        account_rank_data = fetch_last_MMR_registered(account_data["data"]["puuid"])
        if account_rank_data.get("old") == "true":
            player_rank = "Unranked"
        else:
            player_rank = account_rank_data.get("rank")
        account_rr = get_rr(get_puuid(username=username, tag=tag))
        embed_account_ranks = discord.Embed(
            description=f"{username}'s account information : ", color=0x00FF00
        )
        embed_account_ranks.add_field(
            name="Username and tag", value=f"{username}#{tag}", inline=True
        )
        embed_account_ranks.add_field(
            name="Rank",
            value=f"{account_rank_data.get('rank')} | {account_rank_data.get('act')} | ({account_rr}/100)",
            inline=True,
        )

        embed_account_ranks.set_thumbnail(
            url=f"{ranks[player_rank.replace(' ','_')]}"
        )

        embed_account_ranks.set_image(url=account_data["data"]["card"]["wide"])
        embed_account_ranks.set_footer(
            text=f"Request made by @{interaction.user.name}",
            icon_url=f"{interaction.user.avatar.url}",
        )

        await interaction.response.send_message(embed=embed_account_ranks)


@bot.tree.command(
    name="ranks", description="Get a list of all the pre-saved accounts' ranks."
)
async def slash_command(interaction: discord.Interaction):
    for role in interaction.user.roles:
        if role.name == "Calilouat":
            is_permissible = True
            break
        else:
            is_permissible = False

    if is_permissible == True:
        accounts = load_json()["accounts"]
        embed_success = discord.Embed(
            description=f"I have found {len(accounts)} accounts in my database, you'll recieve followup message if you are on the list."
        )
        await interaction.response.defer()
        await interaction.followup.send(embed=embed_success, ephemeral=True)
        for i in range(0, len(accounts)):

            username = accounts[i]["username"]
            tag = accounts[i]["tag"]
            login = accounts[i]["login"]
            password = accounts[i]["password"]

            player_rank_data = fetch_last_MMR_registered_v3(username, tag)
            player_level = get_level(username, tag)
            account_rr = get_rr(get_puuid(username=username, tag=tag))

            embed_account = discord.Embed(
                description=f"{username}'s account information : ",
                color=0x00FF00,
                type="article",
            )

            embed_account.add_field(
                name="Username and tag",
                value=f"{username}#{tag} Level : {player_level}",
                inline=True,
            )

            embed_account.add_field(
                name="Rank",
                value=f"{player_rank_data['data']['current']['tier']['name']} | RR ({player_rank_data['data']['current']['rr']}/100)",
                inline=False,
            )
            embed_account.add_field(
                name="ELO",
                value=f"{player_rank_data['data']['current']['elo']}",
                inline=True,
            )
            embed_account.add_field(
                name="Peak rank",
                value=f"{player_rank_data['data']['peak']['tier']['name'] } | Season : {player_rank_data['data']['peak']['season']['short'] } ",
                inline=False,
            )
            embed_account.add_field(name="Login", value=login, inline=True)

            embed_account.add_field(name="Password", value=password, inline=True)

            embed_account.set_thumbnail(
                url=f"{ranks[player_rank_data['data']['current']['tier']['name'].replace(' ','_')]}"
            )
            embed_account.set_footer(
                text=f"Request made by @{interaction.user.name}",
                icon_url=f"{interaction.user.avatar.url}",
            )
            await interaction.followup.send(embed=embed_account, ephemeral=True)

        embed_end = discord.Embed(
            description=f"You have a spear account? you can share it using the /add_account. Your account will only appear to the chosen ones ;)",
            color=0xFFFF00,
        )
        await interaction.followup.send(embed=embed_end, ephemeral=True)
    else:
        await interaction.response.send_message(
            "You don't have access to this command. If you have been forgotten ask Keygenexe",
            ephemeral=True,
        )


@bot.tree.command(
    name="add_account", description="Add an account to the RanX database."
)
async def slash_command(
    interaction: discord.Interaction, username: str, tag: str, login: str, password: str
):
    user_check = fetch_user(username, tag)
    if user_check == -1:
        embed_account_error = discord.Embed(
            description="Error while adding your account, this user doesnt exists.",
            color=0xFC1808,
        )
        await interaction.response.send_message(
            embed=embed_account_error, ephemeral=True
        )
        return
    else:
        user_check_json = check_user_exist(username, tag)
        if user_check_json == -1:
            embed_account_error = discord.Embed(
                description="Error while adding your account, this account already exists in my database.",
                color=0xFC1808,
            )
            await interaction.response.send_message(
                embed=embed_account_error, ephemeral=True
            )
            return
        else:
            write_to_json(username=username, tag=tag, login=login, password=password)
            embed_account_success = discord.Embed(
                description="Account added successfully, user /ranks to see the rest of the accounts",
                color=0x48F542,
            )
            await interaction.response.send_message(
                embed=embed_account_success, ephemeral=True
            )


# @bot.tree.command(name="skins", description="Check the daily skins for an account")
# async def slash_command(interaction:discord.Interaction, username:str, tag:str):
#    user_check = fetch_user(username, tag)
#    if user_check == -1:
#        embed_account_error = discord.Embed(description="Error while adding your account, this user doesnt exists.",color=0xfc1808)
#        await interaction.response.send_message(embed = embed_account_error, ephemeral=True)
#        return
#    else:
#        await interaction.response.defer()
#        daily_skins_uuid = fetch_user_daily_skins(get_puuid(username=username, tag=tag))
#        for skin_uuid in daily_skins_uuid:
#            skin_item = fetch_skin_item(skin_uuid)
#            skin_embed = discord.Embed(description=f"{username}'s daily skins")
#            skin_embed.add_field(name="skin 1",
#                                 value=skin_item['data']['displayName'],
#                                 inline=False)
#            skin_embed.set_image(url=skin_item['data']['displayIcon'])
#            await interaction.followup.send(embed=skin_embed)
#


def main():
    bot.run(token)


py_hot_reload.run_with_reloader(main)
