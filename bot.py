import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from get_account_json import load_json, write_to_json, check_user_exist
from fetch_api import fetch_rank, get_puuid, fetch_user, get_rr, get_level, return_last_filled_rank
from fetch_api_skins import fetch_skin_item, fetch_user_daily_skins




#TODO: add a command add_command so that people can add accounts to the database (DONE)
#TODO: add a rr in tier in from of the rank eg: (Gold 1 : 20/100) (DONE)
#TODO: try to find a way to check if a player is in a game (NOT POSSIBLE EXCEPT WHEN USING ANOTHER API)

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='/', intents=intents)
client = discord.Client(intents=intents)
load_dotenv()
token = os.getenv('Discord_bot_Token')



@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

ranks = ['Unranked','Iron_1','Iron_2','Iron_3','Bronze_1','Bronze_2','Bronze_3',
         'Silver_1','Silver_2','Silver_3','Gold_1','Gold_2','Gold_3',
         'Platinum_1','Platinum_2','Platinum_3','Diamond_1','Diamond_2',
         'Diamond_3','Ascendant_1','Ascendant_2','Ascendant_3','Immortal_1',
         'Immortal_2','Immortal_3','Radiant']

ranks_url = ['https://i122.fastpic.org/big/2023/1201/92/4ed842285cfa4519fa39b1b77c66d192.png',
             'https://i122.fastpic.org/big/2023/1130/e5/0cf5e14744db48be25d4ae6365a954e5.png',
             'https://i122.fastpic.org/big/2023/1130/9a/31b8deddcd1466170d4d86a934b6b99a.png',
             'https://i122.fastpic.org/big/2023/1130/a1/e2b0045f62349132642f3f4d0199f7a1.png',
             'https://i122.fastpic.org/big/2023/1130/dd/3d5ac2a6190ade272192ac397be368dd.png',
             'https://i122.fastpic.org/big/2023/1130/39/134f8874e4cb0d2ad65557e9b25b6139.png',
             'https://i122.fastpic.org/big/2023/1130/3c/ac3b10d00562ddd45af9f4b2cf72603c.png',
             'https://i122.fastpic.org/big/2023/1130/fa/d46ab6609184406d29470110b97d01fa.png',
             'https://i122.fastpic.org/big/2023/1130/f6/0619f490e5bca4323453eb6ab6c46df6.png',
             'https://i122.fastpic.org/big/2023/1130/57/e68b016a3dc759ef4f5fe268878fe957.png',
             'https://i122.fastpic.org/big/2023/1130/b2/540614fe12d026c5c1c9dfd9010e3fb2.png',
             'https://i122.fastpic.org/big/2023/1130/26/4972be2c581a4b35350af951f08f9d26.png',
             'https://i122.fastpic.org/big/2023/1130/23/490bc63d77fc46d9973f374d53808523.png',
             'https://i122.fastpic.org/big/2023/1201/40/dce027244e3d0ab7e2a5bcf3d6158e40.png',
             'https://i122.fastpic.org/big/2023/1130/94/7981682eda5028d3728a28ccf6fc0c94.png',
             'https://i122.fastpic.org/big/2023/1130/18/879e186b1c63654504271704fabf3018.png',
             'https://i122.fastpic.org/big/2023/1130/b6/82b0f3346833f1f36e861cf6f91b9eb6.png',
             'https://i122.fastpic.org/big/2023/1130/10/b1dde8bf3d633290a30b0a3599fa8f10.png',
             'https://i122.fastpic.org/big/2023/1130/86/0eb703adb9dbfb0a431ef1185e24ff86.png',
             'https://i122.fastpic.org/big/2023/1130/16/c49347e9569a5db85202b6c980c8ed16.png',
             'https://i122.fastpic.org/big/2023/1130/0f/ce25cebf8d622a885158abafa2558d0f.png',
             'https://i122.fastpic.org/big/2023/1130/79/3712b1f5a7c87118b9b641869b7d5679.png',
             'https://i122.fastpic.org/big/2023/1130/ac/e946c43441bc3c15ded914e8c3b553ac.png',
             'https://i122.fastpic.org/big/2023/1130/86/e017e900fb3755a7e18433082ee83186.png',
             'https://i122.fastpic.org/big/2023/1130/15/efda88d8f5ec02bd2530379dbb951d15.png',
             'https://i122.fastpic.org/big/2023/1130/f5/eb9db0c88ae802f5a98611ea889c29f5.png'
             ]

rank_dict = dict(zip(ranks,ranks_url))

