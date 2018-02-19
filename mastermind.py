
from itertools import product
import random

from functools import lru_cache

from collections import namedtuple
from collections import defaultdict

N_COLOURS = 6
N_PEGS    = 4

BOARDS    = list(product( range(N_COLOURS), repeat=N_PEGS ))

game = namedtuple('game', ['played', 'score', 'answer'])


@lru_cache(maxsize=(N_PEGS**N_COLOURS)**2  )
def match(answer: list, guess: list) -> (int, int):
    ''' return position and colour matches for guess 
    
    position matches is the number of exact matches
    colour_matches is the number of matching colours - including position matches
    
    Example:
        pos_matches, col_matches = match(answer=[1,1,3,2], guess=[1,0,2,2])
        print(f'{pos_matches} exact matches and {col_matches-pos_matches} colour matches.')
    
    '''
    position_matches = sum( a==g for a,g in zip(answer, guess) )

    colour_matches = 0
    for col in range(N_COLOURS):
        n_answer = sum( a == col for a in answer )
        n_guess  = sum( g == col for g in guess )
        colour_matches += min(n_answer, n_guess)
    
    return position_matches, colour_matches


def make_bags( guess, bag ):
    ''' given a bag with possible boards and a possible guess, calculate
    the bag-partitions. One bag will hold all the boards which scored 2,2
    and one will hold all the 1,2 boards etc..'''
    new_bags = defaultdict(list)
    
    for answer in bag:
        new_bags[ match( answer, guess ) ].append(answer)

    return new_bags


def partition_score(bag_defs: dict):
    ''' bag_defs has a list of boards for each possible match-score 
    
    calculate score as the worst possible outcome '''
    return max( len(answers) for match_score,answers in bag_defs.items())


def play(verbose=False):

    answer     = random.choice(BOARDS)
    bag        = BOARDS
    game_score = 1
    played     = []

    while len(bag) > 1:
        game_score += 1
        possible_guesses = { guess:make_bags( guess, bag ) for guess in BOARDS}

        (score, best_guess), *_ = sorted((partition_score(bag_defs), board) 
                                          for board,bag_defs in possible_guesses.items())

        # make guess and get score
        score = match(answer, best_guess)

        played.append(best_guess)

        bag = possible_guesses[best_guess][score]
        if verbose:
            print( f'{best_guess} | {score} | {len(bag)} boards left...' )

    if verbose:
        print( f'{bag[0]}' )
    played.append(bag)
    
    if verbose:
        print( f'-----------------------------\n{answer} in {game_score} moves' )

    return game( played=played, score=game_score, answer=answer )



if __name__ == '__main__':

    _ = play(verbose=True)

    # 
    # N = 100
    # plays = []
    # for _ in tqdm(range(N)):
    #     plays.append(play())
        

    # print( f'mean score = {sum(p.score for p in plays)/N}' )