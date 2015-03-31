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

def split_coins(coins):
    heads = [c for c in coins if c.heads]
    tails = [c for c in coins if c.tail]
    return heads, tails

def calculate_adjacency(coins):
    return sum([c.adjacency for c in coins])

def flip_a_coin(flip_coin_with_heads):
    def _flip_a_coin(coins):
        flipped = False
        for coin in coins:
            if coin.previous_coin is None or coin.next_coin is None or flipped:
                continue
            if coin.heads != coin.previous_coin.heads:
                if flip_coin_with_heads and coin.previous_coin.tail and coin.next_coin.tail and coin.heads:
                    coin.flip()
                    flipped = True
                if not flip_coin_with_heads and coin.previous_coin.heads and coin.next_coin.heads and coin.tail:
                    coin.flip()
                    flipped = True
    return _flip_a_coin

flip_a_coin_with_heads = flip_a_coin(True)
flip_a_coin_with_tail = flip_a_coin(False)

if __name__ == '__main__':
    import random
    coin_sides = [random.randint(0,1) for _ in range(20)]
    print(coin_sides)
    coins = []
    for i, cs in enumerate(coin_sides):
        if i == 0:
            coin = Coin(True if cs == 1 else False, None)
        else:
            coin = Coin(True if cs == 1 else False, coins[-1])
        coins.append(coin)

    h, t = split_coins(coins)
    ha, ta = calculate_adjacency(h), calculate_adjacency(t)
    print('Adjacencies before flipping')
    print(coin_states(coins))
    print('Heads -> {}'.format(ha))
    print('Tail -> {}'.format(ta))
    print()
    if ha < ta:
        flip_a_coin_with_heads(coins)
    else:
        flip_a_coin_with_tail(coins)

    h, t = split_coins(coins)
    ha, ta = calculate_adjacency(h), calculate_adjacency(t)
    print('Adjacencies after flipping')
    print(coin_states(coins))
    print('Heads -> {}'.format(ha))
    print('Tail -> {}'.format(ta))
    print()
