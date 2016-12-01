import dibu

if __name__ == '__main__':
    print(dibu.parse('''size height=400, width=500
    rectangle upper_left=(3,4), width=3, height=5
    circle center=(5,6), radius=8
    polyline points=[(7,6), (1,2)]
    text t="Hello worldddd is gut", at=(1,2)
    size height=43, width=500'''))