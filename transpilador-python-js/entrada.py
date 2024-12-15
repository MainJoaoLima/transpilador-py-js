x = 3
y = 1
g = [1,2,3]

def test ():
    for y in g:
        y += 1

        if x > 3 or y > 3:
            return 5
            
        else:
            return 1
