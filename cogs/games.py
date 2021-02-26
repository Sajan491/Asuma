import discord
from discord.ext import commands
import random

class Games(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.winningConditions = [
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [0,4,8],
            [2,4,6]
        ]
        self.player1 = ""
        self.player2 = ""
        self.turn = ""
        self.board = []
        self.gameOver = True
        self.count = 0

    @commands.command()
    async def tictactoe(self, ctx, p1 : discord.Member, p2: discord.Member):
        if self.gameOver:
            self.gameOver = False
            self.board = [":white_large_square:",":white_large_square:",":white_large_square:",
                    ":white_large_square:",":white_large_square:",":white_large_square:",
                    ":white_large_square:",":white_large_square:",":white_large_square:"]
            self.player1  = p1
            self.player2 = p2

            #determine who goes first
            num = random.randint(1,2)
            if num == 1:
                self.turn = self.player1
                await ctx.send("<@" + str(self.player1.id)+ "> goes first as ':regional_indicator_x:' .")
            else:
                self.turn = self.player2
                await ctx.send("<@" + str(self.player2.id)+ "> goes first as ':o2:' .")

            #print the board
            line = ""
            for x in range(len(self.board)):
                if x==2 or x==5 or x==8:
                    line += " " + self.board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + self.board[x]
            await ctx.send("<@" + str(self.turn.id)+ ">'s turn'.")
        else:
            await ctx.send("A game is in progress. Please wait for it to finish.")

    @commands.command()
    async def place(self, ctx, pos: int):

        if not self.gameOver:
            mark = ""
            if self.turn == ctx.author:
                if self.turn == self.player1:
                    mark = ":regional_indicator_x:"
                elif self.turn == self.player2:
                    mark = ":o2:"
                if 0 < pos < 10 and self.board[pos - 1] == ":white_large_square:":
                    self.board[pos - 1] = mark
                    self.count += 1
                    await ctx.channel.purge(limit = 5)

                    # print the board
                    line = ""
                    for x in range(len(self.board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + self.board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + self.board[x]

                    self.check_winner(mark)

                    if self.gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif self.count >= 9:
                        self.gameOver = True
                        self.count = 0
                        await ctx.send("It's a tie!")

                    # switch turns
                    if not self.gameOver:
                        if self.turn == self.player1:
                            self.turn = self.player2
                            await ctx.send("<@" + str(self.player2.id)+">'s turn")
                        elif self.turn == self.player2:
                            self.turn = self.player1
                            await ctx.send("<@" + str(self.player1.id)+">'s turn")
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 and an unmarked tile.")
                    await ctx.channel.purge(limit = 2)
            else:
                await ctx.send("It is not your turn.")
                await ctx.channel.purge(limit = 2)
        else:
            await ctx.send("Please start a new game using the !tictactoe command.")


    def check_winner(self, mark):
        for condition in self.winningConditions:
            if self.board[condition[0]] == mark and self.board[condition[1]] == mark and self.board[condition[2]] == mark:
                self.gameOver = True

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Make sure to mention/ping players")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Also include a position in integer to mark.")
            await ctx.channel.purge(limit = 2)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Make sure to enter an integer.")
            await ctx.channel.purge(limit = 2)

def setup(client):
    client.add_cog(Games(client))

