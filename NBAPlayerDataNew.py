import os, math, random

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (20, 20)

import pygame

pygame.init()
pygame.font.init()

# Part 1: prep work
# --Size of screen--
WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# --Colours--
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (81, 81, 84)
DARK_GREY = (28, 28, 27)
LIGHT_GREY = (150, 157, 158)
BROWN = (38, 8, 6)
LIGHT_BROWN = (92, 33, 9)
DARK_BROWN = (18, 4, 3)
DARK_GREEN = (6, 56, 14)
STEM_GREEN = (94, 115, 77)
DARK_BLUE = (0, 0, 15)
YELLOW = (166, 166, 27)
ORANGE = (148, 99, 7)
DARK_PURPLE = (56, 60, 143)
LIGHT_PURPLE = (165, 48, 194)

# -- fonts --
roman_30 = pygame.font.SysFont("Times New Roman", 30)
roman_20 = pygame.font.SysFont("Times New Roman", 20)

# -- States --
MENU_PAD = 0
DISPLAY_TABLE = 1
ADJUST_FIELD = 2
ADD_RECORD = 3
DELETE_RECORD = 4
VIEW_REPORTS = 5
EXIT = 6

curr_state = MENU_PAD  # set the current state to menu pad so that in the While Loop it will first

# display the menu


# Part 2: functions
def update_file():
    # update the file with the new change/data
    player_data = open("NBA_Players.dat", "w")

    for player in players:  # for every player...
        line = ""
        for field in player:  # add each of their information (adjusted) with a comma to an empty line
            if field == player[-1]:  # do not add comma for last field
                line += field
            else:
                line += field + ","
        player_data.write(
            line +
            "\n")  # add the line + a new space character to the data file
    player_data.close()

    print("\n")


def check_errors(field, data):  ##
    field = field.lower()
    check_empty = data.replace(" ", "")
    if check_empty == "":
        error_text = "Error: No input. Please enter data."
        error_box = [0, 350, WIDTH, 150]
        display_error(error_text, error_box, BLUE)
        return True

    # .lower() everything in case user uses different cases
    elif field == field_titles[id_location].lower(
    ):  # check for possible errors if the user is adjusting/adding Player IDs
        id = data
        if id.isnumeric() == False:
            error_text = "Error: Invalid input. Ensure Player ID's are numbers."
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True

        elif len(id) > max_lenid:
            error_text = "Error: Exceeds max length. Ensure the data fits within %i spaces." % (max_lenid)
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True
        # PINEAPPLE
        for player in players:  # cross check with every player's ID to ensure there are no duplicates
            if player[id_location] == id:
                error_text = "Error: Identical ID. Ensure all Player ID's are unique."
                error_box = [0, 350, WIDTH, 150]
                display_error(error_text, error_box, BLUE)
                return True

    elif field == field_titles[fname_location].lower(
    ) or field == field_titles[lname_location].lower(
    ):  # check for errors with Names
        name = data
        name_alpha = data.replace(" ", "").replace("-", "").replace(
            "'", "")  # get rid of possible non-letter characters in a name
        if name_alpha.isalpha() == False:  # ensure names are inputted correctly
            error_text = "Error: Invalid input. Ensure names consist of only letters (and possibly spaces, ' or -)."
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True
        elif len(name) > max_lenname:
            error_text = "Error: Exceeds max length. Ensure the data fits within %i spaces."% (max_lenname)
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True

    elif field == field_titles[team_location].lower(
    ):  # check for errors with Teams
        team = data
        if team.isalpha() == False or len(team) > max_lenteam or team != team.upper():  # check if the team is in letters, the length is 3, and if it is in uppercase
            error_text = "Error: Invalid input. Ensure team names are the capitalized 3-letter abbreviation of the name."
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True

    elif field == field_titles[jersey_location].lower(
    ):  # check for errors with Jerseys
        jersey_num = data
        if jersey_num.isnumeric() == False or len(jersey_num) > max_lenjersey:
            error_text = "Error: Invalid input. Ensure jerseys numbers are entered as numbers up to 2 digits long."
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True

    elif field == field_titles[pos_location].lower(
    ):  # check for errors with Positions
        position = data
        if position.lower() not in ["guard", "forward", "center"]:
            error_text = "Error: Invalid input. The possible positions are Guard, Forward and Center."
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True
        elif len(position) > max_lenpos:
            error_text = "Error: Exceeds max length. Ensure the data fits within %i spaces." % (max_lenpos)
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True

    elif field == field_titles[weight_location].lower():
        weight = data
        if weight.isnumeric() == False:
            error_text = "Error: Invalid input. Ensure weight is a number in lbs."
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True
        elif len(weight) > max_lenweight:
            error_text = "Error: Exceeds max length. Ensure the data fits within %i spaces." % (max_lenweight)
            error_box = [0, 350, WIDTH, 150]
            display_error(error_text, error_box, BLUE)
            return True

    return False  # did not use an Else here since if it does not return any thing within the ifs and elifs, wit will return false
    # due to having nested ifs and elifs, instead of adding return false on each, it will go directly to this return false


