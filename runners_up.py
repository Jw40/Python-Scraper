from urllib.request import urlopen
from webbrowser import open as urldisplay
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
import re
from re import findall, finditer, MULTILINE, DOTALL
from sqlite3 import *
from array import array

#download and open_html_file functions were sourced externally

def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = True,
             got_the_message = True):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))


import tkinter as tk

### url stored in variable

steam_games_url = 'https://store.steampowered.com/stats/Steam-Game-and-Player-Statistics'
billboard_top_100_url = 'https://open.spotify.com/playlist/4joqw3e0n9gDNVDhgKapCU'
top_10_shows_url = 'https://streamingtvcharts.com/'

############## GLOBAL variables to be called later
global updated_list, r_var, runner_up, the_rest, value, runner_up_value
updated_list = []
r_var = 0
runner_up = []
the_rest = []
value = []
runner_up_value = []

############## find top 10 list of current players STATIC link - steam
def find_game_ranking():
    global updated_list, r_var, pattern, pattern_1, runner_up, the_rest, value, runner_up_value
    updated_list.clear()
    runner_up.clear()
    the_rest.clear()
    value.clear()
    runner_up_value.clear()
    r_var = 1
    #open and read static file link
    data = open(file = 'download1.html', encoding="utf8")
    filecontents = data.read()
    # regular expression to find the top 10 games and online players from data contents
    pattern = re.findall("""/[0-9]{1,10}/[A-Za-z_\d{4}]*/">([:A-Z" "'a-z\d{4}_-]+)</a>""", filecontents)
    pattern_1 = re.findall("""<span class="currentServers">([0-9,]{6,7})</span>""", filecontents)
    players = []
    #limit results to 10 results and every second result
    for pattern_1 in pattern_1[0::2][0:10]:
        players.append(str(pattern_1))
    a = 0
    #limit results of list to 10 games
    for pattern in pattern[0:10]:
         #if item is 2nd add values to array's 
        if a == 1:
            updated_list.append('2nd place:  ' + pattern + ': ' + players[a] +'\n')
            runner_up.append(pattern)
            runner_up_value.append(players[a])
        #else if item is not second add values to array's
        else: 
            updated_list.append(str(a+1) + ':' + pattern + ': ' + players[a] +'\n')
            the_rest.append(pattern)
            value.append(players[a])
        a += 1
        
############ find top 10 list of player currently ONLINE - steam
def find_online_game_ranking():
    
    #call download function to download the steam_games_url which the html link is stored in
    data_2 = download(steam_games_url)
    global updated_list, r_var, pattern_3, pattern_4, runner_up, the_rest, value, runner_up_value
    updated_list.clear()
    runner_up.clear()
    the_rest.clear()
    value.clear()
    runner_up_value.clear()
    r_var = 2
    #regular experssion to find the top 10 games and online players from data contents
    pattern_3 = re.findall("""/[0-9]{1,10}/[A-Za-z_\d{4}]*/">([:A-Z" "'a-z\d{4}_-]+)</a>""", data_2)
    pattern_4 = re.findall("""<span class="currentServers">([0-9,]{6,7})</span>""", data_2)
    players = []
    #limit list to 10 and every second result 
    for pattern_4 in pattern_4[0::2][0:10]:
        players.append(str(pattern_4))
    a = 0
    #limit results to 10
    for pattern_3 in pattern_3[0:10]:
         #if item is 2nd add values to array's 
        if a == 1:
            updated_list.append('2nd place: ' + pattern_3 + ': ' + players[a] +'\n')
            runner_up.append(pattern_3)
            runner_up_value.append(players[a])
        #else if item is not second add values to array's
        else: 
            updated_list.append(str(a+1) + ':' + pattern_3 + ': ' + players[a] +'\n')
            the_rest.append(pattern_3)
            value.append(players[a])
        a += 1

