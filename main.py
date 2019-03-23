import time
import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot, has_role, CheckFailure

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["config"]["token"]
owner_id = config["config"]["owner_id"]
setup_done = config["config"]["Setup"]
role_needed = config["config"]["UserRole"]
verified_roles =["Yellow", "Orange", "Red", "Pink", "Violet", "Blue", "Green", "Indian", "Gray"]

if owner_id == "changeme":
    print("Id is not set in configs. Bot is now closing in 5 seconds...")
    time.sleep(5)
    exit()

client: Bot = commands.Bot(command_prefix='cB!')
client.remove_command('help')


def fix_up_string(string):
    first_letter = string[0]
    other_letters = string[1:]
    return first_letter.upper() + other_letters.lower()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Bot is running.')
    await client.wait_until_ready()
    print("Current Servers:")
    for server in client.servers:
        print(server.name)


@client.command(pass_context=True)
async def setup(ctx):
    global owner_id
    if setup_done == 0:
        if ctx.message.author.id == owner_id:
            global config
            await client.say("Time to set up a bot.")
            await client.say("First, what role should be used as a role for using this bot. Use EXACT NAME")
            botUserRole = await client.wait_for_message(author=ctx.message.author)
            config["config"]["UserRole"] = botUserRole.content
            await client.say("Thanks that's about it. I think")
            await client.say("We are now setting up colors on the server. Please don't change roles during the the process.")
            await client.create_role(ctx.message.author.server, name="Yellow", colour=discord.Colour(0xfff200))
            await client.create_role(ctx.message.author.server, name="Orange", colour=discord.Colour(0xfc6600))
            await client.create_role(ctx.message.author.server, name="Red", colour=discord.Colour(0xd30000))
            await client.create_role(ctx.message.author.server, name="Pink", colour=discord.Colour(0xfc0fc0))
            await client.create_role(ctx.message.author.server, name="Violet", colour=discord.Colour(0xb200ed))
            await client.create_role(ctx.message.author.server, name="Blue", colour=discord.Colour(0x0018f9))
            await client.create_role(ctx.message.author.server, name="Green", colour=discord.Colour(0x3bb143))
            await client.create_role(ctx.message.author.server, name="Indian", colour=discord.Colour(0x7c4700))
            await client.create_role(ctx.message.author.server, name="Gray", colour=discord.Colour(0x828282))
            await client.say("Done it should now work. Please don't run this command agian.")
            await client.say("Restart the bot please...")
            config["config"]["Setup"] = 1
            with open("config.json", "w") as f:
                json.dump(config, f)
            exit()
        else:
            await client.say("Leave and never comeback.")
    else:
        await client.say("I told you not to run it agian.")


@client.command(pass_context=True)
@has_role(role_needed)
async def paint(ctx, arg1):
    author = ctx.message.author
    server = ctx.message.server
    role = discord.utils.get(server.roles, name=fix_up_string(arg1))
    if str(role) == "None" or str(role) not in verified_roles:
        await client.say("That is not a color")
        return
    if role in author.roles:
        await client.remove_roles(author, role)
        await client.say("Removing " + str(role) + " from your name.")
    else:
        await client.add_roles(author, role)
        await client.say("Adding " + str(role) + " to your name.")


@paint.error
async def paint_error(error, ctx):
    if isinstance(error, CheckFailure):
        await client.send_message(ctx.message.channel, "You don't have the correct permissions.")
    else:
        await client.send_message(ctx.message.channel, "You missed something")
        raise error


@client.command()
async def list():
    await client.say('Available colors')
    msg = "```" + '\n'.join(verified_roles) + "```"
    await client.say(msg)


@client.command()
async def help():
    embed = discord.Embed(
        title='Use prefix "cB!"',
        colour=discord.Color.blue()
    )
    embed.set_author(
        name='Command list.',
        icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/black-question-mark-ornament_2753.png')
    embed.add_field(name='cB!paint "color" ', value='Adds or removes color from your name.', inline=False)
    embed.add_field(name='cB!list ', value='Lists all available colors', inline=False)
    await client.say(embed=embed)

client.run(TOKEN)

