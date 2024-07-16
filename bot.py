import discord
from discord.ext import commands

# Create a bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Current user sessions
user_sessions = {}

# When bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
# Start semester
@bot.command()
async def start_semester(ctx):
    user_sessions[ctx.author.id] = {'step': 1, 'subjects': []}
    await ctx.send('How many subjects are you taking this semester?')
    
# Wait for a message
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    user_id = message.author.id
    if user_id in user_sessions:
        session = user_sessions[user_id]
        
        # Get number and name of subjects
        if session['step'] == 1:
            session['number_of_subjects'] = int(message.content)
            session['step'] += 1
            await message.channel.send('Enter the name of your subjects, one per message.')
        
        # Get number of assignments for each subject
        elif session['step'] == 2:
            session['subjects'].append({'name': message.content, 'assignments': []})
            if len() == session['number_of_subjects']:
                session['step'] += 1
                await message.channel.send(f'Enter the assignments for {session["subjects"][0]["name"]}, 
                                           one per message in the format "Assignment Name - Due Date (YYYY-MM-DD)". 
                                           Type "done" when finished.')
            else:
                await message.channel.send(f'Enter the assignments for {session["subjects"][0]["name"]}, 
                                           one per message in the format "Assignment Name - Due Date (YYYY-MM-DD)". 
                                           Type "done" when finished.')
                del user_sessions[user_id]
        else:
            try:
                assignment_name, due_date = message.content.split(' - ')
                session['subjects'][0]['assignments'].append({'name': assignment_name, 'due_date': due_date})
                await message.channel.send('Assignment recorded. Enter another assignment or type "done" if you are finished.')
            except ValueError:
                await message.channel.send('Invalid format. Please use "Assignment Name - Due Date (YYYY-MM-DD)".')
    
    await bot.process_commands(message)

# Start the bot
bot.run('bot_token_here')