from ipywidgets import HTML, Text, HBox, Button, Output, VBox
from IPython.display import clear_output, display
from IPython.display import HTML as ipyHTML
from WordleHelper import Wordle

wordle = Wordle()

title_label = HTML("<h1>Wordle Helper</h1>")

incorrect_letter_label = HTML("<h2>Insert Incorrect Letters:</h2>")
incorrect_letters_box = HBox(
    [Text(description=str(i), placeholder="", width="10%") for i in range(1, 6)]
)

incorrect_place_label = HTML("<h2>Insert Correct Letters in the Incorrect Place:</h2>")
incorrect_place_box = HBox(
    [Text(description=str(i), placeholder="", width="10%") for i in range(1, 6)]
)

correct_place_label = HTML("<h2>Insert Correct Letters in the Correct Place:</h2>")
correct_place_box = HBox(
    [Text(description=str(i), placeholder="", width="10%") for i in range(1, 6)]
)

button_update = Button(
    description="Update Letters",
    tooltip="Update Letters",
    style={"description_width": "initial"},
)

button_reset = Button(
    description="Reset", tooltip="Reset", style={"description_width": "initial"}
)

output = Output()


def update_letters(event):
    with output:
        clear_output()
        incorrect_letters = []
        incorrect_place = []
        correct_place = []
        for count, i in enumerate(incorrect_letters_box.children):
            if i.value != "":
                incorrect_place.append(i.value)
        for count, i in enumerate(incorrect_place_box.children):
            if i.value != "":
                incorrect_place.append((count, i.value))
        for count, i in enumerate(correct_place_box.children):
            if i.value != "":
                correct_place.append((count, i.value))
        guess = wordle.update(
            incorrect_letters=incorrect_letters,
            incorrect_place=incorrect_place,
            correct_place=correct_place,
        )
        if guess is not None:
            display(ipyHTML("<h2>Possible Words:</h2>"))
            for i in guess:
                display(ipyHTML(i))

       
def reset_letters(event):
    with output:
        clear_output()
        wordle.reset()
        display(ipyHTML("<h3>Letters have been reset</h3>"))


button_update.on_click(update_letters)
button_reset.on_click(reset_letters)

WordleWidget = VBox(
    [
        title_label,
        incorrect_letter_label,
        incorrect_letters_box,
        incorrect_place_label,
        incorrect_place_box,
        correct_place_label,
        correct_place_box,
        HBox([button_update, button_reset]),
        output,
    ]
)