############ find top 10 list of artist and song name ONLINE- billboard top 100
def find_online_music():
    global updated_list, r_var, pattern_5, pattern_6, runner_up, the_rest, value, runner_up_value
    updated_list.clear()
    runner_up.clear()
    the_rest.clear()
    value.clear()
    runner_up_value.clear()
    r_var = 3
    #call download function to download the billboard_top_100_url which the html link is stored in
    data_3 = download(billboard_top_100_url)
    ###regular rexpression to find the names of artists in the top 10
    pattern_5 = re.findall("""" tabindex="-1"><span dir="auto">([A-Za-z ,]+[A-Za-z ])</span></a>     &bull; """, data_3)
    pattern_6 = re.findall("""dir="auto">([(\)\[A-Za-z &amp;,-]+)</span><span""", data_3)
    players = []
    #limit results to 10
    for pattern_6 in pattern_6[0:10]:
    ###replaces all instances of &amp; in the html file to '&'
        pattern_6 = pattern_6.replace('&amp;','&')
        players.append(str(pattern_6))
    a = 0
    #limit results to 10, and for each item in pattern 
    for pattern_5 in pattern_5[0:10]:
        #if item is 2nd add values to array's 
        if a == 1:
            updated_list.append('2nd place:  ' + pattern_5 + ':  ' + players[a] +'\n')
            runner_up.append(pattern_5)
            runner_up_value.append(players[a])
        #else if item is not second add values to array's
        else: 
            updated_list.append(str(a+1) + ': ' + pattern_5 + ':  ' + players[a] +'\n')
            the_rest.append(pattern_5)
            value.append(players[a])
        a += 1

########## find top 10 list of Tv shows or movies from ONLINE streaming websites
def find_online_show():
    global updated_list, r_var, pattern_7, pattern_8, runner_up, the_rest, value, runner_up_value
    updated_list.clear()
    runner_up.clear()
    the_rest.clear()
    value.clear()
    runner_up_value.clear()
    r_var = 4
    #call download function to download the top_10_shows_url which the html link is stored in
    data_4 = download(top_10_shows_url)
    ###regular expression to find the name and rating of the streaming program
    pattern_7 = re.findall("""<span>&nbsp;([A-Za-z ]+)</span></div><div class="jet-listing-dynamic-repeater__delimiter">""", data_4)
    pattern_8 = re.findall("""<span>*([0-9. ]+[A-Za-z]+)</span></div><div class="jet-listing-dynamic-repeater__delimiter"> </div>""", data_4)
    players = []
    #limit list to 10
    for pattern_8 in pattern_8[0:10]:
        players.append(str(pattern_8))
    a = 0
    #limit list to 10 and create 4 arrays 
    for pattern_7 in pattern_7[0:10]:
        if a == 1:
            updated_list.append('2nd place: ' + pattern_7 + ': ' + players[a] +'\n')
            runner_up.append(pattern_7)
            runner_up_value.append(players[a])
        else: 
            updated_list.append(str(a+1) + ':' + pattern_7 + ': ' + players[a] +'\n')
            the_rest.append(pattern_7)
            value.append(players[a])
        a += 1
       
###############update button command to insert the updated_lists
def updated():
    #ensure list can be inserted once
    display_box_1.delete('1.0',END)
    display_box_2.delete('1.0',END)
    for i in range(0,10):
        if i == 1:
            display_box_1.insert(END, updated_list[i])
        else:
            display_box_2.insert(END, updated_list[i])
   
#############find source button to load the source html link or file with the open_html_file function and urldisplay
def find_source_url():
    if r_var == 1:
        open_html_file('download1.html')
    elif r_var == 2:
        urldisplay(url = 'https://store.steampowered.com/stats/Steam-Game-and-Player-Statistics')
    elif r_var == 3:
        urldisplay(url = 'https://open.spotify.com/playlist/4joqw3e0n9gDNVDhgKapCU')
    elif r_var == 4:
        urldisplay(url = 'https://streamingtvcharts.com/')

