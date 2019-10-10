from KnuthShuffle import KnuthShuffle

if __name__ == '__main__':
    shuffle = KnuthShuffle(123)
    sBox = shuffle.create_sBox()
    inverse_sBox = shuffle.create_inverse_sBox()
