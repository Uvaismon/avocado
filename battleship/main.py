import random
import time

class BattleShip:
    def __init__(self):
        self.ocean_map = [['0']*10 for i in range(10)]
        self.player_ship = 0
        self.computer_ship = 0

    def print_map(self):
        print('\n    0 1 2 3 4 5 6 7 8 9')
        for i, k in enumerate(self.ocean_map):
            print(i, end=' | ')
            for j in k:
                if j == '0' or j == '2':
                    print(end='  ')
                else:
                    print(j, end=' ')
            print(' | ' + str(i))
        print('    0 1 2 3 4 5 6 7 8 9')
        print('Computer Ships={} | Your ships={}'.format(self.computer_ship,self.player_ship))

    def deploy_player_ships(self):
        print('Deploy your ships')
        while self.player_ship < 5:
            x, y = input('Enter x y coordinates for ship {}: '.format(self.player_ship+1)).split()
            x, y = int(x), int(y)
            if x > 9 or y > 9 or self.ocean_map[x][y] != '0':
                print('Invalid coordinates')
                continue
            self.ocean_map[x][y] = '@'
            self.player_ship += 1

    def deploy_computer_ships(self):
        print('Computer is deploying ships')
        while self.computer_ship < 5:
            time.sleep(2)
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if self.ocean_map[x][y] != '0':
                continue
            self.ocean_map[x][y] = '2'
            self.computer_ship += 1
            print('Computer deployed ship {}'.format(self.computer_ship))

    def play(self):
        while self.computer_ship > 0 and self.player_ship > 0:
            self.print_map()
            print('Your turn')
            x, y = input('Enter x y coordinates to attack: ').split()
            x, y = int(x), int(y)
            if x > 9 or y > 9 :
                print('Sorry, you missed.')
            elif self.ocean_map[x][y] == '2':
                print('Boom, you sunk the ship!')
                self.computer_ship -= 1
                self.ocean_map[x][y] = '!'
            elif self.ocean_map[x][y] == '@':
                print('Oh no, you sunk your own ship')
                self.player_ship -= 1
                self.ocean_map[x][y] = 'x'
            else:
                print('Sorry, you missed.')
                self.ocean_map[x][y] = '-'
            if self.player_ship == 0 or self.computer_ship == 0:
                continue
            print('Computer\'s turn')
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if self.ocean_map[x][y] == '@':
                print('The computer sunk one of your ships')
                self.player_ship -= 1
                self.ocean_map[x][y] = 'x'
            elif self.ocean_map[x][y] == '2':
                print('The computer sunk one of its own ships')
                self.computer_ship -= 1
                self.ocean_map[x][y] = '!'
            else:
                print('The computer missed')
            time.sleep(3)

    def result(self):
        if self.player_ship > 0:
            print('Hooray! You won the battle :)')
        else:
            print('You lost the battle :(')



if __name__ == '__main__':
    game_object = BattleShip()
    print('\n****Welcome to Battle Ship game****\n')
    print('Right now the sea empty')
    game_object.print_map()
    game_object.deploy_player_ships()
    game_object.deploy_computer_ships()
    game_object.play()
    game_object.result()