################# save_button to save to db browers SQL LITE - INSERT INFO - DELETE when user presses the save button

    
def save_button():
    #open connection to db
    try:
        connection = connect(database = 'runners_up.db')
        runnersup_db = connection.cursor()
        print("Connected to SQLite")
        
        sql_delete_query = """DELETE from others"""
        sql_delete_query1 = """DELETE from runner_up"""
        runnersup_db.execute(sql_delete_query)
        runnersup_db.execute(sql_delete_query1)
        connection.commit()
        print('DELETING ALL ITEMS IN TABLE others AND runner_up')
        
        #update the static games list into the database
        if r_var == 1:
            # for each item in the_rest array upto postiton 9 insert into others table
            insert_others_statement = """INSERT INTO others(position, competitor, property) VALUES (?,?,?)"""
            for i in range(0,9):
                others_values = (i+1, the_rest[i], value[i])
                runnersup_db.execute(insert_others_statement, others_values)
                connection.commit()
                print('Number of rows affected:', runnersup_db.rowcount)
            # for each item in runners_up array upto postiton 1 insert into runner_up table
            insert_runner_up_statement = """INSERT INTO runner_up(competitor, property) VALUES (?, ?)"""   
            for i in range(1):
                runner_up_insert = (runner_up[i], runner_up_value[i])
                runnersup_db.execute(insert_runner_up_statement, runner_up_insert)
                connection.commit()
                print('Number of rows affected:', runnersup_db.rowcount)
                runnersup_db.close()
                
        #update the online games list into the database   
        elif r_var == 2:
            # for each item in the_rest array upto postiton 9 insert into others table
            insert_others_statement = """INSERT INTO others(position, competitor, property) VALUES (?,?,?)"""
            for i in range(0,9):
                others_values = (i+1, the_rest[i], value[i])
                runnersup_db.execute(insert_others_statement, others_values)
                connection.commit()
                print('Number of rows affected:', runnersup_db.rowcount)
            # for each item in runners_up array upto postiton 1 insert into runner_up table  
            insert_runner_up_statement = """INSERT INTO runner_up(competitor, property) VALUES (?, ?)"""   
            for i in range(1):
                runner_up_insert = (runner_up[i], runner_up_value[i])
                runnersup_db.execute(insert_runner_up_statement, runner_up_insert)
                connection.commit()
                print('Number of rows affected:', runnersup_db.rowcount)
                runnersup_db.close()
               
        #update the online music list into the database  
        elif r_var == 3:
            # for each item in the_rest array upto postiton 9 insert into others table
            insert_others_statement = """INSERT INTO others(position, competitor, property) VALUES (?,?,?)"""
            for i in range(0,9):
                others_values = (i+1, the_rest[i], value[i])
                runnersup_db.execute(insert_others_statement, others_values)
                connection.commit()
                print('Number of rows affected:', runnersup_db.rowcount)
            # for each item in runners_up array upto postiton 1 insert into runner_up table    
            insert_runner_up_statement = """INSERT INTO runner_up(competitor, property) VALUES (?, ?)"""   
            for i in range(1):
                runner_up_insert = (runner_up[i], runner_up_value[i])
                runnersup_db.execute(insert_runner_up_statement, runner_up_insert)
                connection.commit()
                print('Number of rows affected:', runnersup_db.rowcount)
                runnersup_db.close()
    
        #update the online streaming programs into the database    
        elif r_var == 4:
            # for each item in the_rest array upto postiton 9 insert into others table
            insert_others_statement = """INSERT INTO others(position, competitor, property) VALUES (?,?,?)"""
            for i in range(0,9):
                others_values = (i+1, the_rest[i], value[i])
                runnersup_db.execute(insert_others_statement, others_values)
                connection.commit()
                print('Number of rows affected:', runnersup_db.rowcount)
            # for each item in runners_up array upto postiton 1 insert into runner_up table  
            insert_runner_up_statement = """INSERT INTO runner_up(competitor, property) VALUES (?, ?)"""   
            for i in range(1):
                runner_up_insert = (runner_up[i], runner_up_value[i])
                runnersup_db.execute(insert_runner_up_statement, runner_up_insert)
                connection.commit()
                print('Number of rows affected:', runnersup_db.rowcount)
                runnersup_db.close()
    except Error as e:
        print(e)
    #close connection to db            
    finally:
        if (connection):
            connection.close()
            print('Disconnect to SQLITE')
    
    

##########################################
####Main GUI
window = Tk()
#set the title of the GUI and background colour
window.title('Shannon Noll Presenting Todays 2nd Place')
window.configure(background='gold')

