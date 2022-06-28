#Libraries and dependencies 
import time
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State , MATCH, ALL
from dash_bootstrap_templates import load_figure_template
from transformers import AutoModelWithLMHead, AutoTokenizer
import torch
import plotly.express as px



# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
print(f"Device: {device}")

print("Start loading model...")
name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelWithLMHead.from_pretrained(name)

# Switch to cuda, eval mode, and FP16 for faster inference
if device == "cuda":
    model = model.half()
model.to(device)
model.eval()

print("Done.")


def textbox(text, box="other"):
    style = {
        "max-width": "55%",
        "width": "max-content",
        "padding": "10px 15px",
        "border-radius": "25px",
    }

    if box == "self":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        color = "primary"
        inverse = True

    elif box == "other":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        color = "light"
        inverse = False

    else:
        raise ValueError("Incorrect option for `box`.")

    return dbc.Card(text, style=style, body=True, color=color, inverse=inverse)


conversation = html.Div(
    style={
        "width": "80%",
        "max-width": "800px",
        "height": "60vh",
        "margin": "auto",
        "overflow-y": "auto",
    },
    id="display-conversation",
)

controls = dbc.InputGroup(
    style={"width": "80%", "max-width": "800px", "margin": "auto"},
    children=[
        dbc.Input(id="user-input", placeholder="Send a messsage to Dashy", type="text"),
        dbc.InputGroupAddon(dbc.Button("Submit", id="submit"), addon_type="append",),
    ],
)

####begining of Layout edits
df = px.data.gapminder()

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]

load_figure_template(templates)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
### end of layout edits

server = app.server
#Dictionary containing Disney parks and rides

all_options = {
    'Walt Disney World Resort': ['Dumbo the Flying Elephant', 'The Seas with Nemo & Friends', 'Turtle Talk with Crush'],
    'Disneyland Resort': [u'Autotopia', 'Space Mountain', 'Soarin'],
    'Tokyo Disney Resort': [u'Toy Story Mania', 'Splash Mountain', 'Raging Spirits'],
    'Disneyland Paris': [u'Adventure Isle', 'Autotopia', 'Big Thunder Mountain'],
    'Hong Kong Disneyland Resort': [u'Mystic Manor', 'Iron Man Experience', 'Fantasy Gardens'],
    'Shanghai Disney Resort': [u'JetPacks', 'Roaring Rapids', 'Tron Lightcycle Power Run'],
}

app.layout = dbc.Container(
    fluid=True,
    children=[
        html.H1("Chat with Dashy"),
        html.H6("Hi! I am Dashy a chatbot based on GPT that was trained on 147 million comments+ from Reddit"),
        html.Hr(),
        dcc.Store(id="store-conversation", data=""),
        conversation,
        controls,
        html.Hr(),
        html.H6("Select the Disney Park from Drop Down List"),
        dcc.Dropdown(list(all_options.keys()), id='park_rides',),
         html.Div('Things I would like to do at Disney'),
        dcc.Input(id="new-item"),
        html.Button("Add", id="add"),
        html.Button("Clear Done", id="clear-done"),
        html.Div(id="list-container"),
        html.Div(id="totals")



        ])



style_todo = {"display": "inline", "margin": "10px"}
style_done = {"textDecoration": "line-through", "color": "#888"}
style_done.update(style_todo)




## callback for backend of chatbot
@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [
        textbox(x, box="self") if i % 2 == 0 else textbox(x, box="other")
        for i, x in enumerate(chat_history.split(tokenizer.eos_token)[:-1])
    ]


@app.callback(
    [Output("store-conversation", "data"), Output("user-input", "value")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    if n_clicks == 0:
        return "", ""

    if user_input is None or user_input == "":
        return chat_history, ""

    # # temporary
    # return chat_history + user_input + "<|endoftext|>" + user_input + "<|endoftext|>", ""

    # encode the new user input, add the eos_token and return a tensor in Pytorch
    bot_input_ids = tokenizer.encode(
        chat_history + user_input + tokenizer.eos_token, return_tensors="pt"
    ).to(device)

    # generated a response while limiting the total chat history to 1000 tokens,
    chat_history_ids = model.generate(
        bot_input_ids, max_length=1024, pad_token_id=tokenizer.eos_token_id
    )
    chat_history = tokenizer.decode(chat_history_ids[0])

    return chat_history, ""
#### Call back for todo list
@app.callback(
    [
        Output("list-container", "children"),
        Output("new-item", "value")
    ],
    [
        Input("add", "n_clicks"),
        Input("new-item", "n_submit"),
        Input("clear-done", "n_clicks")
    ],
    [
        State("new-item", "value"),
        State({"index": ALL}, "children"),
        State({"index": ALL, "type": "done"}, "value")
    ]
)
def edit_list(add, add2, clear, new_item, items, items_done):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    adding = len([1 for i in triggered if i in ("add.n_clicks", "new-item.n_submit")])
    clearing = len([1 for i in triggered if i == "clear-done.n_clicks"])
    new_spec = [
        (text, done) for text, done in zip(items, items_done)
        if not (clearing and done)
    ]
    if adding:
        new_spec.append((new_item, []))
    new_list = [
        html.Div([
            dcc.Checklist(
                id={"index": i, "type": "done"},
                options=[{"label": "", "value": "done"}],
                value=done,
                style={"display": "inline"},
                labelStyle={"display": "inline"}
            ),
            html.Div(text, id={"index": i}, style=style_done if done else style_todo)
        ], style={"clear": "both"})
        for i, (text, done) in enumerate(new_spec)
    ]
    return [new_list, "" if adding else new_item]


@app.callback(
    Output({"index": MATCH}, "style"),
    Input({"index": MATCH, "type": "done"}, "value")
)
def mark_done(done):
    return style_done if done else style_todo


@app.callback(
    Output("totals", "children"),
    Input({"index": ALL, "type": "done"}, "value")
)
def show_totals(done):
    count_all = len(done)
    count_done = len([d for d in done if d])
    result = "{} of {} items completed".format(count_done, count_all)
    if count_all:
        result += " - {}%".format(int(100 * count_done / count_all))
    return result

####
if __name__ == "__main__":
    app.run_server(debug=True)

