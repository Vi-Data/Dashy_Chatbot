# Dash Summarization
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/plotly/dash-sample-apps/blob/master/apps/dash-chatbot/ColabDemo.ipynb)

This app lets you chat with [DialoGPT](https://huggingface.co/transformers/model_doc/dialogpt.html), a chatbot based on GPT that was trained on 147M comments+replies from Reddit. The model was developed by [Microsoft Research](https://github.com/microsoft/DialoGPT), and it is hosted on [Huggingface's model repository](https://huggingface.co/microsoft/DialoGPT-large).

![Dashy_Demo_Pic](https://user-images.githubusercontent.com/108215228/176068851-4ed75c73-0348-4452-b69d-e9c74e46518a.gif)
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

The intention for this proof of concept is to build a chatbot that would help Disney (current or potential) guest gather more information regarding the different theme parks.

The nameless chatbot was given a name and as well as different styling.


## Future Improvement
If given more time the chatbot would be given multilingual abilities. Such as being able to converse in Spanish, French and Chinese. As well as being able to view the different rides avaliable at the user selected theme park. 