@bot.tree.command(name="rank",description="Check a player's rank using the username and the tag.")
async def slash_command(interaction:discord.Interaction, username:str, tag:str):
    account_data = fetch_user(username, tag)
    if account_data is None:
        embed_account_error = discord.Embed(description=f"Either the information you have entered are incorrect or there is an issue with the API. Try again later.",color=0xfc1808)
        await interaction.response.send_message(embed=embed_account_error, ephemeral=True)
    else:
        account_rank = return_last_filled_rank(account_data['data']['puuid'])
        account_rr = get_rr(get_puuid(username=username,tag=tag))
        embed_account_ranks = discord.Embed(description=f"{username}'s account information : ",color=0x00FF00)
        embed_account_ranks.add_field(name='Username and tag',
                                    value=f"{username}#{tag}",
                                    inline=True)
        embed_account_ranks.add_field(name='Rank',
                                    value=f"{account_rank.get('rank')} | {account_rank.get('season')} | ({account_rr}/100)",
                                    inline=True)
        
        embed_account_ranks.set_thumbnail(url=f"{rank_dict[account_rank.get('rank').replace(' ','_')]}")
        
        embed_account_ranks.set_image(url=account_data['data']['card']['wide'])
        embed_account_ranks.set_footer(text=f"Request made by @{interaction.user.name}", icon_url=f"{interaction.user.avatar.url}")
        
        await interaction.response.send_message(embed=embed_account_ranks)

@bot.tree.command(name="ranks", description="Get a list of all the pre-saved accounts' ranks.")
async def slash_command(interaction:discord.Interaction):
    for role in interaction.user.roles:
        if role.name =='Calilouat':
            is_permissible = True
            break
        else:
            is_permissible = False
            
    if is_permissible == True:
        accounts = load_json()['accounts']
        embed_success = discord.Embed(description=f"I have found {len(accounts)} accounts in my database, you'll recieve followup message if you are on the list.")
        await interaction.response.defer()
        await interaction.followup.send(embed=embed_success, ephemeral=True)
        for i in range (0, len(accounts)):
            
            username = accounts[i]['username']
            tag = accounts[i]['tag']
            login = accounts[i]['login']
            password = accounts[i]['password']
            
            player_rank = return_last_filled_rank(get_puuid(username, tag))
            player_level = get_level(username, tag)

            if player_rank is None or player_rank.get('rank')=='Unrated':
                player_rank ='Unranked'

            if player_rank ==-2:
                embed_errored_account = discord.Embed(description=f"API limit reached please retry the command in 30 sec",color=0xfc1808)
                await interaction.followup.send(embed=embed_errored_account, ephemeral=True)
                continue
            if player_rank ==-1:
                embed_errored_account = discord.Embed(description=f"There is an issue with the {username}'s account",color=0xfc1808)
                await interaction.followup.send(embed=embed_errored_account, ephemeral=True)
                continue
            account_rr = get_rr(get_puuid(username=username,tag=tag))
            
            embed_account = discord.Embed(description=f"{username}'s account information : ",
                                        color=0x00FF00,
                                        type='article')
            
            embed_account.add_field(name='Username and tag',
                                value=f"{username}#{tag} Level : {player_level}",
                                inline=True)
                                
            embed_account.add_field(name='Rank',
                                value=f"{player_rank.get('rank')} | {player_rank.get('season')} | ({account_rr}/100)",
                                inline=False)
            
            embed_account.add_field(name='Login',
                                value=login,
                                inline=True)
                                
            embed_account.add_field(name='Password',
                                value=password,
                                inline=True)
                                
            embed_account.set_thumbnail(url=f"{rank_dict[player_rank.get('rank').replace(' ','_')]}")
            embed_account.set_footer(text=f"Request made by @{interaction.user.name}", icon_url=f"{interaction.user.avatar.url}")
            
            await interaction.followup.send(embed=embed_account, ephemeral=True)
    else:
        await interaction.response.send_message("You don't have access to this command. If you have been forgotten ask Keygenexe", ephemeral=True)



@bot.tree.command(name="add_account", description="Add an account to the RanX database.")
async def slash_command(interaction:discord.Interaction, username:str, tag:str, login:str, password:str):
    user_check = fetch_user(username, tag)
    if user_check == -1:
        embed_account_error = discord.Embed(description="Error while adding your account, this user doesnt exists.",color=0xfc1808)
        await interaction.response.send_message(embed = embed_account_error, ephemeral=True)
        return
    else:
        user_check_json = check_user_exist(username, tag)
        if user_check_json == -1:
            embed_account_error = discord.Embed(description="Error while adding your account, this account already exists in my database.",color=0xfc1808)
            await interaction.response.send_message(embed=embed_account_error, ephemeral=True)
            return
        else:
            write_to_json(username=username, tag=tag, login=login, password=password)
            embed_account_success = discord.Embed(description="Account added successfully, user /ranks to see the rest of the accounts", color=0x48f542) 
            await interaction.response.send_message(embed=embed_account_success, ephemeral=True)


#@bot.tree.command(name="skins", description="Check the daily skins for an account")
#async def slash_command(interaction:discord.Interaction, username:str, tag:str):
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

bot.run(token)