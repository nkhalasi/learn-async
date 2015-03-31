#Attempt to solve http://blog.csdn.net/xudli/article/details/40818153
class Coin:
    def __init__(self, heads, previous_coin):
        self.heads = True if heads else False
        self.tail = not self.heads
        self.next_coin = None
        if previous_coin:
            self.previous_coin = previous_coin
            self.previous_coin.next_coin = self
        else:
            self.previous_coin = None

    @property
    def adjacency(self):
        adjacency = 0
        if self.previous_coin and self.heads == self.previous_coin.heads:
            adjacency = adjacency + 1
        if self.next_coin and self.heads == self.next_coin.heads:
            adjacency = adjacency + 1
        return adjacency

    def flip(self):
        self.heads = not self.heads
        self.tail = not self.heads

    def __repr__(self):
        return '<Coin: heads={0}, adjacency={1}, previous_coin.heads={2}, next_coin.heads={3}>'.format(self.heads, self.adjacency, self.previous_coin.heads if self.previous_coin else None, self.next_coin.heads if self.next_coin else None)

def coin_states(coins):
    return [1 if c.heads else 0 for c in coins]

def calculate_adjacency(coins):
    return sum([c.adjacency for c in coins])

def flip_coin(coins):
    for coin in coins:
        if coin.previous_coin is None or coin.next_coin is None:
            continue
        #if coin.heads != coin.previous_coin.heads and coin.previous_coin.heads == coin.next_coin.heads:
        if coin.heads != coin.previous_coin.heads and coin.adjacency == 0:
            coin.flip()
            return #because we want to flip on the first eligible coin

if __name__ == '__main__':
    import random
    coin_sides = [random.randint(0,1) for _ in range(20)]
    coins = []
    for i, cs in enumerate(coin_sides):
        if i == 0:
            coin = Coin(True if cs == 1 else False, None)
        else:
            coin = Coin(True if cs == 1 else False, coins[-1])
        coins.append(coin)

    print('Adjacencies before flipping')
    print(coin_states(coins))
    print('Adjacency -> {}'.format(calculate_adjacency(coins)))
    print()
    flip_coin(coins)
    print('Adjacencies after flipping')
    print(coin_states(coins))
    print('Adjacency -> {}'.format(calculate_adjacency(coins)))
    print()