####My Background - select image and place on grid
photo1 = PhotoImage(file='rutgif.gif')
Label (window, image=photo1, bg='gold', borderwidth = 10) .grid(row=1, column=0, rowspan = 10, columnspan = 10, stick = NW)

####create Currently in 2nd place LabelFrame with 3 radio buttons and place them on grid
label_frame_1 = LabelFrame(window, font = ('Arial 20 bold'), fg = 'black', bg = 'gold', borderwidth = 5, text = 'Currently 2nd place')

r = IntVar()

Current_1_label = Radiobutton(label_frame_1, text = 'Most Popular Online Steam Games\n[Title, Players Online]', borderwidth = 2, bg ='gold', fg='black', font=('Times', 18),
                        pady = 1, padx = 1,variable = r, value = 1, command = find_online_game_ranking) .grid(row=1,column=1, stick = W)

Current_2_label = Radiobutton(label_frame_1, text = 'Most Popular Music - Spotify\n[Artist, Song Name]', bg ='gold', fg='black', font=('Times', 18),
                        pady = 1, padx = 1, variable = r, value = 2, command = find_online_music) .grid(row=2,column=1, stick = W)

Current_3_label = Radiobutton(label_frame_1, text = 'Most Popular Streamed Program\n[Title, Imdb rating]', bg ='gold', fg='black', font=('Times', 18),
                        pady = 1, padx = 1, variable = r, value = 3, command = find_online_show) .grid(row=3,column=1, stick = W)

margin = 5
#pack label frame on grid
label_frame_1.grid(padx = margin, pady = margin,
                              row = 1, column = 3, sticky = NE)

####create Previously in 2nd place LabelFrame with 1 radio button and place on the grid

label_frame_2 = LabelFrame(window, font = ('Arial 20 bold'), fg = 'black', bg = 'gold', borderwidth = 5, text = 'Previously 2nd place')

Previous_1_label = Radiobutton(label_frame_2, text = 'Most Popular Online Steam Games\n[Title, Players Online]', borderwidth = 2, bg ='gold', fg='black', font=('Times', 18),
                        pady = 1, padx = 1, variable = r , value = 4, command = find_game_ranking) .grid(row=1,column=1, stick = W)

label_frame_2.grid(padx = margin, pady = margin,
                              row = 2, column = 3, stick = NE)

####create update button and place on the grid

Update_button = Button(window, font = ('Times', 18), fg = 'black', bg = 'white', borderwidth = 3, text = 'Update', padx = 20, command = updated)

Update_button.grid(padx = 10, pady = 5, row = 3, column = 2, stick = W)

####create find source button and place on the grid

Find_source = Button(window, font = ('Times', 18), fg = 'black', bg = 'white', borderwidth = 3, text = 'Find Source', padx = 20, command = find_source_url)

Find_source.grid(padx = 10, pady = 5, row = 3, column = 3, stick = E)

###create save to database button and place on the grid

Save = Button(window, font = ('Times', 18), fg = 'black', bg = 'white', borderwidth = 3, text = 'Save', padx = 20, command = save_button, state = NORMAL)

Save.grid(padx = 10, pady = 5, row = 3, column = 3, stick = W)

####2nd place display box
display_box_1 = Text(window, width = 45, height = 14,
                             font = ('Arial', 15),
                             borderwidth = 5, relief = 'groove')

###Place 2nd_place_textbox on grid
display_box_1.grid(padx = margin, pady = margin,
                              row = 10, column = 2, stick = W)

####top 10 display box
display_box_2 = Text(window, width = 45, height = 14,
                             font = ('Arial', 15),
                             borderwidth = 5, relief = 'groove')
###place top 10 textbox on the grid
display_box_2.grid(padx = margin, pady = margin,
                              row = 10, column = 3, stick = E)
####create presented by title 
sub_title = Label(window, font = ('Arial 12 bold'), fg = 'black', bg = 'gold', text = '2nd Place is Presented by \nShannon Noll, Australian Idols 2003 Runner up.')

###place sub title on grid
sub_title.grid(pady = 5, row = 3, column = 2, stick = E)

window.mainloop()


