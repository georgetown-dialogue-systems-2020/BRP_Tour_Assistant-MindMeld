# BRP_Tour_Assistant-MindMeld

The Blue Ridge Parkway tour assistant is a dialogue system built on the [MindMeld Conversational AI Platform](https://www.mindmeld.com/).

## Requirements

This system requires MindMeld, Python 3.6 or 3.7, and Elasticsearch running in the background.
You can follow the guide in the MindMeld [documentation](https://www.mindmeld.com/docs/userguide/getting_started.html#install-mindmeld) to install all the requirements.

## Quick Start

Assuming you have installed all the pre-requisites, make sure to run Elasticsearch in the very beginning.
```bash
./elasticsearch-7.8.0/bin/elasticsearch
```

Then load all the knowledge bases used in the system.
```bash
python -m tour_assistant load-kb tour_assistant lodgings tour_assistant/data/lodgings.json
python -m tour_assistant load-kb tour_assistant overlooks tour_assistant/data/overlooks.json
python -m tour_assistant load-kb tour_assistant restaurants tour_assistant/data/restaurants.json
python -m tour_assistant load-kb tour_assistant trails tour_assistant/data/trails.json
```

Build the Natural Language Processing models that power the app.
```bash
python -m tour_assistant build
```
Because of some unknown issues (I guess it is about the supervised learning), this `build` operation might fail. If it occurs, just try again.

Now, it is all set. Use `converse` to communicate with the system.
```bash
python -m tour_assistant converse
```
