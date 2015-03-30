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
        self._calculate_adjacency()

    def _calculate_adjacency(self):
        self.adjacency = 0
        if self.previous_coin and self.heads == self.previous_coin.heads:
            self.adjacency = self.adjacency + 1
        if self.next_coin and self.heads == self.next_coin.heads:
            self.adjacency = self.adjacency + 1

    def flip(self):
        self.heads = not self.heads
        self.tail = not self.heads
        self._calculate_adjacency()

    def __repr__(self):
        return '<Coin: heads={0}, adjacency={1}, previous_coin={2}, next_coin={3}>'.format(self.heads, self.adjacency, self.previous_coin.heads if self.previous_coin else None, self.next_coin.heads if self.next_coin else None)

def split_coins(coins):
    heads = [c for c in coins if c.heads]
    tails = [c for c in coins if c.tail]
    return heads, tails

def calculate_adjacency(coins):
    return sum([c.adjacency for c in coins])

if __name__ == '__main__':
    import random
    coin_states = [random.randint(0,1) for _ in range(10)]
    print(coin_states)
    coins = []
    for i, cs in enumerate(coin_states):
        if i == 0:
            coin = Coin(True if cs == 1 else False, None)
        else:
            coin = Coin(True if cs == 1 else False, coins[-1])
        coins.append(coin)
    for coin in coins:
        print(coin)
        print()