def display_error(text, box_dimen, box_col):
    pygame.draw.rect(screen, box_col,
                     box_dimen)  # create a blue box to hide previous errors

    # display the error text
    error_text = text
    error_str = roman_20.render(error_text, 1, BLACK)
    text_width = error_str.get_width()
    center_x = box_dimen[0] + (
        box_dimen[2] // 2
    )  # middle-horizontal is the initial x + half the width
    start_x = center_x - (
        text_width // 2
    )  # the starting pos is the middle of the box minus half the width of the text
    screen.blit(error_str, (start_x, 375))
    pygame.display.flip()


def create_button(rect_dimen, text, colour):
    # draw a rectangle based of the dimensions and colour passed in
    pygame.draw.rect(screen, colour,(rect_dimen[0], rect_dimen[1], rect_dimen[2], rect_dimen[3]))

    # figure out key parts of the box and text
    text_width = text.get_width()
    text_height = text.get_height()
    center_x = rect_dimen[0] + (rect_dimen[2] // 2)  # middle-horizontal is the initial x + half the width
    center_y = rect_dimen[1] + (rect_dimen[3] // 2)  # middle_vertical is the initial y + half the height
    start_x = center_x - (text_width / 2)  # the start x_pos is the middle of the box - half the width of the text
    start_y = center_y - (text_height / 2)  # the start y_pos is the middle of the box - half the height of the text

    screen.blit(text, (start_x, start_y))


def menu_pad():
    global curr_state  # make curr_state global so that we can quickly change to a different function
    # draw the menu
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, HEIGHT))  # blue background
    heading = "Please select an option"
    heading_text = roman_30.render(heading, 1, BLACK)
    screen.blit(heading_text, (263, 10))
    # variables for red boxes
    x_start = 225
    x_width = 350
    y_start = 80
    y_height = 70
    change_y = 85

    # write the options
    options = [
        "1. Display Table.", "2. Adjust a field in a record.",
        "3. Add a new record.", "4. Delete a record.", "5. View reports."
    ]

    for option in options:  # create a button for each option
        button_dimen = [x_start, y_start, x_width,
                        y_height]  # give a list of dimensions for the box
        string = roman_30.render(option, 1, BLACK)
        create_button(button_dimen, string, RED)
        y_start += change_y  # make each box start lower

    y_start = 80  # reset the y_start

    # create an exit button
    exit_dimen = [5, 5, 68, 30]
    exit_text = "Exit"
    exit_str = roman_20.render(exit_text, 1, BLACK)
    create_button(exit_dimen, exit_str, RED)

    pygame.display.flip()

    # check where the user clicks to determine the state
    running_menu = True
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                curr_state = EXIT  # close the program if they click the 'X'
                running_menu = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get x and y coordinates of the click
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                # print(mouse_x, mouse_y)
                if x_start < mouse_x < x_start + x_width and y_start < mouse_y < y_start + y_height:
                    # if the user clicked within the x- and y-bounds of the first box
                    curr_state = DISPLAY_TABLE
                    running_menu = False

                elif x_start < mouse_x < x_start + x_width and (y_start + change_y) < mouse_y < \
                        (y_start + change_y + y_height):  # check if they clicked the second box
                    curr_state = ADJUST_FIELD
                    running_menu = False

                elif x_start < mouse_x < x_start + x_width and (y_start + 2 * change_y) < mouse_y < \
                        (y_start + 2 * change_y + y_height):  # check if they clicked the third box
                    curr_state = ADD_RECORD
                    running_menu = False

                elif x_start < mouse_x < x_start + x_width and (y_start + 3 * change_y) < mouse_y < \
                        (y_start + 3 * change_y + y_height):  # check if they clicked the fourth box
                    curr_state = DELETE_RECORD
                    running_menu = False

                elif x_start < mouse_x < x_start + x_width and (y_start + 4 * change_y) < mouse_y < \
                        (y_start + 4 * change_y + y_height):  # check if they clicked the fifth box
                    curr_state = VIEW_REPORTS
                    running_menu = False

                elif exit_dimen[0] < mouse_x < exit_dimen[0] + exit_dimen[2] and exit_dimen[1] < mouse_y < \
                        exit_dimen[1] + exit_dimen[3]:  # check if they clicked the fifth box
                    curr_state = EXIT
                    running_menu = False


