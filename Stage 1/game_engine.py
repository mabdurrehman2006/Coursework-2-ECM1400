def cli_coords_input():
    valid=[1, 2, 3, 4, 5, 6, 7, 8]
    check=True
    while check==True:
        user_x=input("Enter X coordinate(Between 1 to 8)")
        if user_x.isdigit():
            if int(user_x) in valid:
                check=False
        else:
            check=True
    check=True
    while check==True:
        user_y=input("Enter Y coordinate(Between 1 to 8)")
        if user_y.isdigit():
            if int(user_y) in valid:
                check=False
        else:
            check=True
    coordinates=(int(user_x), int(user_y))
    return coordinates


coord=cli_coords_input()
print(coord)