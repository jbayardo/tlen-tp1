import dibu

if __name__ == '__main__':
    try:
        print(dibu.parse('''size height=400, width=500
        rectangle upper_left=(3,4), width=3, height=5
        circle center=(5,6), radius=8
        polyline points=[(7,6), (1,2)]
        text t="polyline points=[(1,2), (3,4)]", at=(1,2)'''))
    except:
        pass

    print(dibu.parse('''
    size height=300, width=200
    text t="This be what I call \\"Quote\\"", at=(1,2)
    '''))