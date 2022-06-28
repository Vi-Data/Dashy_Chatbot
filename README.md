# Dash Summarization
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/plotly/dash-sample-apps/blob/master/apps/dash-chatbot/ColabDemo.ipynb)

This app lets you chat with [DialoGPT](https://huggingface.co/transformers/model_doc/dialogpt.html), a chatbot based on GPT that was trained on 147M comments+replies from Reddit. The model was developed by [Microsoft Research](https://github.com/microsoft/DialoGPT), and it is hosted on [Huggingface's model repository](https://huggingface.co/microsoft/DialoGPT-large).

![Dashy_Disney_Demo](https://github.com/Vi-Data/NLP_BOT/blob/main/Dashy_Disney_Demo.gif)
## Instructions


To get started, first clone this repo:
```
git clone https://github.com/plotly/dash-sample-apps.git
cd dash-sample-apps/apps/dash-chatbot
```

Create a conda env (or venv) and install the requirements:
```
conda create -n dash-chatbot python=3.7.6
conda activate dash-chatbot
pip install -r requirements.txt
```

You can now run the app:
```
python app.py
```

and visit http://127.0.0.1:8050/.


## Changes to chatbot

The intentions for Dashy the chatbot is to help Disney (current or potential) guests gather more information regarding the different theme parks as well as organize and plan a trip to the happiest place on earth. 

This dash application allows for users to talk to a chatbot. Select from a list of Disney Parks and create a to-do list. Currently a proof of concept and will need further development in order to be fully functional.

## Future Development

If given more time, the chatbot would be given multilingual abilities. Such as being able to converse in Spanish, French and Chinese. As well as accuracy of Disney's Parks information such as available ride and or more accurate Park Hours as that information is more dynamic. By choosing to train models on more Disney specific dataset, chat bot could be improved. The dash app could be improved by providing guests with links and maps to the Disney Parks.