def display_table():  # function to display the data table
    global curr_state
    pygame.draw.rect(screen, BLUE,
                     (0, 0, WIDTH, HEIGHT))  # create blue background

    # create back-to-menu button
    button_rect = [5, 5, 68, 30]
    text = "< Menu"
    string = roman_20.render(text, 1, BLACK)
    create_button(button_rect, string, RED)

    # create the table
    pygame.draw.line(screen, BLACK, (0, 70),
                     (WIDTH, 70))  # draw horizontal line

    long_fields = [0, 1, 2, 5]  # these field indexes have longer data
    long_space = 140
    short_space = 80
    x_start = 0

    for i in range(len(field_titles)):
        if i in long_fields:
            line_space = long_space  # create a bigger space for the longer fields
        else:
            line_space = short_space

        pygame.draw.line(screen, BLACK, (x_start + line_space, 30),
                         (x_start + line_space, HEIGHT))  # vertical line

        # write the headings
        heading = field_titles[i]
        heading_str = roman_20.render(heading, 1, BLACK)
        heading_width = heading_str.get_width()
        mid_x = x_start + (line_space // 2)

        # write the headings based off aspects such as their width and the mid-point of their allotted space
        if heading_width > line_space - 20:  # if the heading title is too long, separate the words
            space = heading.find(" ")

            word1 = heading[:space]
            str1 = roman_20.render(word1, 1, BLACK)
            width1 = str1.get_width()
            start_text1 = mid_x - (width1 // 2)
            screen.blit(str1, (start_text1, 20))

            word2 = heading[space + 1:]
            str2 = roman_20.render(word2, 1, BLACK)
            width2 = str2.get_width()
            start_text2 = mid_x - (width2 // 2)
            screen.blit(str2, (start_text2, 40))

        else:
            string = roman_20.render(heading, 1, BLACK)
            width = string.get_width()
            mid_x = x_start + (line_space // 2)
            start_text = mid_x - (width // 2)
            screen.blit(string, (start_text, 40))

        x_start += line_space  # add space between every line (amount varies based on length of field)

    # write the records
    y_start = 70
    for player in players:
        x_start = 0
        for i in range(len(player)):
            if i in long_fields:
                line_space = long_space
            else:
                line_space = short_space

            data = player[i]
            string = roman_20.render(data, 1, BLACK)
            width = string.get_width()

            if data.isalpha() == True:  # if the data is letters
                screen.blit(string, (x_start + 4, y_start))
            else:  # if the data is a number
                x_new = (x_start + line_space) - width
                screen.blit(string, (x_new - 4, y_start))

            x_start += line_space  # move each field to the right

        y_start += 20  # move each record down

    pygame.display.flip()

    # check where the user clicks
    running_table = True
    while running_table:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                curr_state = EXIT  # close the program if they click the 'X'
                running_table = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get x and y coordinates of the click
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                # if they click the "< Menu" button, take them back to the menu
                if button_rect[0] < mouse_x < (
                        button_rect[0] +
                        button_rect[2]) and button_rect[1] < mouse_y < (
                            button_rect[1] + button_rect[3]):
                    curr_state = MENU_PAD
                    running_table = False


def adjust_field():
    global curr_state

    # get ID
    pygame.draw.rect(screen, BLUE,
                     (0, 0, WIDTH, HEIGHT))  # create blue background
    input_box = [200, 200, 400, 100]
    pygame.draw.rect(screen, WHITE, (input_box[0], input_box[1], input_box[2],
                                     input_box[3]))  # create box to enter data

    # create back-to-menu button
    button_rect = [5, 5, 68, 30]
    text = "< Menu"
    string = roman_20.render(text, 1, BLACK)
    create_button(button_rect, string, RED)

    running_adjust = True  # will be used to see if the user wants to exit the Adjust function
    find_id = True  # if this is True, ask the user for the ID
    id_active = False  # will be used to get user input
    user_id = ""

    while find_id == True and running_adjust == True:
        id_display = "Please enter the player's ID."
        string = roman_30.render(id_display, 1, BLACK)
        screen.blit(string, (200, 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                curr_state = EXIT  # close the program if they click the 'X'
                find_id = False
                running_adjust = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get x and y coordinates of the click
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]

                if button_rect[0] < mouse_x < button_rect[0] + button_rect[
                        2] and button_rect[
                            1] < mouse_y < button_rect[1] + button_rect[3]:
                    curr_state = MENU_PAD
                    find_id = False
                    running_adjust = False

                # if they click the text box, make it so that they are now inputting data
                elif input_box[0] < mouse_x < input_box[0] + input_box[
                        2] and input_box[
                            1] < mouse_y < input_box[1] + input_box[3]:
                    id_active = True

                else:
                    id_active = False

            if event.type == pygame.KEYDOWN:  # check what the user is inputting
                if id_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_id = user_id[:
                                          -1]  # remove the last str if they click backspace
                        # draw over what they wrote to make it look like the characters are deleting
                        pygame.draw.rect(screen, WHITE,
                                         (input_box[0], input_box[1],
                                          input_box[2], input_box[3]))
                        display_input = roman_20.render(user_id, 1, BLACK)
                        screen.blit(display_input,
                                    (input_box[0] + 10,
                                     input_box[1] + 20))  # print the new text
                        pygame.display.flip()

                    elif event.key == pygame.K_RETURN:
                        player_ids = []  # will contain the ID's of each player
                        for player in players:  # add each player's ID
                            player_id = player[id_location]
                            player_ids.append(player_id)

                        if user_id not in player_ids:  # if the user put in an ID which does not exist, stop the function
                            error_text = "Error: Invalid input. Please enter a valid Player ID."
                            error_box = [0, 350, WIDTH, 150]
                            display_error(error_text, error_box, BLUE)

                        else:
                            find_id = False  # if there are no errors, stop asking for the ID

                    else:
                        user_id += event.unicode  # add the input to the user_id str

        # create a border on the text box based off what the user is doing
        if id_active == True:
            pygame.draw.rect(
                screen, GREEN,
                (input_box[0], input_box[1], input_box[2], input_box[3]), 4)
        else:
            pygame.draw.rect(
                screen, RED,
                (input_box[0], input_box[1], input_box[2], input_box[3]), 4)

        # continuously display what the user is inputting
        display_input = roman_20.render(user_id, 1, BLACK)
        screen.blit(display_input, (input_box[0] + 10, input_box[1] + 20))
        pygame.display.flip()

    # get FIELD
    pygame.draw.rect(screen, BLUE,
                     (0, 0, WIDTH, HEIGHT))  # create the blue background again
    pygame.draw.rect(screen, WHITE, (input_box[0], input_box[1], input_box[2],
                                     input_box[3]))  # create box to enter data

    # create back-to-menu button
    button_rect = [5, 5, 68, 30]
    text = "< Menu"
    string = roman_20.render(text, 1, BLACK)
    create_button(button_rect, string, RED)

    find_field = True  # if this is True, ask the user for the Field
    field_active = False  # will be used to get user input
    user_field = ""
    field_index = 0  # will contain the index of the field the user wants to change
    while find_field == True and running_adjust == True:
        field_display = "Please enter the Field name."
        string = roman_30.render(field_display, 1, BLACK)
        screen.blit(string, (200, 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                curr_state = EXIT  # close the program if they click the 'X'
                find_field = False
                running_adjust = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get x and y coordinates of the click
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]

                # if they click the Menu button, go back to Menu Pad
                if button_rect[0] < mouse_x < button_rect[0] + button_rect[2] and button_rect[1] < mouse_y < button_rect[1] + button_rect[3]:
                    curr_state = MENU_PAD
                    find_field = False
                    running_adjust = False

                # if they click the text box, make it so that they are now inputting data
                elif input_box[0] < mouse_x < input_box[0] + input_box[2] and input_box[1] < mouse_y < input_box[1] + \
                        input_box[3]:
                    field_active = True
                else:
                    field_active = False

            if event.type == pygame.KEYDOWN:  # check what the user is inputting
                if field_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_field = user_field[:
                                                -1]  # remove the last str if they click backspace
                        pygame.draw.rect(screen, WHITE,
                                         (input_box[0], input_box[1],
                                          input_box[2], input_box[3]))
                        display_input = roman_20.render(user_field, 1, BLACK)
                        screen.blit(display_input,
                                    (input_box[0] + 10, input_box[1] + 20))
                        pygame.display.flip()

                    elif event.key == pygame.K_RETURN:  # if the user presses "enter", check for validity of input
                        check_lower = user_field.lower()
                        fields_lower = [
                        ]  # will contain the name of each field in lower case
                        for field in field_titles:
                            fields_lower.append(field.lower())

                        if check_lower not in fields_lower:  # check if the field exists
                            error_text = "Error: Invalid input. Please enter an existing field."
                            error_box = [0, 350, WIDTH, 150]
                            display_error(error_text, error_box, BLUE)

                        else:
                            field_index = fields_lower.index(check_lower)
                            find_field = False  # if there are no errors, stop asking for the Field

                    else:
                        user_field += event.unicode  # add the input to the user_field str

        # create a border on the text box based off what the user is doing
        if field_active == True:
            pygame.draw.rect(
                screen, GREEN,
                (input_box[0], input_box[1], input_box[2], input_box[3]), 4)
        else:
            pygame.draw.rect(
                screen, RED,
                (input_box[0], input_box[1], input_box[2], input_box[3]), 4)

        # continuously display what the user is inputting
        display_input = roman_20.render(user_field, 1, BLACK)
        screen.blit(display_input, (input_box[0] + 10, input_box[1] + 20))
        pygame.display.flip()

    # get CHANGE
    pygame.draw.rect(screen, BLUE,
                     (0, 0, WIDTH, HEIGHT))  # create the blue background again
    pygame.draw.rect(screen, WHITE, (input_box[0], input_box[1], input_box[2],
                                     input_box[3]))  # create box to enter data

    # create back-to-menu button
    button_rect = [5, 5, 68, 30]
    text = "< Menu"
    string = roman_20.render(text, 1, BLACK)
    create_button(button_rect, string, RED)

    find_change = True  # if this is True, ask the user for the Field
    change_active = False  # will be used to get user input
    user_change = ""
    while find_change == True and running_adjust == True:
        field_display = "Please enter the Change data."
        string = roman_30.render(field_display, 1, BLACK)
        screen.blit(string, (200, 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                curr_state = EXIT  # close the program if they click the 'X'
                find_change = False
                running_adjust = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get x and y coordinates of the click
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]

                # if they click the Menu button, go back to Menu Pad
                if button_rect[0] < mouse_x < button_rect[0] + button_rect[2] and button_rect[1] < mouse_y < \
                        button_rect[1] + button_rect[3]:
                    curr_state = MENU_PAD
                    find_change = False
                    running_adjust = False

                # if they click the text box, make it so that they are now inputting data
                elif input_box[0] < mouse_x < input_box[0] + input_box[2] and input_box[1] < mouse_y < input_box[1] + \
                        input_box[3]:
                    change_active = True
                else:
                    change_active = False

            if event.type == pygame.KEYDOWN:  # check what the user is inputting
                if change_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_change = user_change[:-1]  # remove the last str if they click backspace
                        pygame.draw.rect(screen, WHITE,
                                         (input_box[0], input_box[1],
                                          input_box[2], input_box[3]))
                        display_input = roman_20.render(user_change, 1, BLACK)
                        screen.blit(display_input,
                                    (input_box[0] + 10, input_box[1] + 20))
                        pygame.display.flip()

                    elif event.key == pygame.K_RETURN:  # if the user presses "enter", check for validity of input
                        error = check_errors(field_titles[field_index], user_change)

                        if error == False:
                            find_change = False  # if there are no errors, stop asking for the Change

                    else:
                        user_change += event.unicode  # add the input to the user_change str

        # create a border on the text box based off what the user is doing
        if change_active == True:
            pygame.draw.rect(
                screen, GREEN,
                (input_box[0], input_box[1], input_box[2], input_box[3]), 4)
        else:
            pygame.draw.rect(
                screen, RED,
                (input_box[0], input_box[1], input_box[2], input_box[3]), 4)

        # continuously display what the user is inputting
        display_input = roman_20.render(user_change, 1, BLACK)
        screen.blit(display_input, (input_box[0] + 10, input_box[1] + 20))
        pygame.display.flip()

    # from here on, the code will update the file with the user's information
    # only do this if the user has not exited the Adjust function
    if running_adjust == True:
        for i in range(
                len(players)
        ):  # for every player, check if their ID matches the ID the user wants
            if players[i][id_location] == user_id:
                player = i  # assign the index of the desired player

        for field in field_titles:  # check for every field
            if user_field == field.lower(
            ):  # if the field is the same as the user's field, assign the index
                field_index = field_titles.index(field)

        players[player][
            field_index] = user_change  # change the field of the record

        update_file()  # update the file with the new data

        curr_state = MENU_PAD



def add_record():
    global curr_state

    pygame.draw.rect(screen, BLUE,(0, 0, WIDTH, HEIGHT))  # create blue background
    input_box = [200, 200, 400, 100]

    # create back-to-menu button
    button_rect = [5, 5, 68, 30]
    text = "< Menu"
    menu_string = roman_20.render(text, 1, BLACK)

    running_add = True  # will be used to see if the user wants to exit the Adjust function
    empty_record = []
    field_active = False

    for field in field_titles:
        # draw the blue box and input box again to override the last time's work
        pygame.draw.rect(screen, BLUE,(0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(screen, WHITE,(input_box[0], input_box[1], input_box[2], input_box[3]))

        # need to redraw the menu button
        create_button(button_rect, menu_string, RED)

        user_field = ""
        find_field = True
        while find_field == True and running_add == True:
            field_display = "Please enter the player's %s." % (field)
            string = roman_30.render(field_display, 1, BLACK)
            height_str = string.get_height()

            pygame.draw.rect(screen, BLUE, (0, 160,WIDTH, height_str))  # cover up past text
            screen.blit(string, (200, 160))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    curr_state = EXIT  # close the program if they click the 'X'
                    running_add = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # get x and y coordinates of the click
                    mouse_x = pygame.mouse.get_pos()[0]
                    mouse_y = pygame.mouse.get_pos()[1]

                    # if they click the Menu button, go back to the menu
                    if button_rect[0] < mouse_x < button_rect[0] + button_rect[2] and button_rect[1] < mouse_y < button_rect[1] + button_rect[3]:
                        curr_state = MENU_PAD
                        running_add = False

                    # if they click the text box, make it so that they are now inputting data
                    elif input_box[0] < mouse_x < input_box[0] + input_box[2] and input_box[1] < mouse_y < input_box[1] + input_box[3]:
                        field_active = True

                    else:
                        field_active = False

                if event.type == pygame.KEYDOWN:  # check what the user is inputting
                    if field_active:
                        if event.key == pygame.K_BACKSPACE:
                            user_field = user_field[:-1]  # remove the last str if they click backspace
                            # draw over what they wrote to make it look like the characters are deleting
                            pygame.draw.rect(screen, WHITE,
                                             (input_box[0], input_box[1],
                                              input_box[2], input_box[3]))
                            display_input = roman_20.render(user_field, 1, BLACK)
                            screen.blit(display_input,
                                        (input_box[0] + 10,
                                         input_box[1] + 20))  # print the new text
                            pygame.display.flip()

                        elif event.key == pygame.K_RETURN:
                            error = check_errors(field, user_field)


                            if error == False:
                                find_field = False  # if there are no errors, stop asking for the Field

                        else:
                            user_field += event.unicode  # add the input to the user_id str

            # create a border on the text box based off what the user is doing
            if field_active == True:
                pygame.draw.rect(screen, GREEN,(input_box[0], input_box[1], input_box[2], input_box[3]), 4)
            else:
                pygame.draw.rect(screen, RED,(input_box[0], input_box[1], input_box[2], input_box[3]), 4)

            # continuously display what the user is inputting
            display_input = roman_20.render(user_field, 1, BLACK)
            screen.blit(display_input, (input_box[0] + 10, input_box[1] + 20))
            pygame.display.flip()

        empty_record.append(user_field)

    if running_add == True:
        players.append(empty_record)
        update_file()
        curr_state = MENU_PAD



def delete_record():
    global curr_state

    # get ID
    pygame.draw.rect(screen, BLUE,(0, 0, WIDTH, HEIGHT))  # create blue background
    input_box = [200, 200, 400, 100]
    pygame.draw.rect(screen, WHITE, (input_box[0], input_box[1], input_box[2],
                                     input_box[3]))  # create box to enter data

    # create back-to-menu button
    button_rect = [5, 5, 68, 30]
    text = "< Menu"
    string = roman_20.render(text, 1, BLACK)
    create_button(button_rect, string, RED)

    running_delete = True  # will be used to see if the user wants to exit the Adjust function
    find_id = True  # if this is True, ask the user for the ID
    id_active = False  # will be used to get user input
    user_id = ""

    while find_id == True and running_delete == True:
        id_display = "Please enter the player's ID."
        string = roman_30.render(id_display, 1, BLACK)
        screen.blit(string, (200, 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                curr_state = EXIT  # close the program if they click the 'X'
                find_id = False
                running_delete = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get x and y coordinates of the click
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]

                if button_rect[0] < mouse_x < button_rect[0] + button_rect[2] and button_rect[1] < mouse_y < \
                        button_rect[1] + button_rect[3]:
                    curr_state = MENU_PAD
                    find_id = False
                    running_delete = False

                # if they click the text box, make it so that they are now inputting data
                elif input_box[0] < mouse_x < input_box[0] + input_box[2] and input_box[1] < mouse_y < input_box[1] + \
                        input_box[3]:
                    id_active = True

                else:
                    id_active = False

            if event.type == pygame.KEYDOWN:  # check what the user is inputting
                if id_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_id = user_id[:
                                          -1]  # remove the last str if they click backspace
                        # draw over what they wrote to make it look like the characters are deleting
                        pygame.draw.rect(screen, WHITE,
                                         (input_box[0], input_box[1],
                                          input_box[2], input_box[3]))
                        display_input = roman_20.render(user_id, 1, BLACK)
                        screen.blit(display_input,
                                    (input_box[0] + 10,
                                     input_box[1] + 20))  # print the new text
                        pygame.display.flip()

                    elif event.key == pygame.K_RETURN:
                        player_ids = []  # will contain the ID's of each player
                        for player in players:  # add each player's ID
                            player_id = player[id_location]
                            player_ids.append(player_id)

                        if user_id not in player_ids:  # if the user put in an ID which does not exist, stop the function
                            error_text = "Error: Invalid input. Please enter a valid Player ID."
                            error_box = [0, 350, WIDTH, 150]
                            display_error(error_text, error_box, BLUE)

                        else:
                            find_id = False  # if there are no errors, stop asking for the ID

                    else:
                        user_id += event.unicode  # add the input to the user_id str

        # create a border on the text box based off what the user is doing
        if id_active == True:
            pygame.draw.rect(
                screen, GREEN,
                (input_box[0], input_box[1], input_box[2], input_box[3]), 4)
        else:
            pygame.draw.rect(
                screen, RED,
                (input_box[0], input_box[1], input_box[2], input_box[3]), 4)

        # continuously display what the user is inputting
        display_input = roman_20.render(user_id, 1, BLACK)
        screen.blit(display_input, (input_box[0] + 10, input_box[1] + 20))
        pygame.display.flip()

    # delete the record of the ID
    # only do this if the user is still in the Delete function
    if running_delete == True:
        # check the id of every player and if it is the same as the user's desired id, remove that player list from the players list
        for player in players:
            if player[id_location] == user_id:
                players.remove(player)

        update_file()  # update the file with the new data

        curr_state = MENU_PAD


def view_reports():
    global curr_state

    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, HEIGHT))  # draw blue background

    # create back-to-menu button
    button_rect = [5, 5, 68, 30]
    text = "< Menu"
    string = roman_20.render(text, 1, BLACK)
    create_button(button_rect, string, RED)

    # collect the stats
    stats = []

    # find IDs of players over 200 lbs
    ppl_200 = []  # will contain the players over 200 lbs
    for player in players:  # check each player's weight
        weight = player[weight_location]
        if int(weight) > 200:  # cast as int since it is orginally a str
            ppl_200.append(player[id_location])
    stat1 = "Players (IDs) over 200 lbs: "
    for id in ppl_200:
        if id == ppl_200[-1]:  # only add a period for the last name
            stat1 += id + "."
        else:
            stat1 += id + ", "
    stats.append(stat1)

    # find IDs of Players on the Toronto Raptors
    ppl_tor = []  # will contain the IDs players on the Raptors
    for player in players:  # check every player's team
        team = player[team_location]
        if team == "TOR":
            ppl_tor.append(player[id_location])
    stat2 = "Players (IDs) on the Toronto Raptors: "
    for id in ppl_tor:
        if id == ppl_tor[-1]:  # only add a period for the last name
            stat2 += id + "."
        else:
            stat2 += id + ", "
    stats.append(stat2)

    # find IDs of players with a last name less than 6 chars long
    ppl_lname6 = []  # will contain IDs of players with the specified type of last name
    for player in players:  # check last name for each player
        last_name = player[lname_location]
        if len(last_name) < 6:
            ppl_lname6.append(player[id_location])
    stat3 = "Players (IDs) with last name < 6 long: "
    for id in ppl_lname6:
        if id == ppl_lname6[-1]:  # only add a period for the last name
            stat3 += id + "."
        else:
            stat3 += id + ", "
    stats.append(stat3)

    start_y = 120
    for stat in stats:
        text = stat
        text_str = roman_30.render(text, 1, BLACK)
        screen.blit(text_str, (5, start_y))
        start_y += 100  # make each stat move down

    pygame.display.flip()

    running_stats = True
    while running_stats:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                curr_state = EXIT  # close the program if they click the 'X'
                running_stats = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get x and y coordinates of the click
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                # if they click the "< Menu" button, take them back to the menu
                if button_rect[0] < mouse_x < (
                        button_rect[0] +
                        button_rect[2]) and button_rect[1] < mouse_y < (
                        button_rect[1] + button_rect[3]):
                    curr_state = MENU_PAD
                    running_stats = False



# Part 3: variables
# data variables:
players = []  # will contain data on all players

field_titles = [
    "Player ID", "First Name", "Last Name", "Team", "Jersey #", "Position",
    "Weight (lbs)"
]
# will contain the indexes of each field
id_location = field_titles.index("Player ID")
fname_location = field_titles.index("First Name")
lname_location = field_titles.index("Last Name")
team_location = field_titles.index("Team")
jersey_location = field_titles.index("Jersey #")
pos_location = field_titles.index("Position")
weight_location = field_titles.index("Weight (lbs)")
# will contain the max length each field can be
max_lenid = 9
max_lenname = 15
max_lenteam = 3
max_lenjersey = 2
max_lenpos = 8
max_lenweight = 3

# main while loop:
working = True  # will be used to turn off the loop generating the picture

# get the information from the data file
player_data = open("NBA_Players.dat", "r")

while True:
    player_info = player_data.readline()
    if player_info == "":
        break

    player_info = player_info.rstrip("\n")
    data = player_info.split(",")

    players.append(data)

player_data.close()

# Part 3: create the picture
# while the working variable == True, create the picture
while working:
    # turn the program off if the user clicks "X"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            working = False

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if curr_state = MENU_PAD:

    print(curr_state)
    if curr_state == MENU_PAD:
        menu_pad()
    elif curr_state == DISPLAY_TABLE:
        display_table()
    elif curr_state == ADJUST_FIELD:
        adjust_field()
    elif curr_state == ADD_RECORD:
        add_record()
    elif curr_state == DELETE_RECORD:
        delete_record()
    elif curr_state == VIEW_REPORTS:
        view_reports()
    else:  # curr_state = EXIT
        break

pygame.quit()
