import PySimpleGUI as sg
import SwedishWordle
from file_score_upd import file_score_upd
from open_hiscore import open_hiscore
from layout import layout_func
from layout import layout2_func
from result_text_func import result_text_func
from change_theme import change_theme

#Skapa ett nytt wordlespel med ord som är 5 långa
game = SwedishWordle.Game(5)

#Definierar grundläggande grafik
def TextChar(value, key):
    return sg.Input(value, key=key, font='Courier 22', size=(10,100), border_width=5,  p=1, enable_events=True, disabled=True)

#Funktion för grafisk uppdatering av score, för kompression av kod
def visual_score_update(score, window):
    window['yiscore'].update(score)                                            #Aktuellt score
    window['High_Score'].update((open_hiscore()))                              #High Score

#Hanterar skapandet av fönster
def wordle_func():  
    score = 0                                                                  #Score på varje enskilt game
    row = 1                                                                    #Spelsekvens, variabel för stegen i spelet.
    sg.theme('Dark blue')                                                      
    window = sg.Window("Wordle SE", layout_func(), finalize=True)
    
    while True:
        
        event, values = window.read()                                          #Inleder, window
        guess = values['input_box']                                            #Input från användare får en variabel, separerar logik/grafik
        result = game.Guess(guess)                                             #Result definieras
        text_output = result_text_func(result)                                 #Grafiken för din skrivna text

        #Om ogiltigt ord
        if len(guess) != 5 and row <= 5 and event == "confirm_button":
            window['string'+str(row)].update("Felaktig längd på ord. Du gissade " + guess + ". Detta spel är om ord som är 5 i längd")

        #Inställningar    
        elif event == "settings_button":
            window_theme = sg.Window('Wordle Wizard', layout2_func())          #Skapar settings-fönster
            
            #Funktioner för olika knapptryck för wordle wizard, ändra färg
            window, event = change_theme(window, window_theme)
                        
        #Nytt spel
        elif event == "new_game_button":
            window.close()

            #Skapa ett nytt wordlespel med ord som är 5 långa
            SwedishWordle.Game(5)

            #Starta GUI
            wordle_func()

        #Vid korrekt svar
        elif sum(result) == 0:                
            window['string'+str(6)].update("Knasvinst län")                    #Grafik meddelande vinst
            visual_score_update(score, window)                                 #Grafik uppdateas för score      
            file_score_upd(score) 
            
        #Vanlig gissning
        elif event == "confirm_button" and row <= len(result):           
            
            #Om gränsen för antalet gissningar överskrids, förlorar du
            if row == len(result):
                window['string'+str(6)].update("Choktorsk bram")
                visual_score_update(score, window)                              #Grafik uppdateras för score
            
            #Grafisk validering av gissade ordet                                        
            score = score + sum(result)                                         #Score uppdateras
            window['string'+str(row)].update((text_output,guess))               #Grafik uppdateras för svar
            visual_score_update(score, window)                                  #Grafik uppdateas för score
            row += 1
            
        #Om man stänger wordle
        elif event == sg.WIN_CLOSED:
            window.close()




